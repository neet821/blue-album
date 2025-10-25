<template>
  <header class="blue-header">
    <div class="container">
      <div class="logo-section">
        <div class="vinyl-disc">
          <div class="vinyl-center"></div>
          <div class="vinyl-grooves"></div>
        </div>
        <h1 class="site-title">
          <span class="title-main">blue</span>
          <span class="title-accent">album</span>
        </h1>
      </div>
      
      <nav class="main-nav">
        <div class="nav-links">
          <router-link to="/" class="nav-link">
            <span class="nav-icon">🏠</span>
            <span class="nav-text">首页</span>
          </router-link>
          <router-link v-if="isAdmin" to="/posts" class="nav-link">
            <span class="nav-icon">📝</span>
            <span class="nav-text">文章</span>
          </router-link>
          <router-link to="/tools" class="nav-link">
            <span class="nav-icon">🛠️</span>
            <span class="nav-text">工具</span>
          </router-link>
        </div>
        
        <div class="nav-controls">
          <!-- 暗黑模式切换按钮 -->
          <button @click="themeStore.toggleTheme" class="theme-toggle" :title="themeStore.isDark ? '切换到浅色模式' : '切换到暗黑模式'">
            <span class="theme-icon">{{ themeStore.isDark ? '☀️' : '🌙' }}</span>
          </button>
          
          <!-- 根据登录状态显示不同的按钮 -->
          <template v-if="isAuthenticated">
            <router-link to="/profile" class="user-link">
              <span class="user-icon">👤</span>
              <span class="user-text">我的主页</span>
            </router-link>
            <button @click="handleLogout" class="logout-btn">
              <span class="logout-icon">🚪</span>
              <span class="logout-text">登出</span>
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="auth-link login-link">
              <span class="auth-icon">🔑</span>
              <span class="auth-text">登录</span>
            </router-link>
            <router-link to="/register" class="auth-link register-link">
              <span class="auth-icon">✨</span>
              <span class="auth-text">注册</span>
            </router-link>
          </template>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isAdmin = computed(() => authStore.currentUser?.role === 'admin');

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
/* ===== 移动优先设计 - 基础样式 (≤480px) ===== */
.blue-header {
  background: var(--gradient-primary);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid var(--accent-text);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px var(--shadow);
  border-radius: var(--radius-lg);
  margin: 0 3px;
}

.blue-header .container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px 12px;
  position: relative;
  overflow: hidden;
  min-height: auto;
  align-items: stretch;
}

.blue-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Logo Section */
.logo-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 5px 0;
  z-index: 2;
}

.vinyl-disc {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: linear-gradient(45deg, #1a202c, #2d3748);
  position: relative;
  animation: spin 10s linear infinite;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.vinyl-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 6px;
  height: 6px;
  background: var(--accent-text);
  border-radius: 50%;
  box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
}

.vinyl-grooves {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 50%;
}

.vinyl-grooves::before,
.vinyl-grooves::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 50%;
}

.vinyl-grooves::before {
  width: 15px;
  height: 15px;
}

