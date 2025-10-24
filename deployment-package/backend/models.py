from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # 'admin' 或 'user'
    is_active = Column(Boolean, default=True, nullable=False)  # 账号是否启用
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, default="未分类")
    views = Column(Integer, default=0)  # 浏览次数
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")

class LinkCategory(Base):
    __tablename__ = "link_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    links = relationship("WebsiteLink", back_populates="category", cascade="all, delete-orphan")

class WebsiteLink(Base):
    __tablename__ = "website_links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(String(300), nullable=True)
    category_id = Column(Integer, ForeignKey("link_categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("LinkCategory", back_populates="links")
    user = relationship("User")

# 同步观影房间表
class SyncRoom(Base):
    __tablename__ = "sync_rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String(20), unique=True, index=True, nullable=False)  # 房间代码
    room_name = Column(String(100), nullable=False)
    host_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    control_mode = Column(String(20), default="host_only", nullable=False)  # host_only 或 all_members
    mode = Column(String(20), default="link", nullable=False)  # link=外链, upload=上传, local=本地
    video_source = Column(Text, nullable=True)  # 视频链接或文件路径
    video_hash = Column(String(64), nullable=True)  # 文件哈希值(模式二使用)
    current_time = Column(Integer, default=0)  # 当前播放时间(秒)
    is_playing = Column(Boolean, default=False)  # 播放状态
    is_active = Column(Boolean, default=True)  # 房间是否活跃
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    host = relationship("User")
    members = relationship("SyncRoomMember", back_populates="room", cascade="all, delete-orphan")
    messages = relationship("SyncRoomMessage", back_populates="room", cascade="all, delete-orphan")

# 房间成员表
class SyncRoomMember(Base):
    __tablename__ = "sync_room_members"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("sync_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nickname = Column(String(50), nullable=True)  # 房间内昵称
    is_verified = Column(Boolean, default=True)  # 是否通过哈希校验(模式二使用)
    is_online = Column(Boolean, default=True)  # 是否在线
    last_active_at = Column(DateTime, default=datetime.utcnow)  # 最后活跃时间
    joined_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("SyncRoom", back_populates="members")
    user = relationship("User")

# 房间聊天消息表
class SyncRoomMessage(Base):
    __tablename__ = "sync_room_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("sync_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("SyncRoom", back_populates="messages")
    user = relationship("User")