from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    category: Optional[str] = "未分类"  # 新增分类字段

class PostCreate(PostBase):
    """创建文章的请求模型"""
    pass

class PostUpdate(BaseModel):
    """更新文章的请求模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None  # 新增分类字段

class Post(PostBase):
    """文章响应模型"""
    id: int
    author_id: int
    views: int = 0  # 浏览次数
    created_at: datetime

    class Config:
        from_attributes = True

class PostWithAuthor(Post):
    """带作者信息的文章模型"""
    author: Optional['UserSimple'] = None

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

# Link Category Schemas
class LinkCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class LinkCategoryCreate(LinkCategoryBase):
    pass

class LinkCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LinkCategory(LinkCategoryBase):
    id: int
    user_id: int
    created_at: datetime
    link_count: Optional[int] = 0  # 该分类下的链接数量

    class Config:
        from_attributes = True

# Website Link Schemas
class WebsiteLinkBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    category_id: int

class WebsiteLinkCreate(WebsiteLinkBase):
    pass

class WebsiteLinkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class WebsiteLink(WebsiteLinkBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True