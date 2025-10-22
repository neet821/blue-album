"""
同步观影房间的数据库操作
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from . import models, schemas
import random
import string
from datetime import datetime

def generate_room_code() -> str:
    """生成6位随机房间代码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_room(db: Session, room: schemas.SyncRoomCreate, user_id: int) -> models.SyncRoom:
    """创建新房间"""
    # 生成唯一房间代码
    while True:
        room_code = generate_room_code()
        if not db.query(models.SyncRoom).filter(models.SyncRoom.room_code == room_code).first():
            break
    
    db_room = models.SyncRoom(
        room_code=room_code,
        room_name=room.room_name,
        host_user_id=user_id,
        control_mode=room.control_mode,
        mode=room.mode,
        video_source=room.video_source,
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    # 房主自动加入房间
    join_room(db, db_room.id, user_id)
    
    return db_room

def get_room_by_code(db: Session, room_code: str) -> models.SyncRoom:
    """通过房间代码获取房间"""
    return db.query(models.SyncRoom).filter(
        models.SyncRoom.room_code == room_code,
        models.SyncRoom.is_active == True
    ).first()

def get_room_by_id(db: Session, room_id: int) -> models.SyncRoom:
    """通过ID获取房间"""
    return db.query(models.SyncRoom).filter(
        models.SyncRoom.id == room_id,
        models.SyncRoom.is_active == True
    ).first()

def get_user_rooms(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    """获取用户参与的房间列表"""
    rooms = db.query(models.SyncRoom).join(
        models.SyncRoomMember
    ).filter(
        models.SyncRoomMember.user_id == user_id,
        models.SyncRoom.is_active == True
    ).order_by(models.SyncRoom.created_at.desc()).offset(skip).limit(limit).all()
    
    # 添加成员数量
    result = []
    for room in rooms:
        member_count = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id
        ).count()
        room_dict = room.__dict__
        room_dict['member_count'] = member_count
        result.append(room_dict)
    
    return result

def update_room(db: Session, room_id: int, room_update: schemas.SyncRoomUpdate) -> models.SyncRoom:
    """更新房间信息"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None
    
    update_data = room_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    
    db_room.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_room)
    return db_room

def close_room(db: Session, room_id: int) -> bool:
    """关闭房间"""
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return False
    
    db_room.is_active = False
    db.commit()
    return True

# 房间成员管理
def join_room(db: Session, room_id: int, user_id: int, nickname: str = None) -> models.SyncRoomMember:
    """加入房间"""
    # 检查是否已加入
    existing = db.query(models.SyncRoomMember).filter(
        models.SyncRoomMember.room_id == room_id,
        models.SyncRoomMember.user_id == user_id
    ).first()
    
    if existing:
        return existing
    
    member = models.SyncRoomMember(
        room_id=room_id,
        user_id=user_id,
        nickname=nickname
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def leave_room(db: Session, room_id: int, user_id: int) -> bool:
    """离开房间"""
    member = db.query(models.SyncRoomMember).filter(
        models.SyncRoomMember.room_id == room_id,
        models.SyncRoomMember.user_id == user_id
    ).first()
    
    if member:
        db.delete(member)
        db.commit()
        return True
    return False

def get_room_members(db: Session, room_id: int):
    """获取房间成员列表"""
    members = db.query(models.SyncRoomMember).options(
        joinedload(models.SyncRoomMember.user)
    ).filter(
        models.SyncRoomMember.room_id == room_id
    ).all()
    
    result = []
    for member in members:
        result.append({
            'id': member.id,
            'user_id': member.user_id,
            'username': member.user.username,
            'nickname': member.nickname or member.user.username,
            'is_verified': member.is_verified,
            'joined_at': member.joined_at.isoformat() if member.joined_at else None  # 修复: 转换datetime为ISO字符串
        })
    
    return result

def is_room_member(db: Session, room_id: int, user_id: int) -> bool:
    """检查用户是否是房间成员"""
    return db.query(models.SyncRoomMember).filter(
        models.SyncRoomMember.room_id == room_id,
        models.SyncRoomMember.user_id == user_id
    ).first() is not None

# 聊天消息管理
def create_message(db: Session, room_id: int, user_id: int, message: str) -> models.SyncRoomMessage:
    """创建聊天消息"""
    db_message = models.SyncRoomMessage(
        room_id=room_id,
        user_id=user_id,
        message=message
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_room_messages(db: Session, room_id: int, skip: int = 0, limit: int = 50):
    """获取房间聊天记录"""
    messages = db.query(models.SyncRoomMessage).options(
        joinedload(models.SyncRoomMessage.user)
    ).filter(
        models.SyncRoomMessage.room_id == room_id
    ).order_by(models.SyncRoomMessage.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for msg in messages:
        result.append({
            'id': msg.id,
            'room_id': msg.room_id,
            'user_id': msg.user_id,
            'username': msg.user.username,
            'message': msg.message,
            'created_at': msg.created_at.isoformat() if msg.created_at else None  # 修复: 转换datetime为ISO字符串
        })
    
    return list(reversed(result))  # 返回正序
