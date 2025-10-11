<script setup>
// 引入布局组件
import TheHeader from './components/TheHeader.vue';
import PostList from './components/PostList.vue';
import TheFooter from './components/TheFooter.vue';
</script>

<template>
  <div id="blog-app">
    <TheHeader />
    <PostList />
    <TheFooter />
  </div>
</template>

<style>
/* 
  将全局样式放在 App.vue 的 <style> 块中 (不加 scoped)
  或者放在 src/style.css 中
*/
body {
  margin: 0;
  background-color: #f9f9f9;
}

#blog-app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 全局和基础样式 */
:root {
  --primary-text-color: #333;
  --secondary-text-color: #666;
  --border-color: #eee;
  --background-color: #f9f9f9;
  --link-color: #007bff;
}

#app-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
  font-family: sans-serif;
}
.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 20px;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

/* 头部 */
.blog-header {
  background-color: #fff;
  border-bottom: 1px solid var(--border-color);
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
}
.blog-header nav a {
  color: var(--secondary-text-color);
  text-decoration: none;
  margin-left: 20px;
  font-weight: 500;
}
.blog-header nav a:hover {
  color: var(--link-color);
}

/* 主要内容区域 */
.main-content {
  padding: 40px 20px;
}

/* 文章条目 */
.post-item {
  background-color: #fff;
  padding: 30px;
  border: 1px solid var(--border-color);
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
  color: var(--primary-text-color);
}

.post-meta {
  font-size: 14px;
  color: var(--secondary-text-color);
  margin-bottom: 15px;
}

.post-excerpt {
  color: var(--secondary-text-color);
}

.read-more {
  display: inline-block;
  margin-top: 15px;
  color: var(--link-color);
  text-decoration: none;
  font-weight: bold;
}

/* 页脚 */
.blog-footer {
  text-align: center;
  padding: 30px 0;
  border-top: 1px solid var(--border-color);
  color: var(--secondary-text-color);
  font-size: 14px;
  background-color: #fff;
}
</style>
