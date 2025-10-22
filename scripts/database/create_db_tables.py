#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建数据库表的脚本
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

print("="*50)
print("开始创建数据库表...")
print("="*50)

try:
    from backend.database import engine
    from backend.models import Base
    
    print("\n正在连接数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("✓ 数据库表创建成功!")
    
    # 验证表是否创建
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n当前数据库中的表: {tables}")
    
    if 'users' in tables and 'posts' in tables:
        print("\n✓✓✓ 所有必需的表都已创建!")
        print("现在可以尝试注册用户了!")
    else:
        print("\n⚠ 警告: 某些表可能未创建成功")
        
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
