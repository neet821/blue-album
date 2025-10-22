"""
完全独立的Socket.IO测试服务器
不依赖任何backend模块
"""
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

print("=" * 60)
print("🚀 独立Socket.IO服务器")
print("=" * 60)

# 创建Socket.IO服务器
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)

# 创建ASGI应用 - 关键：socketio_path应该是相对于mount点的路径
# 当mount到/ws时，socketio_path应该是'/'或留空，让请求直接到达/ws/
socket_app = socketio.ASGIApp(sio, socketio_path='/')
print("✅ Socket.IO服务器创建成功 (socketio_path='/')")

# 创建FastAPI应用
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载Socket.IO
app.mount("/ws", socket_app)
print("✅ Socket.IO已挂载到 /ws")

# 事件处理
@sio.event
async def connect(sid, environ):
    print(f"🔗 客户端连接: {sid}")
    await sio.emit('connected', {'status': 'success'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"❌ 客户端断开: {sid}")

@sio.event
async def join_room(sid, data):
    room_id = data.get('room_id')
    print(f"📥 {sid} 加入房间 {room_id}")
    sio.enter_room(sid, f"room_{room_id}")
    await sio.emit('room_joined', {'room_id': room_id}, room=sid)

@app.get("/")
def root():
    return {"status": "ok", "message": "独立Socket.IO测试服务器"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 服务器地址:")
    print("   HTTP: http://127.0.0.1:8005")
    print("   WebSocket: ws://127.0.0.1:8005/ws/socket.io/")
    print("=" * 60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8005, log_level="info")
