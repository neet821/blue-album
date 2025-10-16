<template>
  <div class="page-container">
    <div class="container">
      <h1>个人中心</h1>
      
      <div class="profile-grid">
        <!-- 用户信息卡片 -->
        <div class="card user-info-card">
          <h2>个人信息</h2>
          <div v-if="currentUser">
            <div class="info-item">
              <span class="label">用户名:</span>
              <span class="value">{{ currentUser.username }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱:</span>
              <span class="value">{{ currentUser.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">角色:</span>
              <span :class="['role-badge', currentUser.role]">
                {{ currentUser.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </div>
            <div class="info-item">
              <span class="label">注册时间:</span>
              <span class="value">{{ formatDate(currentUser.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- 修改密码卡片 -->
        <div class="card password-card">
          <h2>修改密码</h2>
          <form @submit.prevent="changePassword">
            <div class="form-group">
              <label>当前密码</label>
              <input 
                v-model="passwordForm.oldPassword" 
                type="password" 
                required 
                placeholder="请输入当前密码"
              />
            </div>
            
            <div class="form-group">
              <label>新密码</label>
              <input 
                v-model="passwordForm.newPassword" 
                type="password" 
                required 
                minlength="6"
                placeholder="至少6个字符"
              />
            </div>
            
            <div class="form-group">
              <label>确认新密码</label>
              <input 
                v-model="passwordForm.confirmPassword" 
                type="password" 
                required 
                placeholder="再次输入新密码"
              />
            </div>
            
            <div v-if="passwordError" class="error-message">
              {{ passwordError }}
            </div>
            
            <div v-if="passwordSuccess" class="success-message">
              {{ passwordSuccess }}
            </div>
            
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? '处理中...' : '修改密码' }}
            </button>
          </form>
        </div>
      </div>

      <!-- 管理员专用: 用户管理入口 -->
      <div v-if="currentUser?.role === 'admin'" class="admin-section">
        <h2>管理员功能</h2>
        <router-link to="/admin/users" class="btn-admin">
          🔧 用户管理
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const currentUser = computed(() => authStore.currentUser);

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const loading = ref(false);
const passwordError = ref('');
const passwordSuccess = ref('');

// 修改密码
async function changePassword() {
  passwordError.value = '';
  passwordSuccess.value = '';
  
  // 验证新密码
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = '两次输入的新密码不一致';
    return;
  }
  
  if (passwordForm.value.newPassword.length < 6) {
    passwordError.value = '新密码至少需要6个字符';
    return;
  }
  
  loading.value = true;
  
  try {
    await axios.put(
      'http://localhost:8000/api/users/me/password',
      {
        old_password: passwordForm.value.oldPassword,
        new_password: passwordForm.value.newPassword
      },
      {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    );
    
    passwordSuccess.value = '密码修改成功!';
    
    // 清空表单
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    };
    
    // 3秒后清除成功消息
    setTimeout(() => {
      passwordSuccess.value = '';
    }, 3000);
    
  } catch (err) {
    console.error('修改密码失败:', err);
    passwordError.value = err.response?.data?.detail || '修改密码失败,请重试';
  } finally {
    loading.value = false;
  }
}

// 格式化日期
function formatDate(dateString) {
  return new Date(dateString).toLocaleString('zh-CN');
}
</script>

<style scoped>
.page-container {
  padding: 40px 0;
  min-height: 80vh;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card h2 {
  margin-bottom: 20px;
  color: #555;
  font-size: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #888;
  font-weight: 500;
}

.info-item .value {
  color: #333;
}

.role-badge {
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.error-message {
  padding: 12px;
  background: #fee;
  color: #e74c3c;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.success-message {
  padding: 12px;
  background: #d4edda;
  color: #155724;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.admin-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 8px;
  text-align: center;
}

.admin-section h2 {
  color: white;
  margin-bottom: 20px;
}

.btn-admin {
  display: inline-block;
  padding: 12px 30px;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: transform 0.3s;
}

.btn-admin:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}
</style>
