<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>用户登录</h2>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            id="username"
            type="text" 
            v-model="username" 
            placeholder="请输入用户名" 
            required
          >
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input 
            id="password"
            type="password" 
            v-model="password" 
            placeholder="请输入密码" 
            required
          >
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="auth-footer">
        还没有账号? <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');

// 检查 URL 参数中的消息
onMounted(() => {
  if (route.query.message) {
    errorMessage.value = route.query.message;
  }
});

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  const result = await authStore.login(username.value, password.value);

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
  background: var(--primary-bg);
  border-radius: 8px;
  box-shadow: 0 2px 10px var(--shadow);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.auth-card h2 {
  margin: 0 0 30px 0;
  text-align: center;
  color: var(--primary-text);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--secondary-text);
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--link-color);
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: var(--link-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--link-hover);
}

.btn-primary:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
  color: var(--secondary-text);
}

.auth-footer a {
  color: var(--link-color);
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}

.error-message {
  background-color: rgba(255, 68, 68, 0.1);
  border: 1px solid rgba(255, 68, 68, 0.3);
  color: #ff4444;
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
