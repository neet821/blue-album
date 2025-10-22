"""测试独立Socket.IO服务器"""
import time
import socketio
import requests

print("=" * 60)
print("测试独立Socket.IO服务器 (端口8005)")
print("=" * 60)

# 测试1: HTTP端点
print("\n1️⃣ 测试HTTP端点...")
try:
    r = requests.get('http://127.0.0.1:8005/ws/socket.io/?EIO=4&transport=polling', timeout=5)
    print(f"   状态码: {r.status_code}")
    print(f"   响应: {r.text[:100]}")
    if r.status_code == 200:
        print("   ✅ HTTP端点工作正常")
    else:
        print(f"   ❌ HTTP端点返回错误状态码: {r.status_code}")
except Exception as e:
    print(f"   ❌ HTTP请求失败: {e}")

# 测试2: WebSocket连接
print("\n2️⃣ 测试WebSocket连接...")
try:
    sio = socketio.Client()
    
    @sio.event
    def connect():
        print("   ✅ WebSocket连接成功")
    
    @sio.event
    def disconnect():
        print("   断开连接")
    
    sio.connect('http://127.0.0.1:8005', socketio_path='/ws/socket.io', wait_timeout=5)
    time.sleep(1)
    sio.disconnect()
    print("   ✅ WebSocket测试完成")
except Exception as e:
    print(f"   ❌ WebSocket连接失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
