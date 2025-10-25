<template>
  <div class="sync-room-page">
    <div class="container">
      <div class="page-header">
        <h1>🎬 同步观影</h1>
        <p class="subtitle">和朋友一起在线观看视频，实时同步进度</p>
      </div>

      <!-- 创建/加入房间区域 -->
      <div class="action-cards">
        <div class="action-card" @click="showCreateDialog = true">
          <div class="icon">➕</div>
          <h3>创建房间</h3>
          <p>创建一个新的观影房间，邀请朋友加入</p>
        </div>

        <div class="action-card" @click="showJoinDialog = true">
          <div class="icon">🔑</div>
          <h3>加入房间</h3>
          <p>输入房间代码，加入朋友的观影房间</p>
        </div>
      </div>

      <!-- 我的房间列表 -->
      <div class="my-rooms">
        <h2>我的房间</h2>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="rooms.length === 0" class="empty">
          <p>暂无房间，创建一个新房间开始吧！</p>
        </div>
        <div v-else class="room-list">
          <div 
            v-for="room in rooms" 
            :key="room.id" 
            class="room-card"
          >
            <div class="room-content" @click="enterRoom(room)">
              <div class="room-header">
                <h3>{{ room.room_name }}</h3>
                <span class="room-code">{{ room.room_code }}</span>
              </div>
              <div class="room-info">
                <span class="badge" :class="room.mode">{{ modeText(room.mode) }}</span>
                <span class="badge" :class="room.control_mode">{{ controlText(room.control_mode) }}</span>
                <span class="members">👥 {{ room.member_count }} 人</span>
              </div>
              <div class="room-footer">
                <span class="time">{{ formatTime(room.created_at) }}</span>
                <span v-if="room.host_user_id === userId" class="host-badge">房主</span>
              </div>
            </div>
            <!-- 删除按钮(仅房主可见) -->
            <div v-if="room.host_user_id === userId" class="room-actions">
              <el-button 
                type="danger" 
                size="small" 
                text
                @click.stop="deleteRoom(room)"
                :icon="Delete"
              >
                删除
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建房间对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建观影房间" width="500px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="房间名称">
          <el-input 
            v-model="createForm.room_name" 
            placeholder="给房间起个名字"
            maxlength="50"
          />
        </el-form-item>

        <el-form-item label="播放模式">
          <el-radio-group v-model="createForm.mode">
            <el-radio label="link">外部链接</el-radio>
            <el-radio label="upload" disabled>上传视频(开发中)</el-radio>
            <el-radio label="local" disabled>本地视频(开发中)</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="视频链接" v-if="createForm.mode === 'link'">
          <el-input 
            v-model="createForm.video_source" 
            placeholder="输入视频URL(支持 .mp4, .webm 等)"
            type="textarea"
            :rows="2"
          />
        </el-form-item>

        <el-form-item label="控制模式">
          <el-radio-group v-model="createForm.control_mode">
            <el-radio label="host_only">仅房主控制</el-radio>
            <el-radio label="all_members">所有成员控制</el-radio>
          </el-radio-group>
          <div class="form-tip">
            <p v-if="createForm.control_mode === 'host_only'">
              ✅ 只有房主可以控制播放、暂停和跳转，适合教学场景
            </p>
            <p v-else>
              ⚠️ 所有成员都可以控制，适合朋友间观看但可能混乱
            </p>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createRoom" :loading="creating">
          创建房间
        </el-button>
      </template>
    </el-dialog>

    <!-- 加入房间对话框 -->
    <el-dialog v-model="showJoinDialog" title="加入观影房间" width="400px">
      <el-form :model="joinForm" label-width="100px">
        <el-form-item label="房间代码">
          <el-input 
            v-model="joinForm.room_code" 
            placeholder="输入6位房间代码"
            maxlength="6"
            style="text-transform: uppercase;"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showJoinDialog = false">取消</el-button>
        <el-button type="primary" @click="joinRoom" :loading="joining">
          加入房间
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete } from '@element-plus/icons-vue';
import request from '@/utils/request';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const userId = authStore.user?.id;

const loading = ref(false);
const rooms = ref([]);
const showCreateDialog = ref(false);
const showJoinDialog = ref(false);
const creating = ref(false);
const joining = ref(false);

const createForm = ref({
  room_name: '',
  mode: 'link',
  video_source: '',
  control_mode: 'host_only'
});

const joinForm = ref({
  room_code: ''
});

// 获取房间列表
const fetchRooms = async () => {
  loading.value = true;
  try {
    const response = await request.get('/sync-rooms');
    rooms.value = response.data;
  } catch (error) {
    ElMessage.error('获取房间列表失败');
  } finally {
    loading.value = false;
  }
};

