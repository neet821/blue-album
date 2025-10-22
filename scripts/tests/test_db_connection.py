"""测试数据库连接"""
import sys
import traceback

try:
    print("1. 测试导入模块...")
    from backend import database, models
    print("✅ 模块导入成功")
    
    print("\n2. 测试数据库连接...")
    from sqlalchemy import text
    with database.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(f"✅ 数据库连接成功: {result.fetchone()}")
    
    print("\n3. 检查数据库表...")
    from sqlalchemy import inspect
    inspector = inspect(database.engine)
    tables = inspector.get_table_names()
    print(f"当前表: {tables}")
    
    if not tables:
        print("\n⚠️  没有找到表,正在创建...")
        models.Base.metadata.create_all(bind=database.engine)
        tables = inspector.get_table_names()
        print(f"✅ 表创建成功: {tables}")
    
    print("\n✅ 所有测试通过!")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n详细错误信息:")
    traceback.print_exc()
    sys.exit(1)
