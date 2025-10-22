"""
独立验证Socket.IO挂载
"""
import sys
sys.path.insert(0, 'D:\\Laragon\\laragon\\www\\blue-local')

print("开始测试...")

# 导入主应用
from backend.main import app
from backend.websocket_server import socket_app

print(f"✅ app类型: {type(app)}")
print(f"✅ socket_app类型: {type(socket_app)}")

# 检查routes
print("\n已注册的路由:")
for route in app.routes:
    print(f"  - {route.path} ({type(route).__name__})")

print("\n查找/ws挂载...")
ws_found = False
for route in app.routes:
    if hasattr(route, 'path') and '/ws' in route.path:
        print(f"  ✅ 找到: {route.path}")
        ws_found = True
        
if not ws_found:
    print("  ❌ 未找到/ws挂载!")

print("\n完成!")
