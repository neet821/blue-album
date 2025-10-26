"""
同步观影房间的数据库操作
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from . import models, schemas
import random
import string
from datetime import datetime, timezone, timedelta

def to_beijing_time(dt: datetime) -> datetime:
    """将UTC时间转换为北京时间（东八区）"""
    if dt.tzinfo is None:
        # 如果时间没有时区信息，假设是UTC
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=8)))

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
    
    # 添加在线成员数量
    result = []
    for room in rooms:
        # 总成员数
        total_count = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id
        ).count()
        
        # 在线成员数
        online_count = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id,
            models.SyncRoomMember.is_online == True
        ).count()
        
        room_dict = room.__dict__.copy()
        room_dict['member_count'] = online_count  # 显示在线成员数
        room_dict['total_members'] = total_count
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
    """离开房间 - 设置为离线状态而非删除"""
    member = db.query(models.SyncRoomMember).filter(
        models.SyncRoomMember.room_id == room_id,
        models.SyncRoomMember.user_id == user_id
    ).first()
    
    if member:
        # 标记为离线，但保留成员记录
        member.is_online = False
        member.last_active_at = datetime.utcnow()
        db.commit()
        
        # 检查是否需要转移房间控制权
        room = get_room_by_id(db, room_id)
        if room and room.host_user_id == user_id and room.control_mode == "host_only":
            # 房主离开，转为全员控制模式
            room.control_mode = "all_members"
            room.updated_at = datetime.utcnow()
            db.commit()
        
        return True
    return False

def rejoin_room(db: Session, room_id: int, user_id: int) -> bool:
    """重新加入房间（设置为在线状态）"""
    member = db.query(models.SyncRoomMember).filter(
        models.SyncRoomMember.room_id == room_id,
        models.SyncRoomMember.user_id == user_id
    ).first()
    
    if member:
        member.is_online = True
        member.last_active_at = datetime.utcnow()
        db.commit()
        return True
    return False

def get_room_members(db: Session, room_id: int, online_only: bool = True):
    """获取房间成员列表"""
    query = db.query(models.SyncRoomMember).options(
        joinedload(models.SyncRoomMember.user)
    ).filter(
        models.SyncRoomMember.room_id == room_id
    )
    
    # 默认只返回在线成员
    if online_only:
        query = query.filter(models.SyncRoomMember.is_online == True)
    
    members = query.all()
    
    result = []
    for member in members:
        result.append({
            'id': member.id,
            'user_id': member.user_id,
            'username': member.user.username,
            'nickname': member.nickname or member.user.username,
            'is_verified': member.is_verified,
            'is_online': member.is_online,
            'last_active_at': member.last_active_at.isoformat() if member.last_active_at else None,
            'joined_at': member.joined_at.isoformat() if member.joined_at else None
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
            'created_at': to_beijing_time(msg.created_at).isoformat() if msg.created_at else None
        })
    
    return list(reversed(result))  # 返回正序

# 管理员功能
def get_all_rooms_admin(db: Session, skip: int = 0, limit: int = 100):
    """管理员获取所有房间列表（包含成员数量和在线人数）"""
    rooms = db.query(models.SyncRoom).filter(
        models.SyncRoom.is_active == True
    ).order_by(models.SyncRoom.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for room in rooms:
        # 总成员数
        total_members = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id
        ).count()
        
        # 在线成员数
        online_members = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id,
            models.SyncRoomMember.is_online == True
        ).count()
        
        # 获取房主信息
        host = db.query(models.User).filter(models.User.id == room.host_user_id).first()
        
        result.append({
            'id': room.id,
            'room_code': room.room_code,
            'room_name': room.room_name,
            'host_username': host.username if host else 'Unknown',
            'control_mode': room.control_mode,
            'mode': room.mode,
            'total_members': total_members,
            'online_members': online_members,
            'is_playing': room.is_playing,
            'created_at': to_beijing_time(room.created_at).isoformat() if room.created_at else None,
            'updated_at': room.updated_at.isoformat() if room.updated_at else None
        })
    
    return result

def delete_room_admin(db: Session, room_id: int) -> bool:
    """管理员删除房间"""
    room = get_room_by_id(db, room_id)
    if not room:
        return False
    
    # 删除房间（级联删除成员和消息）
    db.delete(room)
    db.commit()
    return True

# 自动清理功能
def cleanup_empty_rooms(db: Session, minutes: int = 10) -> int:
    """清理超过指定时间无人的房间
    
    Args:
        minutes: 无人房间超时时间（分钟）
        
    Returns:
        删除的房间数量
    """
    from datetime import timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    # 查找所有活跃房间
    rooms = db.query(models.SyncRoom).filter(
        models.SyncRoom.is_active == True
    ).all()
    
    deleted_count = 0
    
    for room in rooms:
        # 检查房间是否有在线成员
        online_members = db.query(models.SyncRoomMember).filter(
            models.SyncRoomMember.room_id == room.id,
            models.SyncRoomMember.is_online == True
        ).count()
        
        # 如果没有在线成员且更新时间超过阈值
        if online_members == 0 and room.updated_at < cutoff_time:
            db.delete(room)
            deleted_count += 1
    
    if deleted_count > 0:
        db.commit()
    
    return deleted_count
