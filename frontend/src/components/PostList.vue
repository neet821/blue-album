<script setup>
import { ref } from 'vue';
import PostItem from './PostItem.vue'; // 引入子组件

// 临时的占位数据
const posts = ref([
  { id: 1, title: '我的第一篇博客', excerpt: '这是文章的摘要内容...', date: '2025年10月11日' },
  { id: 2, title: '关于技术选型的心得', excerpt: '这是文章的摘要内容...', date: '2025年10月10日' },
  { id: 3, title: 'Nginx 配置踩坑记录', excerpt: '这是文章的摘要内容...', date: '2025年10月09日' },
]);
</script>

<template>
  <main class="main-content container">
    <!-- 循环渲染 PostItem 组件，并通过 props 传递数据 -->
    <PostItem
      v-for="post in posts"
      :key="post.id"
      :title="post.title"
      :excerpt="post.excerpt"
      :date="post.date"
    />
  </main>
</template>

<style scoped>
.main-content {
  padding: 40px 20px;
}
</style>