"""
添加房间成员在线状态字段

为 sync_room_members 表添加:
- is_online: 是否在线
- last_active_at: 最后活跃时间
"""
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text, Column, Boolean, DateTime
from backend.database import SQLALCHEMY_DATABASE_URL

def add_online_status_columns():
    """添加在线状态相关字段"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 检查字段是否已存在
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'sync_room_members' 
                AND COLUMN_NAME IN ('is_online', 'last_active_at')
            """))
            existing_columns = [row[0] for row in result]
            
            # 添加 is_online 字段
            if 'is_online' not in existing_columns:
                print("添加 is_online 字段...")
                conn.execute(text("""
                    ALTER TABLE sync_room_members 
                    ADD COLUMN is_online BOOLEAN DEFAULT TRUE
                """))
                conn.commit()
                print("✅ is_online 字段添加成功")
            else:
                print("⏭️  is_online 字段已存在")
            
            # 添加 last_active_at 字段
            if 'last_active_at' not in existing_columns:
                print("添加 last_active_at 字段...")
                conn.execute(text("""
                    ALTER TABLE sync_room_members 
                    ADD COLUMN last_active_at DATETIME DEFAULT CURRENT_TIMESTAMP
                """))
                conn.commit()
                print("✅ last_active_at 字段添加成功")
            else:
                print("⏭️  last_active_at 字段已存在")
            
            # 更新现有记录
            print("更新现有记录...")
            conn.execute(text("""
                UPDATE sync_room_members 
                SET is_online = TRUE, 
                    last_active_at = joined_at 
                WHERE last_active_at IS NULL
            """))
            conn.commit()
            print("✅ 现有记录更新完成")
            
        print("\n🎉 数据库迁移完成!")
        
    except Exception as e:
        print(f"❌ 迁移失败: {str(e)}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("开始添加房间成员在线状态字段")
    print("=" * 60)
    add_online_status_columns()
