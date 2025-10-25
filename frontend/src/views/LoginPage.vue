<template>
  <div class="auth-container">
    <div class="music-background">
      <div class="vinyl-record"></div>
      <div class="sound-waves">
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
      </div>
    </div>
    
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo-section">
          <div class="mini-vinyl">🎵</div>
          <h2>欢迎回到 blue-album</h2>
        </div>
        <p class="auth-subtitle">欢迎回来</p>
      </div>
      
      <div v-if="errorMessage" class="error-message">
        <span class="error-icon">⚠️</span>
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="username" class="form-label">
            <span class="label-icon">👤</span>
            用户名
          </label>
          <input 
            id="username"
            type="text" 
            v-model="username" 
            placeholder="请输入用户名" 
            required
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="password" class="form-label">
            <span class="label-icon">🔒</span>
            密码
          </label>
          <input 
            id="password"
            type="password" 
            v-model="password" 
            placeholder="请输入密码" 
            required
            class="form-input"
          >
        </div>

        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="loading" class="loading-spinner"></span>
          <span class="btn-icon">🎵</span>
          <span>{{ loading ? '登录中...' : '登录' }}</span>
        </button>
      </form>

      <div class="auth-footer">
        <p>还没有账号? <router-link to="/register" class="register-link">立即注册</router-link></p>
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
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
  background: var(--gradient-primary);
  overflow: hidden;
}

.music-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  opacity: 0.1;
}

.vinyl-record {
  position: absolute;
  top: 20%;
  left: 10%;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(45deg, #1a202c, #2d3748);
  animation: spin 20s linear infinite;
  box-shadow: 0 0 50px rgba(0,0,0,0.3);
}

.vinyl-record::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: var(--accent-text);
  border-radius: 50%;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.sound-waves {
  position: absolute;
  top: 30%;
  right: 15%;
  display: flex;
  gap: 10px;
  align-items: end;
}

.wave {
  width: 4px;
  background: var(--accent-text);
  border-radius: 2px;
  animation: wave 1.5s ease-in-out infinite;
}

.wave:nth-child(1) {
  height: 20px;
  animation-delay: 0s;
}

.wave:nth-child(2) {
  height: 40px;
  animation-delay: 0.2s;
}

.wave:nth-child(3) {
  height: 30px;
  animation-delay: 0.4s;
}

@keyframes wave {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.5); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.auth-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-2xl);
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding: 50px;
  width: 100%;
  max-width: 450px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.auth-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 15px;
}

.mini-vinyl {
  font-size: 32px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.auth-card h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-subtitle {
  margin: 0;
  color: var(--secondary-text);
  font-size: 16px;
  font-weight: 500;
}

.auth-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: var(--primary-text);
  font-weight: 600;
  font-size: 14px;
}

.label-icon {
  font-size: 16px;
}

.form-input {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 16px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.8);
  color: var(--primary-text);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-text);
  box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
  transform: translateY(-2px);
}

.btn-login {
  width: 100%;
  padding: 18px;
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-login:hover::before {
  left: 100%;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(49, 130, 206, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.btn-icon {
  font-size: 18px;
}

.auth-footer {
  text-align: center;
  color: var(--secondary-text);
}

.auth-footer p {
  margin: 0;
  font-size: 14px;
}

.register-link {
  color: var(--accent-text);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.register-link:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.error-message {
  background: linear-gradient(135deg, #fee, #fcc);
  border: 2px solid #f56565;
  color: #c53030;
  padding: 15px 20px;
  border-radius: var(--radius-sm);
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(245, 101, 101, 0.2);
}

.error-icon {
  font-size: 18px;
}

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .auth-container {
    padding: 15px;
  }
  
  .auth-card {
    padding: 40px;
    max-width: 400px;
  }
  
  .vinyl-record {
    width: 150px;
    height: 150px;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .auth-container {
    padding: 10px;
  }
  
  .auth-card {
    padding: 30px 25px;
    max-width: 100%;
    border-radius: var(--radius-xl);
  }
  
  .auth-card h2 {
    font-size: 24px;
  }
  
  .vinyl-record {
    width: 100px;
    height: 100px;
    top: 10%;
    left: 5%;
  }
  
  .sound-waves {
    right: 10%;
    top: 20%;
  }
  
  .form-input {
    font-size: 16px; /* 防止iOS缩放 */
    padding: 12px 16px;
  }
  
  .btn-login {
    font-size: 16px;
    padding: 15px;
  }
}
</style>
