"""
测试数据库连接是否会阻塞
"""
import time
import sys
sys.path.insert(0, 'D:\\Laragon\\laragon\\www\\blue-local')

print("=" * 60)
print("测试数据库连接")
print("=" * 60)

print("\n1. 导入database模块...")
start = time.time()
try:
    from backend.database import SessionLocal, engine
    print(f"   ✅ 导入成功 ({time.time()-start:.2f}秒)")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")
    exit(1)

print("\n2. 测试创建SessionLocal...")
start = time.time()
try:
    db = SessionLocal()
    print(f"   ✅ SessionLocal创建成功 ({time.time()-start:.2f}秒)")
except Exception as e:
    print(f"   ❌ SessionLocal创建失败: {e}")
    exit(1)

print("\n3. 测试数据库查询...")
start = time.time()
try:
    # 尝试一个简单的查询
    result = db.execute("SELECT 1").fetchone()
    print(f"   ✅ 查询成功: {result} ({time.time()-start:.2f}秒)")
except Exception as e:
    print(f"   ❌ 查询失败: {e}")
finally:
    db.close()

print("\n4. 测试models导入...")
start = time.time()
try:
    from backend import models
    print(f"   ✅ models导入成功 ({time.time()-start:.2f}秒)")
except Exception as e:
    print(f"   ❌ models导入失败: {e}")

print("\n5. 测试sync_room_crud导入...")
start = time.time()
try:
    from backend import sync_room_crud
    print(f"   ✅ sync_room_crud导入成功 ({time.time()-start:.2f}秒)")
except Exception as e:
    print(f"   ❌ sync_room_crud导入失败: {e}")

print("\n" + "=" * 60)
print("✅ 所有测试完成!")
print("=" * 60)
