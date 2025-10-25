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
          
          <!-- 移动端折叠菜单按钮 -->
          <button @click="toggleMobileMenu" class="mobile-menu-toggle">
            <span class="hamburger-icon">{{ isMobileMenuOpen ? '✕' : '☰' }}</span>
          </button>
        </div>
      </nav>
      
      <!-- 移动端折叠菜单 -->
      <div v-if="isMobileMenuOpen" class="mobile-menu-overlay" @click="closeMobileMenu">
        <div class="mobile-menu" @click.stop>
          <div class="mobile-menu-content">
            <router-link to="/" class="mobile-menu-item" @click="closeMobileMenu">
              <span class="menu-icon">🏠</span>
              <span class="menu-text">首页</span>
            </router-link>
            
            <router-link v-if="isAdmin" to="/posts" class="mobile-menu-item" @click="closeMobileMenu">
              <span class="menu-icon">📝</span>
              <span class="menu-text">文章</span>
            </router-link>
            
            <router-link to="/tools" class="mobile-menu-item" @click="closeMobileMenu">
              <span class="menu-icon">🛠️</span>
              <span class="menu-text">工具</span>
            </router-link>
            
            <template v-if="isAuthenticated">
              <router-link to="/profile" class="mobile-menu-item" @click="closeMobileMenu">
                <span class="menu-icon">👤</span>
                <span class="menu-text">主页</span>
              </router-link>
              
              <button @click="handleLogout" class="mobile-menu-item logout-menu-item">
                <span class="menu-icon">🚪</span>
                <span class="menu-text">登出</span>
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isAdmin = computed(() => authStore.currentUser?.role === 'admin');

// 移动端菜单状态
const isMobileMenuOpen = ref(false);

const handleLogout = () => {
  authStore.logout();
  router.push('/');
  closeMobileMenu();
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};
</script>

<style scoped>
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
  margin: 0 10px;
}

.blue-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  min-height: 80px;
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
  align-items: center;
  gap: 15px;
  z-index: 2;
}

.vinyl-disc {
  width: 50px;
  height: 50px;
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
  width: 15px;
  height: 15px;
  background: var(--accent-text);
  border-radius: 50%;
  box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
}

.vinyl-grooves {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
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
  width: 30px;
  height: 30px;
}

.vinyl-grooves::after {
  width: 20px;
  height: 20px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.site-title {
  margin: 0;
  font-size: 28px;
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
  display: flex;
  align-items: center;
  gap: 20px;
  z-index: 2;
  height: 36px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
  height: 36px;
}

.nav-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  border-radius: var(--radius-xl);
  font-weight: 600;
  font-size: 13px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  height: 36px;
  min-width: 60px;
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
  font-size: 16px;
  filter: drop-shadow(0 0 3px rgba(0,0,0,0.3));
}

.nav-text {
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

/* Navigation Controls */
.nav-controls {
  display: flex;
  align-items: stretch;
  gap: 15px;
  height: 36px;
}

.theme-toggle {
  background: rgba(255,255,255,0.2);
  border: 2px solid rgba(255,255,255,0.3);
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.theme-toggle:hover {
  background: rgba(255,255,255,0.3);
  transform: scale(1.1) rotate(15deg);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.theme-icon {
  font-size: 18px;
  display: block;
}

.user-link, .logout-btn, .auth-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-xl);
  text-decoration: none;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  height: 36px;
  min-width: 70px;
  box-sizing: border-box;
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

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .blue-header {
    margin: 0 5px;
  }
  
  .blue-header .container {
    padding: 15px;
    min-height: 70px;
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
    gap: 15px;
    height: 32px;
  }
  
  .nav-links {
    gap: 10px;
    height: 32px;
  }
  
  .nav-link {
    padding: 6px 10px;
    font-size: 12px;
    height: 32px;
    min-width: 50px;
  }
  
  .nav-controls {
    gap: 8px;
    height: 32px;
    align-items: stretch;
  }
  
  .theme-toggle {
    width: 32px;
    height: 32px;
    padding: 8px;
    box-sizing: border-box;
  }
  
  .theme-icon {
    font-size: 16px;
  }
  
  .user-link, .logout-btn, .auth-link {
    padding: 6px 12px;
    font-size: 12px;
    height: 32px;
    min-width: 60px;
    box-sizing: border-box;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .blue-header {
    margin: 0 5px;
  }
  
  .blue-header .container {
    flex-direction: row;
    gap: 10px;
    padding: 12px 15px;
    min-height: 60px;
    flex-wrap: wrap;
  }
  
  .logo-section {
    flex: 1;
    min-width: 120px;
  }
  
  .vinyl-disc {
    width: 30px;
    height: 30px;
  }
  
  .vinyl-center {
    width: 8px;
    height: 8px;
  }
  
  .site-title {
    font-size: 18px;
  }
  
  .main-nav {
    flex: 2;
    gap: 8px;
    justify-content: flex-end;
    height: 28px;
  }
  
  /* PC端导航链接在移动端隐藏 */
  .nav-links {
    display: none;
  }
  
  .nav-controls {
    gap: 6px;
    flex-wrap: wrap;
    height: 28px;
    align-items: stretch;
  }
  
  /* PC端用户按钮在移动端隐藏 */
  .user-link, .logout-btn, .auth-link {
    display: none;
  }
  
  .theme-toggle {
    padding: 6px;
    width: 28px;
    height: 28px;
    box-sizing: border-box;
  }
  
  .theme-icon {
    font-size: 14px;
  }
  
  /* 移动端折叠菜单按钮 */
  .mobile-menu-toggle {
    display: flex;
    background: rgba(255,255,255,0.2);
    border: 2px solid rgba(255,255,255,0.3);
    padding: 6px;
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    width: 28px;
    height: 28px;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    margin-left: 8px;
  }
  
  .mobile-menu-toggle:hover {
    background: rgba(255,255,255,0.3);
    transform: scale(1.1);
  }
  
  .hamburger-icon {
    font-size: 14px;
    display: block;
  }
  
  /* 移动端折叠菜单 */
  .mobile-menu-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 2000;
    display: flex;
    align-items: flex-start;
    justify-content: flex-end;
    padding-top: 80px;
    padding-right: 10px;
  }
  
  .mobile-menu {
    background: var(--bg-primary);
    border-radius: var(--radius-xl);
    box-shadow: 0 10px 40px var(--shadow);
    border: 2px solid var(--accent-text);
    min-width: 200px;
    max-width: 280px;
    overflow: hidden;
  }
  
  .mobile-menu-content {
    padding: 10px 0;
  }
  
  .mobile-menu-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    color: var(--text-primary);
    text-decoration: none;
    transition: all 0.3s ease;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-size: 16px;
  }
  
  .mobile-menu-item:hover {
    background: var(--bg-hover);
    transform: translateX(5px);
  }
  
  .mobile-menu-item.router-link-active {
    background: var(--accent-bg);
    color: var(--accent-text);
    font-weight: 600;
  }
  
  .menu-icon {
    font-size: 20px;
    width: 24px;
    text-align: center;
  }
  
  .menu-text {
    font-weight: 500;
  }
  
  .logout-menu-item {
    color: #ef4444;
  }
  
  .logout-menu-item:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
}
</style>