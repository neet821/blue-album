<script setup>
import { ref, onMounted } from 'vue'; // 引入 onMounted
import axios from 'axios'; // 引入 axios
import PostItem from './PostItem.vue';

// 创建一个响应式变量来存储文章
const posts = ref([]);
const error = ref(null);

// onMounted 是一个生命周期钩子，在组件挂载到页面后执行
onMounted(async () => {
  try {
    // 从后端 API 获取文章数据
    const response = await axios.get('/api/posts');
    posts.value = response.data;
  } catch (err) {
    console.error('获取文章失败:', err);
    error.value = '无法加载文章列表，请稍后再试。';
  }
});
</script>

<template>
  <main class="main-content container">
    <!-- 如果加载出错，显示错误信息 -->
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <!-- 否则，循环渲染文章 -->
    <PostItem
      v-else
      v-for="post in posts"
      :key="post.id"
      :title="post.title"
      :excerpt="post.content"
      :author="post.author?.username"
      :date="new Date(post.created_at).toLocaleDateString()"
    />

    <!-- 如果没有文章，显示提示 -->
    <div v-if="!error && posts.length === 0">
      <p>暂无文章。</p>
    </div>
  </main>
</template>

<style scoped>
.main-content {
  padding: 40px 20px;
}
.error-message {
  color: #e74c3c;
  text-align: center;
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid rgba(255, 68, 68, 0.3);
  padding: 12px;
  border-radius: 4px;
}
</style>