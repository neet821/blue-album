from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    title: str
    content: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    """用户信息更新"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserPasswordUpdate(BaseModel):
    """密码修改"""
    old_password: str
    new_password: str

class User(UserBase):
    id: int
    role: str = "user"
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    posts: List[Post] = []

    class Config:
        from_attributes = True

class UserSimple(UserBase):
    """简化的用户信息(用于列表显示)"""
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None