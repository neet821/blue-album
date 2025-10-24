"""
初始化数据库 - 创建所有表
"""
from backend.database import engine
from backend import models

def init_db():
    print("开始创建数据库表...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功!")
    print("创建的表:")
    print("  - users (用户表)")
    print("  - posts (文章表)")

if __name__ == "__main__":
    init_db()
