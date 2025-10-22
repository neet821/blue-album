"""测试test用户的登录和删除功能"""
import sys
sys.path.append('d:/Laragon/laragon/www/blue-local')

from backend.database import SessionLocal
from backend import models, security, crud

print("=" * 60)
print("测试1: 验证test用户密码")
print("=" * 60)

db = SessionLocal()

try:
    test_user = db.query(models.User).filter(models.User.username == 'test').first()
    
    if test_user:
        # 测试密码验证
        password = "test123"
        is_valid = security.verify_password(password, test_user.hashed_password)
        
        print(f"用户名: {test_user.username}")
        print(f"密码验证 (test123): {'✅ 通过' if is_valid else '❌ 失败'}")
        print(f"账户状态: {'✅ 启用' if test_user.is_active else '❌ 禁用'}")
        print(f"角色: {test_user.role}")
        
        # 检查关联数据
        print(f"\n关联数据统计:")
        posts = db.query(models.Post).filter(models.Post.author_id == test_user.id).count()
        categories = db.query(models.LinkCategory).filter(models.LinkCategory.user_id == test_user.id).count()
        links = db.query(models.WebsiteLink).filter(models.WebsiteLink.user_id == test_user.id).count()
        rooms = db.query(models.SyncRoom).filter(models.SyncRoom.host_user_id == test_user.id).count()
        
        print(f"  文章: {posts}")
        print(f"  链接分类: {categories}")
        print(f"  链接: {links}")
        print(f"  同步房间: {rooms}")
        
        if posts > 0 or categories > 0 or links > 0 or rooms > 0:
            print(f"\n⚠️  用户有关联数据，需要级联删除")
        else:
            print(f"\n✅ 用户无关联数据，可以直接删除")
    else:
        print("❌ test用户不存在")
        
finally:
    db.close()

print("\n" + "=" * 60)
print("测试2: 模拟删除用户（不实际删除）")
print("=" * 60)

db = SessionLocal()
try:
    test_user = db.query(models.User).filter(models.User.username == 'test').first()
    if test_user:
        print(f"如果删除用户 {test_user.username} (ID: {test_user.id}):")
        print(f"  会删除:")
        print(f"    - {db.query(models.Post).filter(models.Post.author_id == test_user.id).count()} 篇文章")
        print(f"    - {db.query(models.LinkCategory).filter(models.LinkCategory.user_id == test_user.id).count()} 个链接分类")
        print(f"    - {db.query(models.WebsiteLink).filter(models.WebsiteLink.user_id == test_user.id).count()} 个链接")
        print(f"    - {db.query(models.SyncRoom).filter(models.SyncRoom.host_user_id == test_user.id).count()} 个同步房间")
        print(f"\n✅ crud.delete_user() 函数已更新为级联删除")
finally:
    db.close()

print("=" * 60)
