"""测试websocket_server导入"""
import sys
import time
sys.path.insert(0, 'D:\\Laragon\\laragon\\www\\blue-local')

print("=" * 60)
print("测试websocket_server导入")
print("=" * 60)

print("\n正在导入websocket_server...")
start = time.time()

try:
    from backend.websocket_server import socket_app, sio
    elapsed = time.time() - start
    print(f"✅ 导入成功! ({elapsed:.2f}秒)")
    print(f"   - socket_app类型: {type(socket_app)}")
    print(f"   - sio类型: {type(sio)}")
    print(f"   - sio.async_mode: {sio.async_mode}")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ 导入失败! ({elapsed:.2f}秒)")
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
