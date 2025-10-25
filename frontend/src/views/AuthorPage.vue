<template>
  <div class="author-page">
    <div class="container">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else>
        <div class="author-header">
          <h1>{{ authorName }} 的文章</h1>
          <p class="author-stats">共 {{ posts.length }} 篇文章</p>
        </div>

        <div v-if="posts.length === 0" class="empty-state">
          <p>该作者还没有发布文章</p>
        </div>

        <div v-else class="posts-grid">
          <div 
            v-for="post in posts" 
            :key="post.id" 
            class="post-card"
            @click="goToPost(post.id)"
          >
            <h2>{{ post.title }}</h2>
            <div class="post-meta">
              <span class="category">{{ post.category || '未分类' }}</span>
              <span class="date">{{ formatDate(post.created_at) }}</span>
            </div>
            <p class="post-preview">{{ getPreview(post.content) }}</p>
          </div>
        </div>

        <div class="back-btn">
          <button @click="goBack" class="btn-back">返回</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const authorId = route.params.id;
const authorName = ref('');
const posts = ref([]);
const loading = ref(true);
const error = ref('');

async function fetchAuthorPosts() {
  loading.value = true;
  error.value = '';
  
  try {
    // 获取该作者的所有文章
    const response = await axios.get(
      `/api/posts?author_id=${authorId}`
    );
    posts.value = response.data;
    
    // 从第一篇文章获取作者名（如果有文章）
    if (posts.value.length > 0 && posts.value[0].author) {
      authorName.value = posts.value[0].author.username;
    } else {
      // 如果没有文章，尝试获取用户信息
      const userResponse = await axios.get(`/api/users/${authorId}`);
      authorName.value = userResponse.data.username;
    }
  } catch (err) {
    error.value = '获取作者文章失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

function goToPost(postId) {
  router.push(`/posts/${postId}`);
}

function goBack() {
  router.back();
}

function getPreview(content) {
  if (!content) return '暂无内容';
  return content.length > 150 ? content.substring(0, 150) + '...' : content;
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('zh-CN');
}

onMounted(() => {
  fetchAuthorPosts();
});
</script>

<style scoped>
.author-page {
  padding: 40px 0;
  min-height: 80vh;
}

.loading,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: var(--secondary-text);
}

.error-message {
  text-align: center;
  padding: 60px 20px;
  color: #e74c3c;
  font-size: 18px;
}

.author-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px;
  background: var(--primary-bg);
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.author-header h1 {
  margin: 0 0 12px 0;
  color: var(--primary-text);
  font-size: 28px;
}

.author-stats {
  color: var(--secondary-text);
  font-size: 16px;
  margin: 0;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.post-card {
  background: var(--primary-bg);
  padding: 24px;
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px var(--shadow-hover);
}

.post-card h2 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: var(--primary-text);
}

.post-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--secondary-text);
  margin-bottom: 12px;
}

.category {
  background: var(--link-color);
  color: white;
  padding: 2px 8px;
  border-radius: var(--radius-xs);
  font-size: 12px;
}

.post-preview {
  color: var(--secondary-text);
  line-height: 1.6;
  margin: 0;
}

.back-btn {
  text-align: center;
  padding: 20px 0;
}

.btn-back {
  padding: 10px 30px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: var(--radius-xs);
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #7f8c8d;
}
</style>
