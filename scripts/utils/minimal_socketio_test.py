"""
最小化Socket.IO测试服务器
用于验证Socket.IO本身是否工作
"""
import socketio
from fastapi import FastAPI
import uvicorn

print("=" * 60)
print("🚀 启动最小化Socket.IO测试服务器")
print("=" * 60)

# 创建Socket.IO服务器
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)

# 创建ASGI应用
socket_app = socketio.ASGIApp(sio, socketio_path='socket.io')
print("✅ Socket.IO ASGI应用创建成功")

# 创建FastAPI应用
app = FastAPI()

# 挂载Socket.IO
app.mount("/ws", socket_app)
print("✅ Socket.IO已挂载到 /ws 路径")

@sio.event
async def connect(sid, environ):
    print(f"🔗 客户端连接: {sid}")
    await sio.emit('message', {'data': 'Connected!'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"❌ 客户端断开: {sid}")

@sio.event
async def test_message(sid, data):
    print(f"📨 收到测试消息: {data}")
    await sio.emit('test_response', {'status': 'success', 'data': data}, room=sid)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Minimal Socket.IO Test Server"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 服务器信息:")
    print("   - HTTP: http://127.0.0.1:8002")
    print("   - WebSocket: ws://127.0.0.1:8002/ws/socket.io/")
    print("=" * 60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="info")
