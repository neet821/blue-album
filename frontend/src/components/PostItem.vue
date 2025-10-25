<script setup>
// 定义该组件可以接收哪些属性
defineProps({
  title: String,
  excerpt: String,
  date: String,
  author: String
});
</script>

<template>
  <article class="post-item">
    <h2 class="post-title">{{ title }}</h2>
    <p class="post-meta">
      <span v-if="author" class="author">作者: {{ author }} · </span>
      发布于 {{ date }}
    </p>
    <p class="post-excerpt">{{ excerpt }}</p>
    <a href="#" class="read-more">阅读全文 &rarr;</a>
  </article>
</template>

<style scoped>
.post-item {
  background-color: var(--primary-bg);
  padding: 30px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  margin-bottom: 30px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px var(--shadow);
}
.post-item:hover {
  box-shadow: 0 4px 15px var(--shadow-hover);
}
.post-title {
  margin-top: 0;
  font-size: 28px;
  color: var(--primary-text);
}
.post-meta {
  font-size: 14px;
  color: var(--secondary-text);
  margin-bottom: 15px;
}
.post-meta .author {
  color: var(--link-color);
  font-weight: 500;
}
.post-excerpt {
  color: var(--secondary-text);
}
.read-more {
  display: inline-block;
  margin-top: 15px;
  color: var(--link-color);
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}
.read-more:hover {
  color: var(--link-hover);
}
</style>