.vinyl-grooves::after {
  width: 10px;
  height: 10px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.site-title {
  margin: 0;
  font-size: 16px;
  font-weight: 900;
  cursor: pointer;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.title-main {
  color: #ffffff;
  text-shadow: 0 0 10px rgba(255,255,255,0.5);
}

.title-accent {
  color: var(--accent-text);
  margin-left: 5px;
  font-style: italic;
}

/* Navigation */
.main-nav {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  width: 100%;
  height: 32px;
  gap: 8px;
  z-index: 2;
}

.nav-links {
  display: flex;
  gap: 4px;
  height: 32px;
  justify-content: flex-start;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.nav-links::-webkit-scrollbar {
  display: none;
}

.nav-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 6px 6px;
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  border-radius: var(--radius-xl);
  font-weight: 600;
  font-size: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  height: 32px;
  min-width: 40px;
  flex-shrink: 0;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.nav-link.router-link-active {
  background: rgba(255,255,255,0.25);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.nav-icon {
  font-size: 12px;
  filter: drop-shadow(0 0 3px rgba(0,0,0,0.3));
}

.nav-text {
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
  display: none;
}

/* Navigation Controls */
.nav-controls {
  display: flex;
  align-items: stretch;
  gap: 4px;
  height: 32px;
  flex-shrink: 0;
}

.theme-toggle {
  background: rgba(255,255,255,0.2);
  border: 2px solid rgba(255,255,255,0.3);
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  flex-shrink: 0;
}

.theme-toggle:hover {
  background: rgba(255,255,255,0.3);
  transform: scale(1.1) rotate(15deg);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.theme-icon {
  font-size: 14px;
  display: block;
}

.user-link, .logout-btn, .auth-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 6px 8px;
  border-radius: var(--radius-xl);
  text-decoration: none;
  font-weight: 600;
  font-size: 10px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  height: 32px;
  min-width: 40px;
  box-sizing: border-box;
  flex-shrink: 0;
}

.user-link, .auth-link {
  background: rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.9);
  border: 1px solid rgba(255,255,255,0.3);
}

.logout-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ffffff;
  border: 1px solid rgba(239, 68, 68, 0.3);
  cursor: pointer;
}

.register-link {
  background: var(--gradient-accent);
  border: 1px solid rgba(255,255,255,0.5);
}

.user-link:hover, .auth-link:hover, .logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.user-link:hover, .auth-link:hover {
  background: rgba(255,255,255,0.3);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.user-text, .logout-text, .auth-text {
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
  display: none;
}

/* ===== 平板适配 (481px-768px) ===== */
@media (min-width: 481px) {
  .blue-header {
    margin: 0 5px;
  }

  .blue-header .container {
    flex-direction: row;
    padding: 15px;
    min-height: 70px;
    gap: 15px;
  }

  .logo-section {
    flex: 0 0 auto;
    justify-content: flex-start;
    padding: 0;
  }

  .vinyl-disc {
    width: 35px;
    height: 35px;
  }

  .vinyl-center {
    width: 10px;
    height: 10px;
  }

  .site-title {
    font-size: 22px;
  }

  .main-nav {
    display: flex;
    flex: 1;
    height: 32px;
    gap: 15px;
  }

  .nav-links {
    flex: 1;
    gap: 10px;
    overflow-x: visible;
  }

  .nav-link {
    height: 32px;
    padding: 6px 10px;
    font-size: 12px;
    min-width: 50px;
    gap: 4px;
  }

  .nav-icon {
    font-size: 14px;
  }

  .nav-text {
    display: inline;
  }

  .nav-controls {
    gap: 8px;
    height: 32px;
  }

  .theme-toggle {
    width: 32px;
    height: 32px;
    padding: 8px;
  }

  .theme-icon {
    font-size: 16px;
  }

  .user-link, .logout-btn, .auth-link {
    height: 32px;
    padding: 6px 12px;
    font-size: 12px;
    min-width: 60px;
    gap: 4px;
  }

  .user-text, .logout-text, .auth-text {
    display: inline;
  }
}

/* ===== 桌面适配 (≥769px) ===== */
@media (min-width: 769px) {
  .blue-header {
    margin: 0 10px;
  }

  .blue-header .container {
    padding: 20px;
    min-height: 80px;
  }

  .logo-section {
    gap: 15px;
  }

  .vinyl-disc {
    width: 50px;
    height: 50px;
  }

  .vinyl-center {
    width: 15px;
    height: 15px;
  }

  .vinyl-grooves {
    width: 40px;
    height: 40px;
  }

  .vinyl-grooves::before {
    width: 30px;
    height: 30px;
  }

  .vinyl-grooves::after {
    width: 20px;
    height: 20px;
  }

  .site-title {
    font-size: 28px;
  }

  .main-nav {
    height: 36px;
    gap: 20px;
  }

  .nav-links {
    gap: 15px;
    height: 36px;
  }

  .nav-link {
    height: 36px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 60px;
    gap: 6px;
  }

  .nav-icon {
    font-size: 16px;
  }

  .nav-controls {
    gap: 15px;
    height: 36px;
  }

  .theme-toggle {
    width: 36px;
    height: 36px;
    padding: 10px;
  }

  .theme-icon {
    font-size: 18px;
  }

  .user-link, .logout-btn, .auth-link {
    height: 36px;
    padding: 8px 14px;
    font-size: 13px;
    min-width: 70px;
    gap: 6px;
  }
}
</style>