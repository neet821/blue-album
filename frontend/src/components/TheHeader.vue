<template>
  <header class="blog-header">
    <div class="container">
      <h1>blue-album</h1>
      <nav>
        <router-link to="/">首页</router-link>
        <!-- 只有管理员能看到文章栏 -->
        <router-link v-if="isAdmin" to="/posts">文章</router-link>
        <router-link to="/archive">归档</router-link>
        <router-link to="/about">关于</router-link>
        <span class="divider">|</span>
        <router-link to="/tools">在线工具</router-link>
        
        <!-- 暗黑模式切换按钮 -->
        <button @click="themeStore.toggleTheme" class="theme-toggle" :title="themeStore.isDark ? '切换到浅色模式' : '切换到暗黑模式'">
          {{ themeStore.isDark ? '☀️' : '🌙' }}
        </button>
        
        <!-- 根据登录状态显示不同的按钮 -->
        <template v-if="isAuthenticated">
          <router-link to="/profile">我的主页</router-link>
          <a href="#" @click.prevent="handleLogout">登出</a>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </template>
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
.blog-header {
  background-color: var(--primary-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 20px 0;
  transition: all 0.3s ease;
}

.blog-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .blog-header .container {
    gap: 10px;
  }
  
  .blog-header nav {
    gap: 3px;
  }
  
  .blog-header nav a,
  .blog-header nav .router-link {
    margin-left: 10px;
    font-size: 14px;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .blog-header {
    padding: 15px 0;
  }
  
  .blog-header .container {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .blog-header h1 {
    font-size: 20px;
    margin-bottom: 0;
  }
  
  .blog-header nav {
    width: 100%;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: flex-start;
  }
  
  .blog-header nav a,
  .blog-header nav .router-link {
    margin-left: 0;
    margin-right: 12px;
    font-size: 13px;
    padding: 4px 8px;
    border-radius: 4px;
    background-color: var(--secondary-bg);
    transition: all 0.3s ease;
  }
  
  .blog-header nav a:hover,
  .blog-header nav .router-link:hover {
    background-color: var(--link-color);
    color: white;
  }
  
  .divider {
    display: none;
  }
  
  .theme-toggle {
    margin-left: 0;
    font-size: 16px;
    padding: 4px 8px;
  }
}

.blog-header h1 {
  margin: 0;
  font-size: 24px;
  cursor: pointer;
  color: var(--primary-text);
}

.blog-header nav {
  display: flex;
  align-items: center;
  gap: 5px;
}

.blog-header nav a,
.blog-header nav .router-link {
  color: var(--secondary-text);
  text-decoration: none;
  margin-left: 15px;
  font-weight: 500;
  transition: color 0.3s;
}

.blog-header nav a:hover,
.blog-header nav .router-link:hover {
  color: var(--link-color);
}

.blog-header nav .router-link-active {
  color: var(--link-color);
  font-weight: 600;
}

.divider {
  margin: 0 10px;
  color: var(--border-color);
}

/* 暗黑模式切换按钮 */
.theme-toggle {
  background: none;
  border: 1px solid var(--border-color);
  padding: 6px 12px;
  margin-left: 15px;
  cursor: pointer;
  font-size: 18px;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.theme-toggle:hover {
  background-color: var(--secondary-bg);
  border-color: var(--link-color);
  transform: scale(1.05);
}
</style>