<script setup>
// 引入布局组件
import TheHeader from './components/TheHeader.vue';
import TheFooter from './components/TheFooter.vue';
import { useThemeStore } from './stores/theme';

// 初始化主题
const themeStore = useThemeStore();
</script>

<template>
  <div id="app">
    <TheHeader />
    <main>
      <router-view />
    </main>
    <TheFooter />
  </div>
</template>

<style>
/* Blue Album 主题 - 浅色模式 */
:root {
  --primary-bg: #ffffff;
  --secondary-bg: #f8fafc;
  --accent-bg: #e3f2fd;
  --primary-text: #1a202c;
  --secondary-text: #4a5568;
  --accent-text: #2b6cb0;
  --border-color: #e2e8f0;
  --link-color: #3182ce;
  --link-hover: #2c5aa0;
  --shadow: rgba(49, 130, 206, 0.15);
  --shadow-hover: rgba(49, 130, 206, 0.25);
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

/* Blue Album 暗黑模式 */
body.dark-mode {
  --primary-bg: #0f1419;
  --secondary-bg: #1a202c;
  --accent-bg: #2d3748;
  --primary-text: #f7fafc;
  --secondary-text: #a0aec0;
  --accent-text: #63b3ed;
  --border-color: #2d3748;
  --link-color: #63b3ed;
  --link-hover: #90cdf4;
  --shadow: rgba(99, 179, 237, 0.2);
  --shadow-hover: rgba(99, 179, 237, 0.3);
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

body {
  margin: 0;
  background-color: var(--secondary-bg);
  color: var(--primary-text);
  transition: background-color 0.3s ease, color 0.3s ease;
}

#blog-app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: var(--primary-text);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .container {
    max-width: 90%;
    padding: 0 15px;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .container {
    max-width: 95%;
    padding: 0 10px;
  }
}

#app-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
  font-family: sans-serif;
}

.card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 20px;
  margin-top: 20px;
  background-color: var(--primary-bg);
  box-shadow: 0 2px 4px var(--shadow);
  transition: all 0.3s ease;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 20px;
  background-color: var(--link-color);
  color: white;
  border: none;
  border-radius: var(--radius-xs);
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: var(--link-hover);
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
  background-color: var(--primary-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 20px 0;
  transition: all 0.3s ease;
}

.blog-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.blog-header h1 {
  margin: 0;
  font-size: 24px;
  color: var(--primary-text);
}

.blog-header nav a {
  color: var(--secondary-text);
  text-decoration: none;
  margin-left: 20px;
  font-weight: 500;
  transition: color 0.3s ease;
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
  background-color: var(--primary-bg);
  padding: 30px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  margin-bottom: 30px;
  transition: all 0.3s ease;
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

/* 页脚 */
.blog-footer {
  text-align: center;
  padding: 30px 0;
  border-top: 1px solid var(--border-color);
  color: var(--secondary-text);
  font-size: 14px;
  background-color: var(--primary-bg);
  transition: all 0.3s ease;
}

/* 输入框样式 */
input, textarea, select {
  background-color: var(--primary-bg);
  color: var(--primary-text);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--link-color);
}

/* 链接样式 */
a {
  color: var(--link-color);
  transition: color 0.3s ease;
}

a:hover {
  color: var(--link-hover);
}
</style>
