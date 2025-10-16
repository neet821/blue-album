<template>
  <header class="blog-header">
    <div class="container">
      <h1>我的个人博客</h1>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/archive">归档</router-link>
        <router-link to="/about">关于</router-link>
        <span class="divider">|</span>
        <router-link to="/tools">在线工具</router-link>
        
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

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
.blog-header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
  padding: 20px 0;
}
.blog-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.blog-header h1 {
  margin: 0;
  font-size: 24px;
  cursor: pointer;
}
.blog-header nav a,
.blog-header nav .router-link {
  color: #666;
  text-decoration: none;
  margin-left: 15px;
  font-weight: 500;
  transition: color 0.3s;
}
.blog-header nav a:hover,
.blog-header nav .router-link:hover {
  color: #007bff;
}
.blog-header nav .router-link-active {
  color: #007bff;
  font-weight: 600;
}
.divider {
  margin: 0 10px;
  color: #ccc;
}
</style>