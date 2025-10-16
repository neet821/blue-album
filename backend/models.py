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