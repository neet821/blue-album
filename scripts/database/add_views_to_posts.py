"""
为 posts 表添加 views (浏览次数) 字段
"""
import pymysql

def add_views_column():
    try:
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            database='blue_local_db',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 检查 views 字段是否已存在
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'blue_local_db' 
            AND TABLE_NAME = 'posts' 
            AND COLUMN_NAME = 'views'
        """)
        
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✅ views 字段已存在，无需添加")
        else:
            # 添加 views 字段
            cursor.execute("""
                ALTER TABLE posts 
                ADD COLUMN views INT DEFAULT 0 AFTER category
            """)
            connection.commit()
            print("✅ 成功添加 views 字段")
            
            # 初始化现有文章的浏览次数为0
            cursor.execute("""
                UPDATE posts 
                SET views = 0 
                WHERE views IS NULL
            """)
            connection.commit()
            print("✅ 已初始化现有文章的浏览次数")
        
        cursor.close()
            
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
    finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    print("开始添加 views 字段...")
    add_views_column()
    print("完成!")
