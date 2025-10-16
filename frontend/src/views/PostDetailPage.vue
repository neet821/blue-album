<template>
  <div class="post-detail-container">
    <div class="container">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else-if="post" class="post-content">
        <div class="post-header">
          <h1>{{ post.title }}</h1>
          <div class="post-meta">
            <span class="author">
              作者: 
              <router-link :to="`/author/${post.author_id}`" class="author-link">
                {{ post.author?.username || '未知' }}
              </router-link>
            </span>
            <span class="category">分类: {{ post.category || '未分类' }}</span>
            <span class="views">👁️ {{ post.views || 0 }} 次浏览</span>
            <span class="date">{{ formatDate(post.created_at) }}</span>
          </div>
          
          <div v-if="canEdit" class="post-actions">
            <button @click="editPost" class="btn-edit">编辑</button>
            <button @click="deletePost" class="btn-delete">删除</button>
          </div>
        </div>

        <div class="post-body">
          <p v-if="!post.content">暂无内容</p>
          <div v-else class="content markdown-body" v-html="renderedContent"></div>
        </div>

        <div class="post-footer">
          <button @click="goBack" class="btn-back">返回列表</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';
// 使用 marked 库进行 Markdown 渲染
import { marked } from 'marked';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const post = ref(null);
const loading = ref(true);
const error = ref('');

const postId = route.params.id;

const canEdit = computed(() => {
  if (!authStore.isAuthenticated || !post.value) return false;
  // 仅管理员可以编辑/删除
  return authStore.currentUser?.role === 'admin';
});

// Markdown 渲染
const renderedContent = computed(() => {
  if (!post.value?.content) return '';
  try {
    return marked(post.value.content);
  } catch (e) {
    console.error('Markdown 渲染失败:', e);
    return post.value.content; // 降级为纯文本
  }
});

async function fetchPost() {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await axios.get(`http://localhost:8000/api/posts/${postId}`);
    post.value = response.data;
  } catch (err) {
    error.value = err.response?.status === 404 ? '文章不存在' : '获取文章失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

function editPost() {
  router.push(`/posts/${postId}/edit`);
}

async function deletePost() {
  if (!confirm('确定要删除这篇文章吗？此操作不可恢复！')) {
    return;
  }
  
  try {
    await axios.delete(
      `http://localhost:8000/api/posts/${postId}`,
      {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    );
    
    alert('文章已删除');
    router.push('/posts');
  } catch (err) {
    alert(err.response?.data?.detail || '删除失败');
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString('zh-CN');
}

function goBack() {
  router.push('/posts');
}

onMounted(() => {
  fetchPost();
});
</script>

<style scoped>
.post-detail-container {
  padding: 40px 0;
  min-height: 80vh;
}

.loading, .error-message {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: var(--primary-text);
}

.error-message {
  color: #e74c3c;
}

.post-content {
  background: var(--primary-bg);
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
}

.post-header {
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 20px;
  margin-bottom: 30px;
}

.post-header h1 {
  margin: 0 0 16px 0;
  color: var(--primary-text);
  font-size: 32px;
}

.post-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: var(--secondary-text);
  margin-bottom: 16px;
}

.author-link {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.author-link:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.post-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-edit, .btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-edit {
  background: var(--link-color);
  color: white;
}

.btn-edit:hover {
  background: var(--link-hover);
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

.post-body {
  margin-bottom: 40px;
}

.content {
  color: var(--primary-text);
  line-height: 1.8;
  font-size: 16px;
}

/* Markdown 样式 */
.markdown-body {
  word-wrap: break-word;
  color: var(--primary-text);
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--primary-text);
}

.markdown-body h1 {
  font-size: 2em;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.3em;
}

.markdown-body h2 {
  font-size: 1.5em;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.3em;
}

.markdown-body h3 {
  font-size: 1.25em;
}

.markdown-body p {
  margin-bottom: 16px;
}

.markdown-body code {
  background: var(--secondary-bg);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
  color: var(--primary-text);
}

.markdown-body pre {
  background: var(--secondary-bg);
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 16px;
  border: 1px solid var(--border-color);
}

.markdown-body pre code {
  background: none;
  padding: 0;
}

.markdown-body blockquote {
  border-left: 4px solid var(--border-color);
  padding-left: 16px;
  color: var(--secondary-text);
  margin: 16px 0;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 2em;
  margin-bottom: 16px;
}

.markdown-body li {
  margin-bottom: 4px;
}

.markdown-body a {
  color: var(--link-color);
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body img {
  max-width: 100%;
  height: auto;
}

.markdown-body table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}

.markdown-body table th,
.markdown-body table td {
  border: 1px solid var(--border-color);
  padding: 8px 12px;
}

.markdown-body table th {
  background: var(--secondary-bg);
  font-weight: 600;
}

.post-footer {
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
}

.btn-back {
  padding: 10px 20px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .post-content {
    padding: 24px;
  }
  
  .post-header h1 {
    font-size: 24px;
  }
}
</style>
