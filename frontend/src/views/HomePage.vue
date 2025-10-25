<template>
  <div class="home-page">
    <div class="container">
      <div class="welcome-section" v-if="isAuthenticated">
        <h2>欢迎回来, {{ currentUser?.username }}!</h2>
      </div>

      <PostList />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import PostList from '../components/PostList.vue';

const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUser = computed(() => authStore.currentUser);

// 页面加载时检查认证状态
onMounted(() => {
  authStore.checkAuth();
});
</script>

<style scoped>
.home-page {
  padding: 40px 0;
}

.welcome-section {
  background: var(--primary-bg);
  border-radius: var(--radius-sm);
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px var(--shadow);
  border: 1px solid var(--border-color);
}

.welcome-section h2 {
  margin: 0;
  color: var(--primary-text);
  font-size: 24px;
}
</style>
