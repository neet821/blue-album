from sqlalchemy.orm import Session
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
    
    # 如果要更新密码,需要先哈希
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
    """删除用户(管理员功能)"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()