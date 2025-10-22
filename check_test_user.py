"""检查test用户状态"""
import sys
sys.path.append('d:/Laragon/laragon/www/blue-local')

from backend.database import SessionLocal
from backend import models

db = SessionLocal()

try:
    # 查找test用户
    test_user = db.query(models.User).filter(models.User.username == 'test').first()
    
    if test_user:
        print("=" * 60)
        print("找到test用户:")
        print("=" * 60)
        print(f"ID: {test_user.id}")
        print(f"用户名: {test_user.username}")
        print(f"邮箱: {test_user.email}")
        print(f"是否管理员: {test_user.is_admin}")
        print(f"哈希密码: {test_user.hashed_password[:50]}...")
        print(f"创建时间: {test_user.created_at}")
        
        # 检查是否有关联数据
        posts_count = db.query(models.Post).filter(models.Post.author_id == test_user.id).count()
        categories_count = db.query(models.Category).filter(models.Category.user_id == test_user.id).count()
        links_count = db.query(models.Link).filter(models.Link.user_id == test_user.id).count()
        
        print(f"\n关联数据:")
        print(f"  文章数: {posts_count}")
        print(f"  分类数: {categories_count}")
        print(f"  链接数: {links_count}")
        
        # 检查同步房间相关
        if hasattr(models, 'SyncRoom'):
            rooms_count = db.query(models.SyncRoom).filter(models.SyncRoom.host_user_id == test_user.id).count()
            print(f"  同步房间数: {rooms_count}")
        
        print("=" * 60)
    else:
        print("❌ 未找到test用户")
        
        # 列出所有用户
        all_users = db.query(models.User).all()
        print(f"\n数据库中共有 {len(all_users)} 个用户:")
        for u in all_users:
            print(f"  - {u.username} (ID: {u.id}, 管理员: {u.is_admin})")
    
finally:
    db.close()
