<script setup>
// 定义该组件可以接收哪些属性
defineProps({
  title: String,
  excerpt: String,
  date: String
});
</script>

<template>
  <article class="post-item">
    <h2 class="post-title">{{ title }}</h2>
    <p class="post-meta">发布于 {{ date }}</p>
    <p class="post-excerpt">{{ excerpt }}</p>
    <a href="#" class="read-more">阅读全文 &rarr;</a>
  </article>
</template>

<style scoped>
.post-item {
  background-color: #fff;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 30px;
  transition: box-shadow 0.2s ease-in-out;
}
.post-item:hover {
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.post-title {
  margin-top: 0;
  font-size: 28px;
}
.post-meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}
.post-excerpt {
  color: #666;
}
.read-more {
  display: inline-block;
  margin-top: 15px;
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}
</style>