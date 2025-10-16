<template>
  <div class="admin-container">
    <div class="container">
      <h1>用户管理</h1>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else class="users-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>角色</th>
              <th>状态</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['role-badge', user.role]">
                  {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  {{ user.is_active ? '正常' : '已禁用' }}
                </span>
              </td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td class="actions">
                <button @click="editUser(user)" class="btn-edit">编辑</button>
                <button 
                  @click="toggleUserStatus(user)" 
                  :class="['btn-toggle', user.is_active ? 'deactivate' : 'activate']"
                >
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
                <button 
                  v-if="user.id !== currentUser?.id"
                  @click="deleteUser(user)" 
                  class="btn-delete"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 编辑用户对话框 -->
      <div v-if="editingUser" class="modal">
        <div class="modal-content">
          <h2>编辑用户: {{ editingUser.username }}</h2>
          <form @submit.prevent="saveUser">
            <div class="form-group">
              <label>邮箱</label>
              <input v-model="editForm.email" type="email" required />
            </div>
            
            <div class="form-group">
              <label>角色</label>
              <select v-model="editForm.role" :disabled="editingUser.id === currentUser?.id">
                <option value="user">普通用户</option>
                <option value="admin">管理员</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>状态</label>
              <select v-model="editForm.is_active">
                <option :value="true">正常</option>
                <option :value="false">已禁用</option>
              </select>
            </div>
            
            <div class="modal-actions">
              <button type="submit" class="btn-save">保存</button>
              <button type="button" @click="cancelEdit" class="btn-cancel">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const currentUser = computed(() => authStore.currentUser);

const users = ref([]);
const loading = ref(true);
const error = ref('');
const editingUser = ref(null);
const editForm = ref({
  email: '',
  role: 'user',
  is_active: true
});

// 获取所有用户
async function fetchUsers() {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await axios.get('http://localhost:8000/api/admin/users', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    users.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || '获取用户列表失败';
    if (err.response?.status === 403) {
      error.value = '您没有管理员权限';
    }
  } finally {
    loading.value = false;
  }
}

// 编辑用户
function editUser(user) {
  editingUser.value = user;
  editForm.value = {
    email: user.email,
    role: user.role,
    is_active: user.is_active
  };
}

// 保存用户
async function saveUser() {
  try {
    await axios.put(
      `http://localhost:8000/api/admin/users/${editingUser.value.id}`,
      editForm.value,
      {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    );
    
    alert('用户信息更新成功');
    editingUser.value = null;
    fetchUsers();
  } catch (err) {
    alert(err.response?.data?.detail || '更新失败');
  }
}

// 取消编辑
function cancelEdit() {
  editingUser.value = null;
}

// 切换用户状态
async function toggleUserStatus(user) {
  const newStatus = !user.is_active;
  const action = newStatus ? '启用' : '禁用';
  
  if (!confirm(`确定要${action}用户 "${user.username}" 吗?`)) {
    return;
  }
  
  try {
    await axios.put(
      `http://localhost:8000/api/admin/users/${user.id}`,
      { is_active: newStatus },
      {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    );
    
    alert(`${action}成功`);
    fetchUsers();
  } catch (err) {
    alert(err.response?.data?.detail || `${action}失败`);
  }
}

// 删除用户
async function deleteUser(user) {
  if (!confirm(`确定要删除用户 "${user.username}" 吗? 此操作不可恢复!`)) {
    return;
  }
  
  try {
    await axios.delete(
      `http://localhost:8000/api/admin/users/${user.id}`,
      {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    );
    
    alert('用户删除成功');
    fetchUsers();
  } catch (err) {
    alert(err.response?.data?.detail || '删除失败');
  }
}

// 格式化日期
function formatDate(dateString) {
  return new Date(dateString).toLocaleString('zh-CN');
}

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.admin-container {
  padding: 40px 0;
  min-height: 80vh;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

.loading, .error-message {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error-message {
  color: #e74c3c;
}

.users-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #555;
}

.role-badge, .status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin {
  background: #3498db;
  color: white;
}

.role-badge.user {
  background: #95a5a6;
  color: white;
}

.status-badge.active {
  background: #2ecc71;
  color: white;
}

.status-badge.inactive {
  background: #e74c3c;
  color: white;
}

.actions {
  display: flex;
  gap: 8px;
}

.actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-edit:hover {
  background: #2980b9;
}

.btn-toggle.deactivate {
  background: #f39c12;
  color: white;
}

.btn-toggle.activate {
  background: #2ecc71;
  color: white;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

/* 模态框 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-content h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-save {
  background: #2ecc71;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-save:hover {
  background: #27ae60;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #7f8c8d;
}
</style>
