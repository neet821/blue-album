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

# --- 文章 API ---

@app.get("/api/posts", response_model=list[schemas.PostWithAuthor])
def read_posts(
    skip: int = 0, 
    limit: int = 100, 
    author_id: int = None,
    search: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    """获取文章列表，支持分页、按作者筛选、搜索和分类过滤"""
    posts = crud.get_posts(db, skip=skip, limit=limit, author_id=author_id, 
                          search=search, category=category)
    return posts

@app.get("/api/posts/{post_id}", response_model=schemas.PostWithAuthor)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """获取单篇文章详情并增加浏览次数"""
    post = crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 增加浏览次数
    crud.increment_post_views(db, post_id)
    
    # 重新获取更新后的文章（包含新的浏览次数）
    post = crud.get_post_by_id(db, post_id)
    return post

@app.post("/api/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建文章（仅管理员）"""
    # 权限检查：仅管理员可以创建文章
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create posts")
    
    return crud.create_post(db, post, author_id=current_user.id)

@app.put("/api/posts/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新文章（仅作者或管理员）"""
    db_post = crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 权限检查：仅作者或管理员可以编辑
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
    updated_post = crud.update_post(db, post_id, post_update)
    return updated_post

@app.delete("/api/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文章（仅作者或管理员）"""
    db_post = crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 权限检查：仅作者或管理员可以删除
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    crud.delete_post(db, post_id)
    return {"message": "Post deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}

# --- Link Categories API ---

@app.get("/api/categories")
def get_categories(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有分类"""
    return crud.get_categories_by_user(db, user_id=current_user.id)

@app.post("/api/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.LinkCategoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建分类"""
    return crud.create_category(db, category, user_id=current_user.id)

@app.put("/api/categories/{category_id}")
def update_category(
    category_id: int,
    category_update: schemas.LinkCategoryUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新分类"""
    db_category = crud.update_category(db, category_id, category_update, user_id=current_user.id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/api/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除分类"""
    success = crud.delete_category(db, category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# --- Website Links API ---

@app.get("/api/links")
def get_links(
    category_id: int = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的链接,可选按分类筛选"""
    return crud.get_links_by_user(db, user_id=current_user.id, category_id=category_id)

@app.post("/api/links", status_code=status.HTTP_201_CREATED)
def create_link(
    link: schemas.WebsiteLinkCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建链接"""
    # 验证分类是否属于当前用户
    category = crud.get_category_by_id(db, link.category_id, user_id=current_user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.create_link(db, link, user_id=current_user.id)

@app.put("/api/links/{link_id}")
def update_link(
    link_id: int,
    link_update: schemas.WebsiteLinkUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新链接"""
    # 如果要修改分类,验证分类是否属于当前用户
    if link_update.category_id:
        category = crud.get_category_by_id(db, link_update.category_id, user_id=current_user.id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    db_link = crud.update_link(db, link_id, link_update, user_id=current_user.id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    return db_link

@app.delete("/api/links/{link_id}")
def delete_link(
    link_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除链接"""
    success = crud.delete_link(db, link_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Link deleted successfully"}
