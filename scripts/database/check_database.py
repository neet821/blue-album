import sys
sys.path.insert(0, '.')

print("正在检查数据库...")

# 1. 测试数据库连接
print("\n1. 测试 MySQL 连接...")
try:
    import pymysql
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4'
    )
    print("✓ MySQL 连接成功")
    
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE 'blue_local_db'")
    result = cursor.fetchone()
    
    if result:
        print("✓ 数据库 blue_local_db 已存在")
    else:
        print("✗ 数据库 blue_local_db 不存在,正在创建...")
        cursor.execute("CREATE DATABASE blue_local_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        print("✓ 数据库创建成功")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ MySQL 连接失败: {e}")
    sys.exit(1)

# 2. 测试 SQLAlchemy 连接
print("\n2. 测试 SQLAlchemy 连接...")
try:
    from backend.database import engine, SessionLocal
    from backend.models import Base, User, Post
    
    # 测试连接
    with engine.connect() as connection:
        print("✓ SQLAlchemy 引擎连接成功")
    
    # 创建表
    print("\n3. 创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建/更新成功")
    
    # 检查表是否存在
    print("\n4. 检查表结构...")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"✓ 找到的表: {tables}")
    
    if 'users' in tables:
        columns = inspector.get_columns('users')
        print("\n用户表列:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
    
    if 'posts' in tables:
        columns = inspector.get_columns('posts')
        print("\n文章表列:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
    
    print("\n✓ 数据库检查完成!")
    
except Exception as e:
    print(f"✗ 数据库操作失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n数据库已准备就绪,可以开始注册用户了!")
