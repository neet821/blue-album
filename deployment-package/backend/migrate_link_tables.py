"""
数据库迁移脚本 - 创建 link_categories 和 website_links 表
运行此脚本以添加网站收藏管理功能所需的数据库表
"""
import sys
import os

# 添加父目录到路径以允许导入 backend 包
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_path)

from backend.database import engine
from backend.models import Base, LinkCategory, WebsiteLink

def create_link_tables():
    """创建链接管理相关的表"""
    print("正在创建 link_categories 和 website_links 表...")
    
    try:
        # 只创建新表,不会影响现有表
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("✅ 表创建成功!")
        print("- link_categories (链接分类表)")
        print("- website_links (网站链接表)")
    except Exception as e:
        print(f"❌ 创建表时出错: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("网站收藏管理功能 - 数据库迁移")
    print("=" * 50)
    
    success = create_link_tables()
    
    if success:
        print("\n✅ 迁移完成!现在可以使用网站收藏管理功能了。")
    else:
        print("\n❌ 迁移失败,请检查错误信息。")
