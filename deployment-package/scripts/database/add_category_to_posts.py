"""
为 posts 表添加 category 字段
"""
import pymysql

def add_category_column():
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
        
        # 检查 category 字段是否已存在
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'blue_local_db' 
            AND TABLE_NAME = 'posts' 
            AND COLUMN_NAME = 'category'
        """)
        
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✅ category 字段已存在，无需添加")
        else:
            # 添加 category 字段
            cursor.execute("""
                ALTER TABLE posts 
                ADD COLUMN category VARCHAR(50) DEFAULT '未分类' AFTER content
            """)
            connection.commit()
            print("✅ 成功添加 category 字段")
            
            # 更新现有文章的分类为"未分类"
            cursor.execute("""
                UPDATE posts 
                SET category = '未分类' 
                WHERE category IS NULL
            """)
            connection.commit()
            print("✅ 已更新现有文章的分类")
        
        cursor.close()
            
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
    finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    print("开始添加 category 字段...")
    add_category_column()
    print("完成!")
