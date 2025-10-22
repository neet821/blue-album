"""
检查WebSocket模块导入
"""
import sys
sys.path.insert(0, 'D:\\Laragon\\laragon\\www\\blue-local')

try:
    print("尝试导入websocket_server...")
    from backend.websocket_server import socket_app, sio
    print(f"✅ 导入成功!")
    print(f"   socket_app 类型: {type(socket_app)}")
    print(f"   sio 类型: {type(sio)}")
    print(f"   sio async_mode: {sio.async_mode}")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