// 创建房间
const createRoom = async () => {
  if (!createForm.value.room_name.trim()) {
    ElMessage.warning('请输入房间名称');
    return;
  }

  if (createForm.value.mode === 'link' && !createForm.value.video_source.trim()) {
    ElMessage.warning('请输入视频链接');
    return;
  }

  creating.value = true;
  try {
    const response = await request.post('/sync-rooms', createForm.value);
    ElMessage.success('房间创建成功！');
    showCreateDialog.value = false;
    
    // 跳转到房间页面
    router.push(`/tools/sync-room/${response.data.id}`);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '创建房间失败');
  } finally {
    creating.value = false;
  }
};

// 加入房间
const joinRoom = async () => {
  const roomCode = joinForm.value.room_code.trim().toUpperCase();
  
  if (!roomCode || roomCode.length !== 6) {
    ElMessage.warning('请输入正确的6位房间代码');
    return;
  }

  joining.value = true;
  try {
    // 先通过代码获取房间信息
    const roomResponse = await request.get(`/sync-rooms/code/${roomCode}`);
    const roomId = roomResponse.data.id;
    
    // 加入房间
    await request.post(`/sync-rooms/code/${roomCode}/join`);
    
    ElMessage.success('加入房间成功！');
    showJoinDialog.value = false;
    
    // 跳转到房间页面
    router.push(`/tools/sync-room/${roomId}`);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '加入房间失败');
  } finally {
    joining.value = false;
  }
};

// 进入房间
const enterRoom = (room) => {
  router.push(`/tools/sync-room/${room.id}`);
};

// 工具函数
const modeText = (mode) => {
  const modes = {
    link: '外部链接',
    upload: '上传视频',
    local: '本地视频'
  };
  return modes[mode] || mode;
};

const controlText = (control) => {
  const controls = {
    host_only: '房主控制',
    all_members: '全员控制'
  };
  return controls[control] || control;
};

const formatTime = (time) => {
  if (!time) return '未知时间';
  
  try {
    const date = new Date(time);
    
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '时间格式错误';
    }
    
    const now = new Date();
    const diff = now - date;
    
    // 如果时间在未来,显示完整时间
    if (diff < 0) {
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
    
    // 相对时间
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`;
    if (diff < 2592000000) return `${Math.floor(diff / 86400000)} 天前`;
    
    // 超过30天显示完整日期
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  } catch (error) {
    console.error('格式化时间错误:', error, time);
    return '时间错误';
  }
};

// 删除房间
const deleteRoom = async (room) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除房间"${room.room_name}"吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    );
    
    // 执行删除
    await request.delete(`/sync-rooms/${room.id}`);
    ElMessage.success('房间已删除');
    
    // 刷新列表
    await fetchRooms();
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消删除
      return;
    }
    console.error('删除房间失败:', error);
    ElMessage.error(error.response?.data?.detail || '删除房间失败');
  }
};

onMounted(() => {
  fetchRooms();
});
</script>

<style scoped>
.sync-room-page {
  min-height: 100vh;
  padding: 40px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 50px;
  color: white;
}

.page-header h1 {
  font-size: 48px;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 18px;
  opacity: 0.9;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.action-card {
  background: white;
  border-radius: var(--radius-xl);
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.action-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.action-card .icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.action-card h3 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.action-card p {
  color: #666;
  font-size: 14px;
}

.my-rooms {
  background: white;
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.my-rooms h2 {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: #999;
  font-size: 16px;
}

.room-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.room-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--radius-sm);
  padding: 25px;
  transition: all 0.3s ease;
  color: white;
  position: relative;
  display: flex;
  flex-direction: column;
}

.room-content {
  flex: 1;
  cursor: pointer;
}

.room-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
}

.room-actions {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.room-actions .el-button {
  color: #fff;
  border-color: rgba(255, 255, 255, 0.5);
}

.room-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #fff;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.room-header h3 {
  font-size: 20px;
  margin: 0;
  flex: 1;
}

.room-code {
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  border-radius: var(--radius-xs);
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 14px;
}

.room-info {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.badge {
  padding: 5px 12px;
  border-radius: var(--radius-xl);
  font-size: 12px;
  background: rgba(255, 255, 255, 0.2);
}

.members {
  font-size: 14px;
}

.room-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.time {
  font-size: 12px;
  opacity: 0.8;
}

.host-badge {
  background: rgba(255, 215, 0, 0.3);
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: bold;
}

.form-tip {
  margin-top: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: var(--radius-xs);
  font-size: 13px;
  color: #666;
}

.form-tip p {
  margin: 0;
}

/* 暗黑模式支持 */
@media (prefers-color-scheme: dark) {
  .my-rooms {
    background: #1a1a1a;
  }

  .my-rooms h2 {
    color: #e0e0e0;
  }

  .action-card {
    background: #2a2a2a;
  }

  .action-card h3 {
    color: #e0e0e0;
  }

  .action-card p {
    color: #999;
  }
}
</style>
