from sqlalchemy.orm import Session, joinedload
from typing import Optional
from . import models, schemas, security

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    
    # 检查是否是第一个用户,如果是则设为管理员
    user_count = db.query(models.User).count()
    role = "admin" if user_count == 0 else "user"
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """获取所有用户(管理员功能)"""
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """更新用户信息(管理员功能)"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    # 如果要更新密码,需要加密
    if "password" in update_data:
        update_data["hashed_password"] = security.get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_id: int, old_password: str, new_password: str):
    """用户修改自己的密码"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # 验证旧密码
    if not security.verify_password(old_password, db_user.hashed_password):
        return False
    
    # 更新密码
    db_user.hashed_password = security.get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """删除用户(管理员功能) - 级联删除所有关联数据"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    try:
        # 1. 删除用户的文章
        db.query(models.Post).filter(models.Post.author_id == user_id).delete()
        
        # 2. 删除用户的链接
        db.query(models.WebsiteLink).filter(models.WebsiteLink.user_id == user_id).delete()
        
        # 3. 删除用户的链接分类（会级联删除该分类下的所有链接）
        db.query(models.LinkCategory).filter(models.LinkCategory.user_id == user_id).delete()
        
        # 4. 删除用户的同步房间消息
        user_rooms = db.query(models.SyncRoom).filter(models.SyncRoom.host_user_id == user_id).all()
        for room in user_rooms:
            db.query(models.SyncRoomMessage).filter(models.SyncRoomMessage.room_id == room.id).delete()
            db.query(models.SyncRoomMember).filter(models.SyncRoomMember.room_id == room.id).delete()
        
        # 5. 删除用户的同步房间
        db.query(models.SyncRoom).filter(models.SyncRoom.host_user_id == user_id).delete()
        
        # 6. 删除用户作为成员的房间关系
        db.query(models.SyncRoomMember).filter(models.SyncRoomMember.user_id == user_id).delete()
        
        # 7. 删除用户发送的房间消息
        db.query(models.SyncRoomMessage).filter(models.SyncRoomMessage.user_id == user_id).delete()
        
        # 8. 最后删除用户
        db.delete(db_user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"删除用户失败: {str(e)}")
        return False

# --- 文章 CRUD ---

def get_posts(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None, 
              search: Optional[str] = None, category: Optional[str] = None):
    """获取文章列表,支持按作者筛选、搜索和分类过滤,包含作者信息"""
    query = db.query(models.Post).options(joinedload(models.Post.author))
    
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Post.title.like(search_filter)) | 
            (models.Post.content.like(search_filter))
        )
    
    if category:
        query = query.filter(models.Post.category == category)
    
    return query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def get_post_by_id(db: Session, post_id: int):
    """根据 ID 获取文章,包含作者信息"""
    return db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == post_id).first()

def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    """创建文章"""
    db_post = models.Post(
        title=post.title,
        content=post.content,
        category=post.category if hasattr(post, 'category') else "未分类",
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    """更新文章"""
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    """删除文章"""
    db_post = get_post_by_id(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False

def increment_post_views(db: Session, post_id: int):
    """增加文章浏览次数"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db_post.views += 1
        db.commit()
        return True
    return False

# Link Category CRUD
def get_categories_by_user(db: Session, user_id: int):
    """获取用户的所有分类"""
    from sqlalchemy import func
    categories = db.query(
        models.LinkCategory,
        func.count(models.WebsiteLink.id).label('link_count')
    ).outerjoin(
        models.WebsiteLink
    ).filter(
        models.LinkCategory.user_id == user_id
    ).group_by(
        models.LinkCategory.id
    ).all()
    
    result = []
    for category, link_count in categories:
        category_dict = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "user_id": category.user_id,
            "created_at": category.created_at,
            "link_count": link_count
        }
        result.append(category_dict)
    return result

def get_category_by_id(db: Session, category_id: int, user_id: int):
    """获取特定分类"""
    return db.query(models.LinkCategory).filter(
        models.LinkCategory.id == category_id,
        models.LinkCategory.user_id == user_id
    ).first()

def create_category(db: Session, category: schemas.LinkCategoryCreate, user_id: int):
    """创建分类"""
    db_category = models.LinkCategory(
        name=category.name,
        description=category.description,
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.LinkCategoryUpdate, user_id: int):
    """更新分类"""
    db_category = get_category_by_id(db, category_id, user_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int):
    """删除分类(级联删除该分类下的所有链接)"""
    db_category = get_category_by_id(db, category_id, user_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# Website Link CRUD
def get_links_by_user(db: Session, user_id: int, category_id: Optional[int] = None):
    """获取用户的链接,可按分类筛选"""
    query = db.query(models.WebsiteLink).filter(models.WebsiteLink.user_id == user_id)
    if category_id:
        query = query.filter(models.WebsiteLink.category_id == category_id)
    return query.order_by(models.WebsiteLink.created_at.desc()).all()

def get_link_by_id(db: Session, link_id: int, user_id: int):
    """获取特定链接"""
    return db.query(models.WebsiteLink).filter(
        models.WebsiteLink.id == link_id,
        models.WebsiteLink.user_id == user_id
    ).first()

def create_link(db: Session, link: schemas.WebsiteLinkCreate, user_id: int):
    """创建链接"""
    db_link = models.WebsiteLink(
        title=link.title,
        url=link.url,
        description=link.description,
        category_id=link.category_id,
        user_id=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def update_link(db: Session, link_id: int, link_update: schemas.WebsiteLinkUpdate, user_id: int):
    """更新链接"""
    db_link = get_link_by_id(db, link_id, user_id)
    if not db_link:
        return None
    
    update_data = link_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_link, field, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link

def delete_link(db: Session, link_id: int, user_id: int):
    """删除链接"""
    db_link = get_link_by_id(db, link_id, user_id)
    if db_link:
        db.delete(db_link)
        db.commit()
        return True
    return False
