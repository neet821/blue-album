<template>
  <div class="sync-room-player">
    <div class="room-container">
      <!-- 左侧：视频播放器 -->
      <div class="player-section">
        <div class="player-header">
          <div class="room-info">
            <h2>{{ roomInfo.room_name }}</h2>
            <span class="room-code">房间代码: {{ roomInfo.room_code }}</span>
            <!-- 隐身模式提示 -->
            <div v-if="isStealthMode" class="stealth-indicator">
              <el-tag type="warning" size="small">👁️ 管理员隐身模式</el-tag>
            </div>
          </div>
          <div class="room-controls">
            <el-button size="small" @click="copyRoomCode">📋 复制代码</el-button>
            <el-button size="small" type="danger" @click="leaveRoom">🚪 离开房间</el-button>
          </div>
        </div>

        <!-- 本地视频文件选择器 -->
        <div v-if="roomInfo.mode === 'local'" class="local-video-selector">
          <div class="file-selector">
            <input
              type="file"
              ref="localFileInput"
              accept="video/mp4,video/webm,video/avi,video/quicktime,video/x-ms-wmv,video/x-flv,video/x-matroska,video/mp2t,video/3gpp,video/mpeg,.mkv,.avi,.mov,.wmv,.flv,.m4v,.3gp,.mpg,.mpeg,.ts,.mts,.m2ts,.vob"
              @change="onLocalFileSelected"
              style="display: none"
            />

            <!-- 文件选择区域 -->
            <div
              class="file-drop-zone"
              @click="$refs.localFileInput.click()"
              :class="{ 'has-file': localVideoUrl !== null }"
            >
              <div class="file-drop-content">
                <div class="file-icon">
                  <i class="el-icon-video-play" v-if="!localVideoUrl"></i>
                  <i class="el-icon-check" v-else></i>
                </div>
                <div class="file-text">
                  <p v-if="!localVideoUrl" class="file-title">点击选择本地视频文件</p>
                  <p v-else class="file-title">✅ 已选择视频文件</p>
                  <p class="file-subtitle">
                    支持格式：MP4, WebM, AVI, MOV, MKV, WMV, FLV, 3GP, MPEG 等
                    <span v-if="localVideoUrl" class="file-status">(已加载)</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="local-mode-tip">
            <el-alert
              type="info"
              :closable="false"
              show-icon
            >
              💡 本地视频同步模式：请选择与房主相同的视频文件，所有成员的播放进度将保持同步
            </el-alert>
          </div>
        </div>

        <!-- 视频播放器 -->
        <div class="video-container">
          <video
            ref="videoPlayer"
            class="video-player"
            controls
            :src="currentVideoSrc"
            @play="onPlay"
            @pause="onPause"
            @seeking="onSeeking"
            @timeupdate="onTimeUpdate"
          >
            您的浏览器不支持视频播放
          </video>
        </div>

        <!-- 播放控制提示 -->
        <div class="control-info">
          <el-alert
            v-if="roomInfo.control_mode === 'host_only' && !isHost"
            type="info"
            :closable="false"
            show-icon
          >
            当前为房主控制模式，只有房主可以控制播放
          </el-alert>
          <el-alert
            v-else-if="roomInfo.control_mode === 'all_members'"
            type="success"
            :closable="false"
            show-icon
          >
            当前为全员控制模式，所有成员都可以控制播放
          </el-alert>
        </div>

        <!-- 成员列表 -->
        <div class="members-panel">
          <h3>👥 房间成员 ({{ members.length }})</h3>
          <div class="member-list">
            <div
              v-for="member in members"
              :key="member.user_id"
              class="member-item"
            >
              <span class="member-name">
                {{ member.nickname || member.username }}
                <span v-if="member.user_id === roomInfo.host_user_id" class="host-badge">👑</span>
              </span>
              <span class="member-status">{{ member.user_id === currentUserId ? '(你)' : '' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：聊天区域 -->
      <div class="chat-section">
        <div class="chat-header">
          <h3>💬 聊天室</h3>
        </div>

        <div class="chat-messages" ref="chatContainer">
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="message"
            :class="{ 'own-message': msg.user_id === currentUserId }"
          >
            <div class="message-header">
              <span class="message-author">{{ msg.username }}</span>
              <span class="message-time">{{ formatMessageTime(msg.created_at) }}</span>
            </div>
            <div class="message-content">{{ msg.message }}</div>
          </div>
        </div>

        <div class="chat-input">
          <el-input
            v-model="newMessage"
            placeholder="输入消息..."
            @keyup.enter="sendMessage"
            maxlength="500"
          >
            <template #append>
              <el-button @click="sendMessage" :disabled="!newMessage.trim()">
                发送
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { io } from 'socket.io-client';
import request from '../utils/request';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const roomId = ref(parseInt(route.params.id));
const currentUserId = computed(() => authStore.user?.id);
const currentUsername = computed(() => authStore.user?.username);

// 检查是否为管理员隐身模式
const isStealthMode = ref(sessionStorage.getItem('adminStealthMode') === 'true');
const stealthRoomId = ref(sessionStorage.getItem('stealthRoomId'));

const videoPlayer = ref(null);
const chatContainer = ref(null);
const localFileInput = ref(null);
const socket = ref(null);

// 本地视频相关
const localVideoUrl = ref(null);

const roomInfo = ref({
  id: 0,
  room_code: '',
  room_name: '',
  host_user_id: 0,
  control_mode: 'host_only',
  mode: 'link',
  video_source: '',
  current_time: 0,
  is_playing: false
});

const members = ref([]);
const messages = ref([]);
const newMessage = ref('');

const isHost = computed(() => currentUserId.value === roomInfo.value.host_user_id);
const canControl = computed(() => {
  return isHost.value || roomInfo.value.control_mode === 'all_members';
});

// 当前视频源（根据模式动态选择）
const currentVideoSrc = computed(() => {
  if (roomInfo.value.mode === 'local') {
    return localVideoUrl.value;
  }
  return roomInfo.value.video_source;
});

// 防止重复触发事件
let isUpdating = false;
let timeUpdateTimer = null;

// 获取房间信息
const fetchRoomInfo = async () => {
  try {
    // 隐身模式的管理员使用管理员API
    const apiEndpoint = isStealthMode.value ? `/admin/sync-rooms/${roomId.value}` : `/sync-rooms/${roomId.value}`;
    const response = await request.get(apiEndpoint);
    roomInfo.value = response.data;
    
    // 如果是隐身模式，从房间详情中提取成员信息
    if (isStealthMode.value && response.data.members) {
      members.value = response.data.members;
    }
    
    // 设置视频源（仅link模式）
    if (videoPlayer.value && roomInfo.value.mode === 'link' && roomInfo.value.video_source) {
      videoPlayer.value.src = roomInfo.value.video_source;
    }
  } catch (error) {
    ElMessage.error('获取房间信息失败');
    router.push('/tools/sync-room');
  }
};

// 获取成员列表
const fetchMembers = async () => {
  try {
    if (isStealthMode.value) {
      // 隐身模式下，成员信息已经从房间详情中获取
      // 这里不需要额外调用
      return;
    } else {
      const response = await request.get(`/sync-rooms/${roomId.value}/members`);
      members.value = response.data;
    }
  } catch (error) {
    console.error('获取成员列表失败', error);
  }
};

// 获取聊天记录
const fetchMessages = async () => {
  try {
    // 隐身模式的管理员使用管理员API
    const apiEndpoint = isStealthMode.value ? `/admin/sync-rooms/${roomId.value}/messages` : `/sync-rooms/${roomId.value}/messages`;
    const response = await request.get(apiEndpoint);
    messages.value = response.data;
    scrollToBottom();
  } catch (error) {
    console.error('获取聊天记录失败', error);
  }
};

// 本地视频文件选择处理
const onLocalFileSelected = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 验证文件类型
  if (!file.type.startsWith('video/')) {
    ElMessage.warning('请选择有效的视频文件');
    return;
  }

  // 创建本地URL
  const url = URL.createObjectURL(file);
  localVideoUrl.value = url;

  ElMessage.success(`已选择视频文件：${file.name}`);

  // 如果视频播放器已准备好，设置源
  nextTick(() => {
    if (videoPlayer.value) {
      videoPlayer.value.src = url;
      // 如果房间正在播放，同步状态
      if (roomInfo.value.is_playing) {
        videoPlayer.value.currentTime = roomInfo.value.current_time;
        videoPlayer.value.play().catch(console.error);
      }
    }
  });
};

// 初始化 WebSocket
const initWebSocket = () => {
  // 连接到 WebSocket 服务器
  // ✅ 不指定URL,自动使用当前页面的域名(localhost:5173)
  // Vite会通过代理将/ws路径转发到后端8000端口
  socket.value = io({
    path: '/ws/socket.io',
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5
  });

  socket.value.on('connect', () => {
    console.log('WebSocket 连接成功', socket.value.id);
    
    // 加入房间
    socket.value.emit('join_room', {
      room_id: roomId.value,
      user_id: currentUserId.value,
      username: currentUsername.value,
      stealth: isStealthMode.value  // 添加隐身模式参数
    });
  });

  socket.value.on('disconnect', () => {
    console.log('WebSocket 断开连接');
  });

  socket.value.on('error', (data) => {
    ElMessage.error(data.message || '发生错误');
  });

  // 加入成功
  socket.value.on('join_success', (data) => {
    console.log('加入房间成功', data);
    roomInfo.value = data.room;
    members.value = data.members;
    
    // 同步视频状态
    if (videoPlayer.value) {
      videoPlayer.value.currentTime = data.room.current_time;
      if (data.room.is_playing) {
        videoPlayer.value.play();
      }
    }
  });

  // 新成员加入
  socket.value.on('member_joined', async (data) => {
    console.log('新成员加入:', data);
    ElMessage.info(`${data.username} 加入了房间`);
    // 立即刷新成员列表
    await fetchMembers();
  });

  // 成员离开
  socket.value.on('member_left', async (data) => {
    console.log('成员离开:', data);
    
    // 检查是否有控制模式变化
    if (data.control_mode_changed) {
      ElMessage.warning(data.message || '房主已离开，房间已转为全员控制模式');
      // 更新房间信息
      if (roomInfo.value) {
        roomInfo.value.control_mode = data.new_control_mode;
      }
    }
    
    // 立即刷新成员列表（只显示在线成员）
    await fetchMembers();
  });

  // 播放控制同步
  socket.value.on('playback_sync', (data) => {
    console.log('收到播放同步:', data);
    
    // 修复：如果是自己发送的控制指令，则忽略（避免房主自己受影响）
    if (data.user_id === currentUserId.value) {
      console.log('忽略自己发送的控制指令');
      return;
    }
    
    isUpdating = true;
    
    if (data.action === 'play') {
      videoPlayer.value?.play();
    } else if (data.action === 'pause') {
      videoPlayer.value?.pause();
    } else if (data.action === 'seek' && data.time !== undefined) {
      if (videoPlayer.value) {
        videoPlayer.value.currentTime = data.time;
        // 修复：seek后根据房间播放状态决定是否自动播放
        // 解决"房主拖动进度条后成员视频暂停但跳到新位置"的问题
        if (data.is_playing && videoPlayer.value.paused) {
          videoPlayer.value.play();
        } else if (!data.is_playing && !videoPlayer.value.paused) {
          videoPlayer.value.pause();
        }
      }
    } else if (data.action === 'sync' && data.time !== undefined) {
      // 处理同步请求：设置到指定时间和播放状态
      if (videoPlayer.value) {
        videoPlayer.value.currentTime = data.time;
        if (data.is_playing && videoPlayer.value.paused) {
          videoPlayer.value.play();
        } else if (!data.is_playing && !videoPlayer.value.paused) {
          videoPlayer.value.pause();
        }
      }
    }
    
    setTimeout(() => {
      isUpdating = false;
    }, 500);
  });

  // 时间同步 - 优化：快速同步策略，确保延迟<1秒
  socket.value.on('time_sync', (data) => {
    if (!canControl.value && videoPlayer.value) {
      const diff = Math.abs(videoPlayer.value.currentTime - data.time);
      
      // 优化同步策略：
      // 大偏差（>2秒）：立即强制同步
      // 中等偏差（0.5-2秒）：平滑调整播放速率
      // 小偏差（<0.5秒）：忽略，避免卡顿
      
      if (diff > 2) {
        // 大偏差：立即跳转
        isUpdating = true;
        videoPlayer.value.currentTime = data.time;
        videoPlayer.value.playbackRate = 1.0; // 恢复正常速度
        setTimeout(() => {
          isUpdating = false;
        }, 300);
      } else if (diff > 0.5) {
        // 中等偏差：通过调整播放速率平滑追赶
        if (videoPlayer.value.currentTime < data.time) {
          // 落后：加速播放
          videoPlayer.value.playbackRate = 1.1;
        } else {
          // 超前：减速播放
          videoPlayer.value.playbackRate = 0.9;
        }
        
        // 1秒后恢复正常速度
        setTimeout(() => {
          if (videoPlayer.value) {
            videoPlayer.value.playbackRate = 1.0;
          }
        }, 1000);
      }
      // 小偏差：忽略
    }
  });

  // 新消息
  socket.value.on('new_message', (data) => {
    console.log('收到新消息:', data);
    // 检查消息是否已存在(避免重复)
    const exists = messages.value.some(msg => 
      msg.id === data.id || 
      (msg.user_id === data.user_id && 
       msg.message === data.message && 
       Math.abs(new Date(msg.created_at) - new Date(data.created_at)) < 2000)
    );
    
    if (!exists) {
      messages.value.push(data);
      scrollToBottom();
    }
  });
};

// 视频播放事件
let isControllingPlayback = false;

const onPlay = () => {
  if (isUpdating || isControllingPlayback) return;
  
  if (!canControl.value) {
    // 没有控制权限时，立即同步房主的播放状态
    console.log('成员尝试播放，同步房主状态');
    socket.value?.emit('request_sync', {
      room_id: roomId.value,
      user_id: currentUserId.value
    });
    
    isControllingPlayback = true;
    videoPlayer.value?.pause();
    setTimeout(() => { isControllingPlayback = false; }, 100);
    
    const now = Date.now();
    if (now - lastWarningTime > 2000) {
      ElMessage.warning('只有房主可以控制播放');
      lastWarningTime = now;
    }
    return;
  }
  
  console.log('发送播放控制: play');
  socket.value?.emit('playback_control', {
    room_id: roomId.value,
    user_id: currentUserId.value,
    action: 'play'
  });
};

const onPause = () => {
  if (isUpdating || isControllingPlayback) return;
  
  if (!canControl.value) {
    // 没有控制权限时，立即同步房主的播放状态
    console.log('成员尝试暂停，同步房主状态');
    socket.value?.emit('request_sync', {
      room_id: roomId.value,
      user_id: currentUserId.value
    });
    
    const now = Date.now();
    if (now - lastWarningTime > 2000) {
      ElMessage.warning('只有房主可以控制播放');
      lastWarningTime = now;
    }
    return;
  }
  
  console.log('发送播放控制: pause');
  socket.value?.emit('playback_control', {
    room_id: roomId.value,
    user_id: currentUserId.value,
    action: 'pause'
  });
};

// 添加节流控制避免无限循环
let lastWarningTime = 0;
let isRestoringTime = false;

const onSeeking = () => {
  if (isUpdating || isRestoringTime) return;
  
  if (!canControl.value) {
    // 节流：2秒内只显示一次警告
    const now = Date.now();
    if (now - lastWarningTime > 2000) {
      ElMessage.warning('只有房主可以控制进度');
      lastWarningTime = now;
    }
    
    // 恢复到房间进度,设置标志避免循环
    if (videoPlayer.value && roomInfo.value) {
      isRestoringTime = true;
      videoPlayer.value.currentTime = roomInfo.value.current_time || 0;
      setTimeout(() => { isRestoringTime = false; }, 100);
    }
    return;
  }
  
  const time = Math.floor(videoPlayer.value?.currentTime || 0);
  console.log('发送进度跳转:', time);
  socket.value?.emit('playback_control', {
    room_id: roomId.value,
    user_id: currentUserId.value,
    action: 'seek',
    time: time
  });
};

const onTimeUpdate = () => {
  // 只有房主需要定期同步时间，成员不需要频繁发送
  if (!canControl.value) return;
  
  // 优化：房主每0.8秒发送一次时间更新，确保延迟在1秒以内
  if (timeUpdateTimer) return;
  
  timeUpdateTimer = setTimeout(() => {
    const time = videoPlayer.value?.currentTime || 0;
    socket.value?.emit('time_update', {
      room_id: roomId.value,
      user_id: currentUserId.value,
      time: time
    });
    timeUpdateTimer = null;
  }, 800); // 优化为800ms，保证延迟<1秒
};

// 发送消息
const sendMessage = () => {
  const message = newMessage.value.trim();
  if (!message) return;
  
  console.log('发送聊天消息:', message);
  
  socket.value?.emit('send_message', {
    room_id: roomId.value,
    user_id: currentUserId.value,
    username: currentUsername.value,
    message: message
  });
  
  newMessage.value = '';
};

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

// 复制房间代码
const copyRoomCode = () => {
  navigator.clipboard.writeText(roomInfo.value.room_code);
  ElMessage.success('房间代码已复制');
};

// 离开房间
const leaveRoom = async () => {
  try {
    await ElMessageBox.confirm('确定要离开房间吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    socket.value?.emit('leave_room_event', {
      room_id: roomId.value,
      user_id: currentUserId.value
    });
    
    socket.value?.disconnect();
    router.push('/tools/sync-room');
  } catch {
    // 取消离开
  }
};

