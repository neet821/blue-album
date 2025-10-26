<template>
  <div class="admin-rooms-container">
    <div class="header">
      <h2>同步观影房间管理</h2>
      <div class="actions">
        <el-button @click="refreshRooms" :icon="Refresh" :loading="loading">刷新</el-button>
        <el-button @click="cleanupEmptyRooms" type="warning" :icon="Delete">
          清理空房间
        </el-button>
      </div>
    </div>

    <div class="stats">
      <el-statistic title="活跃房间总数" :value="totalRooms" />
      <el-statistic title="在线用户总数" :value="totalOnlineUsers" />
      <el-statistic title="空房间数量" :value="emptyRoomsCount" />
    </div>

    <el-table :data="rooms" style="width: 100%" v-loading="loading" stripe>
      <el-table-column prop="room_code" label="房间代码" width="120" />
      <el-table-column prop="room_name" label="房间名称" width="180" />
      <el-table-column prop="host_username" label="房主" width="120" />
      
      <el-table-column label="控制模式" width="130">
        <template #default="{ row }">
          <el-tag :type="row.control_mode === 'host_only' ? 'primary' : 'success'">
            {{ row.control_mode === 'host_only' ? '房主控制' : '全员控制' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="成员" width="100">
        <template #default="{ row }">
          <span>{{ row.online_members }} / {{ row.total_members }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_playing ? 'success' : 'info'" size="small">
            {{ row.is_playing ? '播放中' : '暂停' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="mode" label="模式" width="100">
        <template #default="{ row }">
          {{ getModeText(row.mode) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="updated_at" label="最后活跃" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="enterRoom(row)">
            进入房间
          </el-button>
          <el-button link type="info" size="small" @click="viewRoom(row)">
            查看
          </el-button>
          <el-button link type="warning" size="small" @click="editRoom(row)">
            编辑
          </el-button>
          <el-popconfirm
            title="确定删除此房间吗？"
            @confirm="deleteRoom(row.id)"
            confirm-button-text="确定"
            cancel-button-text="取消"
          >
            <template #reference>
              <el-button link type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑房间对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑房间"
      width="500px"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="房间名称">
          <el-input v-model="editForm.room_name" />
        </el-form-item>
        <el-form-item label="控制模式">
          <el-radio-group v-model="editForm.control_mode">
            <el-radio value="host_only">房主控制</el-radio>
            <el-radio value="all_members">全员控制</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="房间状态">
          <el-switch
            v-model="editForm.is_active"
            active-text="活跃"
            inactive-text="关闭"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRoom">保存</el-button>
      </template>
    </el-dialog>

    <!-- 查看房间详情对话框 -->
    <el-dialog
      v-model="viewDialogVisible"
      title="房间详情"
      width="700px"
    >
      <el-descriptions :column="2" border v-if="currentRoom">
        <el-descriptions-item label="房间代码">
          {{ currentRoom.room_code }}
        </el-descriptions-item>
        <el-descriptions-item label="房间名称">
          {{ currentRoom.room_name }}
        </el-descriptions-item>
        <el-descriptions-item label="房主">
          {{ currentRoom.host_username }}
        </el-descriptions-item>
        <el-descriptions-item label="控制模式">
          <el-tag :type="currentRoom.control_mode === 'host_only' ? 'primary' : 'success'">
            {{ currentRoom.control_mode === 'host_only' ? '房主控制' : '全员控制' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="视频模式">
          {{ getModeText(currentRoom.mode) }}
        </el-descriptions-item>
        <el-descriptions-item label="播放状态">
          <el-tag :type="currentRoom.is_playing ? 'success' : 'info'">
            {{ currentRoom.is_playing ? '播放中' : '暂停' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">
          {{ formatDate(currentRoom.created_at) }}
        </el-descriptions-item>
      </el-descriptions>
      
      <h3 style="margin-top: 20px;">房间成员 ({{ currentRoom?.members?.length || 0 }})</h3>
      <el-table :data="currentRoom?.members || []" style="width: 100%">
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="nickname" label="昵称" width="150" />
        <el-table-column label="在线状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_online ? 'success' : 'info'" size="small">
              {{ row.is_online ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="joined_at" label="加入时间">
          <template #default="{ row }">
            {{ formatDate(row.joined_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 根据端口生成唯一的存储key，避免多实例串账户
const getStorageKey = (key) => {
  const port = window.location.port || '80';
  return `${key}_${port}`;
};

const router = useRouter()
import { ElMessage } from 'element-plus'
import { Refresh, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const rooms = ref([])
const loading = ref(false)
const editDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const currentRoom = ref(null)
const editForm = ref({
  room_name: '',
  control_mode: 'host_only',
  is_active: true
})
const editingRoomId = ref(null)

const totalRooms = computed(() => rooms.value.length)
const totalOnlineUsers = computed(() => 
  rooms.value.reduce((sum, room) => sum + room.online_members, 0)
)
const emptyRoomsCount = computed(() => 
  rooms.value.filter(room => room.online_members === 0).length
)

const getModeText = (mode) => {
  const modeMap = {
    'link': '外链',
    'upload': '上传',
    'local': '本地'
  }
  return modeMap[mode] || mode
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const refreshRooms = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem(getStorageKey('token'))
    const response = await axios.get('/api/admin/sync-rooms', {
      headers: { Authorization: `Bearer ${token}` }
    })
    rooms.value = response.data.rooms
    ElMessage.success('刷新成功')
  } catch (error) {
    console.error('获取房间列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取房间列表失败')
  } finally {
    loading.value = false
  }
}

const deleteRoom = async (roomId) => {
  try {
    const token = localStorage.getItem(getStorageKey('token'))
    await axios.delete(`/api/admin/sync-rooms/${roomId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    ElMessage.success('房间删除成功')
    await refreshRooms()
  } catch (error) {
    console.error('删除房间失败:', error)
    ElMessage.error(error.response?.data?.detail || '删除房间失败')
  }
}

const viewRoom = async (room) => {
  try {
    const token = localStorage.getItem(getStorageKey('token'))
    const response = await axios.get(`/api/admin/sync-rooms/${room.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    currentRoom.value = response.data
    viewDialogVisible.value = true
  } catch (error) {
    console.error('获取房间详情失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取房间详情失败')
  }
}

const enterRoom = (room) => {
  // 管理员直接进入房间页面
  router.push(`/tools/sync-room/${room.id}`)
}

const editRoom = (room) => {
  editingRoomId.value = room.id
  editForm.value = {
    room_name: room.room_name,
    control_mode: room.control_mode,
    is_active: room.is_active !== undefined ? room.is_active : true
  }
  editDialogVisible.value = true
}

const saveRoom = async () => {
  try {
    const token = localStorage.getItem(getStorageKey('token'))
    await axios.put(`/api/admin/sync-rooms/${editingRoomId.value}`, editForm.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    ElMessage.success('房间更新成功')
    editDialogVisible.value = false
    await refreshRooms()
  } catch (error) {
    console.error('更新房间失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新房间失败')
  }
}

const cleanupEmptyRooms = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem(getStorageKey('token'))
    const response = await axios.post('/api/admin/sync-rooms/cleanup', {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    ElMessage.success(response.data.message)
    await refreshRooms()
  } catch (error) {
    console.error('清理空房间失败:', error)
    ElMessage.error(error.response?.data?.detail || '清理空房间失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshRooms()
  
  // 每30秒自动刷新
  const intervalId = setInterval(refreshRooms, 30000)
  
  // 组件卸载时清除定时器
  onBeforeUnmount(() => {
    clearInterval(intervalId)
  })
})
</script>

<script>
import { onBeforeUnmount } from 'vue'
</script>

<style scoped>
.admin-rooms-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.stats {
  display: flex;
  gap: 40px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: var(--radius-xs);
}
</style>
