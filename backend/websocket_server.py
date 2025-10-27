"""
WebSocket 服务器 - 处理实时同步和聊天
使用 python-socketio + FastAPI
"""
import socketio
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Dict, Set
import logging
from datetime import datetime

from . import sync_room_crud, models
from .database import SessionLocal

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 Socket.IO 服务器
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # 开发环境允许所有来源
    logger=True,
    engineio_logger=True
)

# 存储房间和用户的连接映射
# room_connections: {room_id: {user_id: sid, ...}}
room_connections: Dict[int, Dict[int, str]] = {}

def get_db():
    """获取数据库会话 - 注意:调用者负责关闭连接"""
    return SessionLocal()

@sio.event
async def connect(sid, environ):
    """客户端连接事件"""
    logger.info(f"Client connected: {sid}")
    await sio.emit('connected', {'status': 'success'}, room=sid)

@sio.event
async def disconnect(sid):
    """客户端断开连接事件"""
    logger.info(f"Client disconnected: {sid}")
    
    # 从所有房间中移除该连接
    for room_id, connections in list(room_connections.items()):
        for user_id, connection_sid in list(connections.items()):
            if connection_sid == sid:
                del connections[user_id]
                
                # 通知房间其他成员
                await sio.emit('member_left', {
                    'user_id': user_id,
                    'room_id': room_id
                }, room=f'room_{room_id}', skip_sid=sid)
                
                # 如果房间空了,清理房间
                if not connections:
                    del room_connections[room_id]
                
                break

@sio.event
async def join_room(sid, data):
    """加入房间"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        username = data.get('username', 'Anonymous')
        stealth = data.get('stealth', False)  # 检查是否为隐身模式
        
        if not room_id or not user_id:
            await sio.emit('error', {'message': '缺少必要参数'}, room=sid)
            return
        
        db = get_db()
        
        # 验证房间存在
        room = sync_room_crud.get_room_by_id(db, room_id)
        if not room:
            await sio.emit('error', {'message': '房间不存在'}, room=sid)
            return
        
        # 验证用户是房间成员（隐身模式管理员除外）
        from .crud import get_user_by_id
        user = get_user_by_id(db, user_id)
        is_admin_stealth = stealth and user and user.role == 'admin'
        
        if not is_admin_stealth and not sync_room_crud.is_room_member(db, room_id, user_id):
            await sio.emit('error', {'message': '您不是该房间成员'}, room=sid)
            return
        
        # 加入 Socket.IO 房间
        await sio.enter_room(sid, f'room_{room_id}')
        
        # 记录连接（隐身模式管理员不记录为正式成员）
        if not is_admin_stealth:
            if room_id not in room_connections:
                room_connections[room_id] = {}
            room_connections[room_id][user_id] = sid
        
        # 获取房间成员列表
        members = sync_room_crud.get_room_members(db, room_id)
        
        # 通知该用户加入成功
        await sio.emit('join_success', {
            'room_id': room_id,
            'room': {
                'id': room.id,
                'room_code': room.room_code,
                'room_name': room.room_name,
                'host_user_id': room.host_user_id,
                'control_mode': room.control_mode,
                'mode': room.mode,
                'video_source': room.video_source,
                'current_time': room.current_time,
                'is_playing': room.is_playing
            },
            'members': members
        }, room=sid)
        
        # 如果不是隐身模式，通知房间其他成员有新成员加入
        if not stealth:
            await sio.emit('member_joined', {
                'user_id': user_id,
                'username': username,
                'room_id': room_id
            }, room=f'room_{room_id}', skip_sid=sid)
        
        logger.info(f"User {user_id} joined room {room_id}" + (" (stealth)" if stealth else ""))
        
    except Exception as e:
        logger.error(f"Error in join_room: {str(e)}")
        await sio.emit('error', {'message': f'加入房间失败: {str(e)}'}, room=sid)
    finally:
        if db:
            db.close()

@sio.event
async def leave_room_event(sid, data):
    """离开房间"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        
        if not room_id or not user_id:
            return
        
        db = get_db()
        
        # 调用数据库函数更新成员状态
        sync_room_crud.leave_room(db, room_id, user_id)
        
        # 离开 Socket.IO 房间
        await sio.leave_room(sid, f'room_{room_id}')
        
        # 移除连接记录
        was_connected = room_id in room_connections and user_id in room_connections[room_id]
        if was_connected:
            del room_connections[room_id][user_id]
            
            if not room_connections[room_id]:
                del room_connections[room_id]
        
        # 如果是正式成员，通知其他成员（隐身模式管理员不通知）
        if was_connected:
            await sio.emit('member_left', {
                'user_id': user_id,
                'room_id': room_id
            }, room=f'room_{room_id}')
        
        logger.info(f"User {user_id} left room {room_id}")
        
    except Exception as e:
        logger.error(f"Error in leave_room_event: {str(e)}")
    finally:
        if db:
            db.close()

