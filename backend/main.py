from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import crud, models, schemas, security
from .database import SessionLocal, engine
from .websocket_server import socket_app  # 导入 WebSocket 应用

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS 中间件 ---
# 从配置中获取CORS origins
from .config import config

# 开发环境:允许所有来源
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:8000",
]

# 添加配置中的CORS origins
if hasattr(config, 'CORS_ORIGINS'):
    origins.extend(config.CORS_ORIGINS)

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


# ==================== 同步观影 API ====================
from . import sync_room_crud
from typing import List

@app.post("/api/sync-rooms", response_model=schemas.SyncRoomInfo)
def create_sync_room(
    room: schemas.SyncRoomCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建同步观影房间"""
    db_room = sync_room_crud.create_room(db, room, current_user.id)
    
    # 获取成员数量
    member_count = len(sync_room_crud.get_room_members(db, db_room.id))
    
    room_dict = db_room.__dict__.copy()
    room_dict['member_count'] = member_count
    
    return room_dict

@app.get("/api/sync-rooms/code/{room_code}", response_model=schemas.SyncRoomInfo)
def get_room_by_code(
    room_code: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """通过房间代码获取房间信息"""
    room = sync_room_crud.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 获取成员数量
    member_count = len(sync_room_crud.get_room_members(db, room.id))
    
    room_dict = room.__dict__.copy()
    room_dict['member_count'] = member_count
    
    return room_dict

@app.get("/api/sync-rooms/{room_id}", response_model=schemas.SyncRoomInfo)
def get_room(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取房间详细信息"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 验证用户是房间成员
    if not sync_room_crud.is_room_member(db, room_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a room member")
    
    # 获取成员数量
    member_count = len(sync_room_crud.get_room_members(db, room.id))
    
    room_dict = room.__dict__.copy()
    room_dict['member_count'] = member_count
    
    return room_dict

@app.get("/api/sync-rooms", response_model=List[schemas.SyncRoomInfo])
def get_user_rooms(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """获取用户参与的房间列表"""
    rooms = sync_room_crud.get_user_rooms(db, current_user.id, skip, limit)
    return rooms

@app.post("/api/sync-rooms/{room_id}/join")
def join_sync_room(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """加入房间"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    member = sync_room_crud.join_room(db, room_id, current_user.id)
    
    return {
        "message": "Joined room successfully",
        "room_id": room_id,
        "member_id": member.id
    }

@app.post("/api/sync-rooms/code/{room_code}/join")
def join_sync_room_by_code(
    room_code: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """通过房间代码加入房间"""
    room = sync_room_crud.get_room_by_code(db, room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    member = sync_room_crud.join_room(db, room.id, current_user.id)
    
    return {
        "message": "Joined room successfully",
        "room_id": room.id,
        "room_code": room.room_code,
        "member_id": member.id
    }

@app.post("/api/sync-rooms/{room_id}/leave")
def leave_sync_room(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """离开房间"""
    success = sync_room_crud.leave_room(db, room_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Not in this room")
    
    return {"message": "Left room successfully"}

@app.delete("/api/sync-rooms/{room_id}")
def close_sync_room(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """关闭房间(仅房主，且房间必须为空)"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")
    
    if room.host_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以关闭房间")
    
    success, message = sync_room_crud.close_room(db, room_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"message": message}

@app.get("/api/sync-rooms/{room_id}/members", response_model=List[schemas.SyncRoomMemberInfo])
def get_room_members(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取房间成员列表"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 验证用户是房间成员
    if not sync_room_crud.is_room_member(db, room_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a room member")
    
    # 默认只返回在线成员
    members = sync_room_crud.get_room_members(db, room_id, online_only=True)
    return members

@app.get("/api/sync-rooms/{room_id}/messages", response_model=List[schemas.SyncRoomMessage])
def get_room_messages(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """获取房间聊天记录"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 验证用户是房间成员
    if not sync_room_crud.is_room_member(db, room_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a room member")
    
    messages = sync_room_crud.get_room_messages(db, room_id, skip, limit)
    return messages

@app.put("/api/sync-rooms/{room_id}", response_model=schemas.SyncRoomInfo)
def update_sync_room(
    room_id: int,
    room_update: schemas.SyncRoomUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新房间信息(仅房主)"""
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.host_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only host can update the room")
    
    updated_room = sync_room_crud.update_room(db, room_id, room_update)
    
    # 获取在线成员数量
    member_count = len(sync_room_crud.get_room_members(db, updated_room.id, online_only=True))
    
    room_dict = updated_room.__dict__.copy()
    room_dict['member_count'] = member_count
    
    return room_dict


# =====================================================
# 管理员同步观影管理接口
# =====================================================
@app.get("/api/admin/sync-rooms")
def admin_get_all_rooms(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """管理员获取所有房间列表"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    rooms = sync_room_crud.get_all_rooms_admin(db, skip, limit)
    return {"rooms": rooms, "total": len(rooms)}

@app.get("/api/admin/sync-rooms/{room_id}")
def admin_get_room_detail(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员获取房间详情"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 获取房间成员（包括离线成员）
    members = sync_room_crud.get_room_members(db, room_id, online_only=False)
    
    # 获取房主信息
    host = db.query(models.User).filter(models.User.id == room.host_user_id).first()
    
    return {
        "id": room.id,
        "room_code": room.room_code,
        "room_name": room.room_name,
        "host_user_id": room.host_user_id,
        "host_username": host.username if host else "Unknown",
        "control_mode": room.control_mode,
        "mode": room.mode,
        "video_source": room.video_source,
        "current_time": room.current_time,
        "is_playing": room.is_playing,
        "is_active": room.is_active,
        "created_at": room.created_at.isoformat() if room.created_at else None,
        "updated_at": room.updated_at.isoformat() if room.updated_at else None,
        "members": members
    }

@app.put("/api/admin/sync-rooms/{room_id}")
def admin_update_room(
    room_id: int,
    room_update: schemas.SyncRoomUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员编辑房间（不限制房主）"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    room = sync_room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    updated_room = sync_room_crud.update_room(db, room_id, room_update)
    
    return {
        "message": "Room updated successfully",
        "room": {
            "id": updated_room.id,
            "room_code": updated_room.room_code,
            "room_name": updated_room.room_name,
            "control_mode": updated_room.control_mode
        }
    }

@app.delete("/api/admin/sync-rooms/{room_id}")
def admin_delete_room(
    room_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员删除房间"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = sync_room_crud.delete_room_admin(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {"message": "Room deleted successfully"}

@app.post("/api/admin/sync-rooms/cleanup")
def admin_cleanup_empty_rooms(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    minutes: int = 10
):
    """管理员手动清理空房间"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    deleted_count = sync_room_crud.cleanup_empty_rooms(db, minutes)
    return {"message": f"Cleaned up {deleted_count} empty rooms"}


# =====================================================
# 挂载 WebSocket 服务（必须在所有路由之后）
# =====================================================
app.mount("/ws", socket_app)

# =====================================================
# 启动后台任务
# =====================================================
import asyncio
from . import background_tasks

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    # 启动空房间清理任务
    asyncio.create_task(background_tasks.cleanup_task(interval_minutes=5, empty_timeout_minutes=10))
    print("✅ 同步观影空房间清理任务已启动")
