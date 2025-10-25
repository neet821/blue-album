<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>用户注册</h2>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            id="username"
            type="text" 
            v-model="username" 
            placeholder="请输入用户名" 
            required
            minlength="3"
          >
        </div>

        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            id="email"
            type="email" 
            v-model="email" 
            placeholder="请输入邮箱" 
            required
          >
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input 
            id="password"
            type="password" 
            v-model="password" 
            placeholder="请输入密码 (至少6位)" 
            required
            minlength="6"
          >
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            id="confirmPassword"
            type="password" 
            v-model="confirmPassword" 
            placeholder="请再次输入密码" 
            required
          >
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <div class="auth-footer">
        已有账号? <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const errorMessage = ref('');

const handleRegister = async () => {
  // 验证密码匹配
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致';
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  const result = await authStore.register(
    username.value, 
    email.value, 
    password.value
  );

  loading.value = false;

  if (result.success) {
    router.push('/');
  } else {
    errorMessage.value = result.message;
  }
};
</script>

<style scoped>
.auth-container {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  margin: 0 0 30px 0;
  text-align: center;
  color: #333;
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
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.auth-footer a {
  color: #007bff;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}

.error-message {
  background-color: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .auth-container {
    padding: 15px;
  }
  
  .auth-card {
    padding: 30px;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .auth-container {
    padding: 10px;
    min-height: 100vh;
  }
  
  .auth-card {
    padding: 20px;
    max-width: 100%;
  }
  
  .auth-card h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .form-group input {
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .btn-primary {
    font-size: 16px;
    padding: 14px;
  }
}
</style>
