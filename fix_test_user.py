"""修复test用户 - 重置密码和启用账户"""
import sys
sys.path.append('d:/Laragon/laragon/www/blue-local')

from backend.database import SessionLocal
from backend import models, security

db = SessionLocal()

try:
    # 查找test用户
    test_user = db.query(models.User).filter(models.User.username == 'test').first()
    
    if test_user:
        print("=" * 60)
        print("找到test用户，开始修复...")
        print("=" * 60)
        
        # 1. 确保账户启用
        test_user.is_active = True
        
        # 2. 重置密码为 "test123"
        new_password = "test123"
        test_user.hashed_password = security.get_password_hash(new_password)
        
        db.commit()
        
        print("✅ 修复完成！")
        print(f"   用户名: {test_user.username}")
        print(f"   新密码: {new_password}")
        print(f"   账户状态: {'启用' if test_user.is_active else '禁用'}")
        print(f"   是否管理员: {'是' if test_user.role == 'admin' else '否'}")
        print("=" * 60)
    else:
        print("❌ 未找到test用户")
        print("\n创建test用户...")
        
        # 创建test用户
        from backend.schemas import UserCreate
        new_user = models.User(
            username="test",
            email="test@example.com",
            hashed_password=security.get_password_hash("test123"),
            role="user",
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ test用户创建成功！")
        print(f"   用户名: test")
        print(f"   密码: test123")
        print(f"   邮箱: test@example.com")
        print("=" * 60)
    
finally:
    db.close()