// 格式化时间
const formatMessageTime = (time) => {
  const date = new Date(time);
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(async () => {
  await fetchRoomInfo();
  await fetchMembers();
  await fetchMessages();
  initWebSocket();
});

onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.emit('leave_room_event', {
      room_id: roomId.value,
      user_id: currentUserId.value
    });
    socket.value.disconnect();
  }
  
  if (timeUpdateTimer) {
    clearTimeout(timeUpdateTimer);
  }
  
  // 清理隐身模式状态
  if (isStealthMode.value) {
    sessionStorage.removeItem('adminStealthMode');
    sessionStorage.removeItem('stealthRoomId');
  }
});
</script>

<style scoped>
.sync-room-player {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

.room-container {
  max-width: 1600px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
}

/* 左侧播放器区域 */
.player-section {
  background: white;
  border-radius: var(--radius-sm);
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.room-info h2 {
  margin: 0 0 5px 0;
  font-size: 24px;
  color: #333;
}

.room-code {
  color: #666;
  font-size: 14px;
}

.stealth-indicator {
  margin-top: 8px;
}

.video-container {
  background: #000;
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin-bottom: 20px;
}

.video-player {
  width: 100%;
  height: auto;
  max-height: 70vh;
  display: block;
}

.control-info {
  margin-bottom: 20px;
}

.members-panel {
  background: #f9f9f9;
  border-radius: var(--radius-sm);
  padding: 15px;
}

.members-panel h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
}

.member-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.member-item {
  background: white;
  padding: 8px 15px;
  border-radius: var(--radius-xl);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.host-badge {
  font-size: 12px;
}

.member-status {
  color: #999;
  font-size: 12px;
}

/* 右侧聊天区域 */
.chat-section {
  background: white;
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 40px);
}

.chat-header {
  padding: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 15px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.message-author {
  font-weight: bold;
  font-size: 13px;
  color: #333;
}

.message-time {
  font-size: 11px;
  color: #999;
}

.message-content {
  background: #f0f0f0;
  padding: 10px 15px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: #333;
  word-wrap: break-word;
}

.own-message .message-content {
  background: #667eea;
  color: white;
}

.chat-input {
  padding: 20px;
  border-top: 2px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .room-container {
    grid-template-columns: 1fr;
  }

  .chat-section {
    height: 500px;
  }
}

/* 暗黑模式 */
@media (prefers-color-scheme: dark) {
  .sync-room-player {
    background: #1a1a1a;
  }

  .player-section,
  .chat-section {
    background: #2a2a2a;
  }

  .room-info h2,
  .chat-header h3 {
    color: #e0e0e0;
  }

  .room-code,
  .member-status {
    color: #999;
  }

  .members-panel {
    background: #1a1a1a;
  }

  .member-item {
    background: #333;
    color: #e0e0e0;
  }

  .message-author {
    color: #e0e0e0;
  }

  .message-content {
    background: #333;
    color: #e0e0e0;
  }

  .own-message .message-content {
    background: #667eea;
    color: white;
  }

  /* 本地视频模式样式 */
  .local-video-selector {
    margin-bottom: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .file-selector {
    margin-bottom: 15px;
  }

  .file-drop-zone {
    border: 2px dashed rgba(102, 126, 234, 0.5);
    border-radius: 8px;
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(102, 126, 234, 0.05);
  }

  .file-drop-zone:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }

  .file-drop-zone.has-file {
    border-color: #67c23a;
    background: rgba(103, 194, 58, 0.1);
  }

  .file-drop-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  .file-icon {
    font-size: 48px;
    color: #667eea;
  }

  .file-drop-zone.has-file .file-icon {
    color: #67c23a;
  }

  .file-text {
    color: #e0e0e0;
  }

  .file-title {
    font-size: 18px;
    font-weight: 500;
    margin: 0 0 5px 0;
  }

  .file-subtitle {
    font-size: 14px;
    margin: 0;
    opacity: 0.8;
  }

  .file-status {
    color: #67c23a;
    font-weight: 500;
  }

  .local-mode-tip {
    margin-top: 10px;
  }

  .local-mode-tip .el-alert {
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    color: #e0e0e0;
  }

  .local-mode-tip .el-alert__icon {
    color: #667eea;
  }
}
</style>
