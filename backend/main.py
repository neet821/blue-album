from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import crud, models, schemas, security
from .database import SessionLocal, engine

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS 中间件 ---
# 开发环境:允许所有来源
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# --- 依赖项 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    """从 token 获取当前用户"""
    username = security.decode_access_token(token)
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 检查账号是否被禁用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been disabled",
        )
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    """验证当前用户是否为管理员"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

# --- API 路由 ---

@app.post("/api/auth/login", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/api/users/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户的信息"""
    return current_user

@app.put("/api/users/me/password")
def update_my_password(
    password_update: schemas.UserPasswordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码"""
    result = crud.update_user_password(
        db, current_user.id, password_update.old_password, password_update.new_password
    )
    if result is False:
        raise HTTPException(status_code=400, detail="Incorrect old password")
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}

# --- 管理员 API ---

@app.get("/api/admin/users", response_model=list[schemas.UserSimple])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有用户列表(仅管理员)"""
    return crud.get_all_users(db, skip=skip, limit=limit)

@app.get("/api/admin/users/{user_id}", response_model=schemas.User)
def get_user_detail(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取用户详细信息(仅管理员)"""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/admin/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新用户信息(仅管理员)"""
    # 防止管理员修改自己的角色
    if user_id == current_admin.id and user_update.role:
        raise HTTPException(status_code=400, detail="Cannot modify your own role")
    
    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/admin/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除用户(仅管理员)"""
    # 防止管理员删除自己
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.get("/api/posts", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    # 如果没有文章，可以返回一些临时数据用于前端展示
    if not posts:
        return [
            {"id": 1, "title": "欢迎来到我的博客", "content": "这是第一篇示例文章。", "author_id": 1, "created_at": "2025-10-11T12:00:00"},
            {"id": 2, "title": "关于 FastAPI 和 Vue", "content": "这是一个强大的组合。", "author_id": 1, "created_at": "2025-10-10T15:30:00"},
        ]
    return posts

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}