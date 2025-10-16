"""更新数据库表结构 - 添加角色和状态字段"""
from backend.database import engine
from sqlalchemy import text

def update_database():
    print("开始更新数据库表结构...")
    
    with engine.connect() as conn:
        # 检查并添加 role 字段
        try:
            print("1. 检查 role 字段...")
            result = conn.execute(text("SHOW COLUMNS FROM users LIKE 'role'"))
            if result.fetchone() is None:
                print("   添加 role 字段...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL"
                ))
                conn.commit()
                print("✅ role 字段添加成功")
            else:
                print("⚠️  role 字段已存在,跳过")
        except Exception as e:
            print(f"❌ 添加 role 字段失败: {e}")
        
        # 检查并添加 is_active 字段
        try:
            print("2. 检查 is_active 字段...")
            result = conn.execute(text("SHOW COLUMNS FROM users LIKE 'is_active'"))
            if result.fetchone() is None:
                print("   添加 is_active 字段...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE NOT NULL"
                ))
                conn.commit()
                print("✅ is_active 字段添加成功")
            else:
                print("⚠️  is_active 字段已存在,跳过")
        except Exception as e:
            print(f"❌ 添加 is_active 字段失败: {e}")
        
        # 检查并添加 updated_at 字段
        try:
            print("3. 检查 updated_at 字段...")
            result = conn.execute(text("SHOW COLUMNS FROM users LIKE 'updated_at'"))
            if result.fetchone() is None:
                print("   添加 updated_at 字段...")
                conn.execute(text(
                    "ALTER TABLE users ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
                ))
                conn.commit()
                print("✅ updated_at 字段添加成功")
            else:
                print("⚠️  updated_at 字段已存在,跳过")
        except Exception as e:
            print(f"❌ 添加 updated_at 字段失败: {e}")
        
        # 检查当前表结构
        print("\n4. 检查当前表结构...")
        result = conn.execute(text("DESCRIBE users"))
        columns = result.fetchall()
        
        print("\n当前 users 表结构:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # 将第一个注册的用户设置为管理员
        print("\n5. 设置管理员账号...")
        result = conn.execute(text("SELECT id, username FROM users ORDER BY id LIMIT 1"))
        first_user = result.fetchone()
        
        if first_user:
            conn.execute(text(
                f"UPDATE users SET role = 'admin' WHERE id = {first_user[0]}"
            ))
            conn.commit()
            print(f"✅ 用户 '{first_user[1]}' 已设置为管理员")
        else:
            print("⚠️  暂无用户,注册后第一个用户将自动成为管理员")
    
    print("\n✅ 数据库表结构更新完成!")

if __name__ == "__main__":
    update_database()