@sio.event
async def playback_control(sid, data):
    """播放控制事件"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        action = data.get('action')  # play, pause, seek, rate
        time = data.get('time')
        rate = data.get('rate', 1.0)
        
        if not room_id or not user_id or not action:
            await sio.emit('error', {'message': '缺少必要参数'}, room=sid)
            return
        
        db = get_db()
        room = sync_room_crud.get_room_by_id(db, room_id)
        
        if not room:
            await sio.emit('error', {'message': '房间不存在'}, room=sid)
            return
        
        # 检查控制权限
        if room.control_mode == 'host_only' and user_id != room.host_user_id:
            await sio.emit('error', {'message': '只有房主可以控制播放'}, room=sid)
            return
        
        # 更新房间状态 - 修复：直接更新room对象而不是调用update_room
        if action == 'play':
            room.is_playing = True
        elif action == 'pause':
            room.is_playing = False
        elif action == 'seek' and time is not None:
            room.current_time = time
        
        # 提交更改
        room.updated_at = datetime.utcnow()
        db.commit()
        
        # 广播给房间所有成员(包括发送者,确保同步)
        # 修复：seek时也要携带当前的播放状态，确保成员视频状态一致
        await sio.emit('playback_sync', {
            'action': action,
            'time': time,
            'rate': rate,
            'is_playing': room.is_playing,  # 添加播放状态
            'user_id': user_id
        }, room=f'room_{room_id}')
        
        logger.info(f"Playback control in room {room_id}: {action} by user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in playback_control: {str(e)}")
        await sio.emit('error', {'message': f'控制失败: {str(e)}'}, room=sid)
    finally:
        if db:
            db.close()

@sio.event
async def send_message(sid, data):
    """发送聊天消息"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        username = data.get('username', 'Anonymous')
        message = data.get('message', '').strip()
        
        if not room_id or not user_id or not message:
            await sio.emit('error', {'message': '消息不能为空'}, room=sid)
            return
        
        if len(message) > 500:
            await sio.emit('error', {'message': '消息过长'}, room=sid)
            return
        
        db = get_db()
        
        # 验证房间成员
        if not sync_room_crud.is_room_member(db, room_id, user_id):
            await sio.emit('error', {'message': '您不是该房间成员'}, room=sid)
            return
        
        # 保存消息到数据库
        db_message = sync_room_crud.create_message(db, room_id, user_id, message)
        
        # 广播消息给房间所有成员(包括发送者)
        await sio.emit('new_message', {
            'id': db_message.id,
            'room_id': room_id,
            'user_id': user_id,
            'username': username,
            'message': message,
            'created_at': db_message.created_at.isoformat()
        }, room=f'room_{room_id}')
        
        logger.info(f"Message sent in room {room_id} by user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        await sio.emit('error', {'message': f'发送消息失败: {str(e)}'}, room=sid)
    finally:
        if db:
            db.close()

@sio.event
async def time_update(sid, data):
    """时间更新(房主定期发送当前播放时间)"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        time = data.get('time')
        
        if not room_id or not user_id or time is None:
            return
        
        db = get_db()
        room = sync_room_crud.get_room_by_id(db, room_id)
        
        if not room:
            return
        
        # 只有房主或有权限的用户才能发送时间更新
        if room.control_mode == 'host_only' and user_id != room.host_user_id:
            return
        
        # 广播时间同步(不保存到数据库,避免频繁写入)
        await sio.emit('time_sync', {
            'time': time,
            'user_id': user_id
        }, room=f'room_{room_id}', skip_sid=sid)
        
    except Exception as e:
        logger.error(f"Error in time_update: {str(e)}")
    finally:
        if db:
            db.close()

@sio.event
async def request_sync(sid, data):
    """处理成员请求同步事件"""
    db = None
    try:
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        
        if not room_id or not user_id:
            await sio.emit('error', {'message': '缺少必要参数'}, room=sid)
            return
        
        db = get_db()
        
        # 验证房间存在
        room = sync_room_crud.get_room_by_id(db, room_id)
        if not room:
            await sio.emit('error', {'message': '房间不存在'}, room=sid)
            return
        
        # 验证用户是房间成员
        if not sync_room_crud.is_room_member(db, room_id, user_id):
            await sio.emit('error', {'message': '您不是该房间成员'}, room=sid)
            return
        
        # 发送当前播放状态给请求者
        await sio.emit('playback_sync', {
            'action': 'sync',
            'time': room.current_time,
            'is_playing': room.is_playing,
            'user_id': room.host_user_id  # 标记为房主状态同步
        }, room=sid)
        
        logger.info(f"Sync requested for user {user_id} in room {room_id}")
        
    except Exception as e:
        logger.error(f"Error in request_sync: {str(e)}")
        await sio.emit('error', {'message': f'同步请求失败: {str(e)}'}, room=sid)
    finally:
        if db:
            db.close()

# 创建 ASGI 应用
# 关键修复：当mount到/ws时，socketio_path应该是'/'，这样完整路径才是 /ws/socket.io/
socket_app = socketio.ASGIApp(sio, socketio_path='/')
