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
/* 全局样式 - 浅色模式 */
:root {
  --primary-bg: #ffffff;
  --secondary-bg: #f9f9f9;
  --primary-text: #333333;
  --secondary-text: #666666;
  --border-color: #eeeeee;
  --link-color: #007bff;
  --link-hover: #0056b3;
  --shadow: rgba(0, 0, 0, 0.1);
  --shadow-hover: rgba(0, 0, 0, 0.08);
}

/* 暗黑模式 */
body.dark-mode {
  --primary-bg: #1a1a1a;
  --secondary-bg: #2d2d2d;
  --primary-text: #e4e4e4;
  --secondary-text: #a0a0a0;
  --border-color: #404040;
  --link-color: #4a9eff;
  --link-hover: #6db3ff;
  --shadow: rgba(0, 0, 0, 0.3);
  --shadow-hover: rgba(0, 0, 0, 0.5);
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

#app-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
  font-family: sans-serif;
}

.card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
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
  border-radius: 4px;
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
  border-radius: 8px;
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
