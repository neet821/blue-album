<template>
  <div class="posts-container">
    <div class="container">
      <div class="header-section">
        <h1>所有文章</h1>
        <router-link 
          v-if="authStore.currentUser?.role === 'admin'" 
          to="/posts/new" 
          class="btn-create"
        >
          ✏️ 写文章
        </router-link>
      </div>

      <!-- 搜索和筛选区 -->
      <div class="search-section">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索文章标题或内容..." 
          @input="handleSearch"
          class="search-input"
        />
        <select v-model="selectedCategory" @change="handleCategoryChange" class="category-filter">
          <option value="">所有分类</option>
          <option value="技术">技术</option>
          <option value="生活">生活</option>
          <option value="随笔">随笔</option>
          <option value="教程">教程</option>
          <option value="未分类">未分类</option>
          <option value="其他">其他</option>
        </select>
        <select v-model="sortBy" @change="handleSortChange" class="sort-filter">
          <option value="date">最新发布</option>
          <option value="views">最多浏览</option>
        </select>
      </div>

      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else-if="posts.length === 0" class="empty-state">
        <p>还没有文章,快来创建第一篇吧!</p>
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
            <span class="author">
              作者: 
              <router-link :to="`/author/${post.author_id}`" class="author-link" @click.stop>
                {{ post.author?.username || '未知' }}
              </router-link>
            </span>
            <span class="category">分类: {{ post.category || '未分类' }}</span>
            <span class="views">👁️ {{ post.views || 0 }} 次浏览</span>
            <span class="date">{{ formatDate(post.created_at) }}</span>
          </div>
          <p class="post-preview">{{ getPreview(post.content) }}</p>
        </div>
      </div>

      <div v-if="posts.length > 0" class="pagination">
        <button 
          @click="prevPage" 
          :disabled="currentPage === 1"
          class="btn-page"
        >
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} 页</span>
        <button 
          @click="nextPage" 
          :disabled="posts.length < pageSize"
          class="btn-page"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const router = useRouter();
const authStore = useAuthStore();

const posts = ref([]);
const loading = ref(true);
const error = ref('');
const currentPage = ref(1);
const pageSize = 10;
const searchQuery = ref('');
const selectedCategory = ref('');
const sortBy = ref('date'); // 'date' 或 'views'
let searchTimeout = null;

async function fetchPosts() {
  loading.value = true;
  error.value = '';
  
  try {
    const skip = (currentPage.value - 1) * pageSize;
    let url = `http://localhost:8000/api/posts?skip=${skip}&limit=${pageSize}`;
    
    if (searchQuery.value) {
      url += `&search=${encodeURIComponent(searchQuery.value)}`;
    }
    
    if (selectedCategory.value) {
      url += `&category=${encodeURIComponent(selectedCategory.value)}`;
    }
    
    const response = await axios.get(url);
    let fetchedPosts = response.data;
    
    // 前端排序（按浏览量或日期）
    if (sortBy.value === 'views') {
      fetchedPosts.sort((a, b) => (b.views || 0) - (a.views || 0));
    }
    
    posts.value = fetchedPosts;
  } catch (err) {
    error.value = '获取文章列表失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  // 防抖：输入停止500ms后才搜索
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    fetchPosts();
  }, 500);
}

function handleCategoryChange() {
  currentPage.value = 1;
  fetchPosts();
}

function handleSortChange() {
  currentPage.value = 1;
  fetchPosts();
}

function goToPost(postId) {
  router.push(`/posts/${postId}`);
}

function getPreview(content) {
  if (!content) return '暂无内容';
  return content.length > 150 ? content.substring(0, 150) + '...' : content;
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('zh-CN');
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchPosts();
  }
}

function nextPage() {
  currentPage.value++;
  fetchPosts();
}

onMounted(() => {
  fetchPosts();
});
</script>

<style scoped>
.posts-container {
  padding: 40px 0;
  min-height: 80vh;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  color: var(--primary-text);
  margin: 0;
}

.btn-create {
  padding: 12px 24px;
  background: var(--link-color);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-create:hover {
  background: var(--link-hover);
}

/* 搜索区域样式 */
.search-section {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--primary-bg);
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
  background: var(--primary-bg);
  color: var(--primary-text);
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: var(--link-color);
}

.category-filter {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
  background: var(--primary-bg);
  color: var(--primary-text);
  cursor: pointer;
  min-width: 150px;
  transition: border-color 0.3s;
}

.category-filter:focus {
  outline: none;
  border-color: var(--link-color);
}

.sort-filter {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
  background: var(--primary-bg);
  color: var(--primary-text);
  cursor: pointer;
  min-width: 130px;
  transition: border-color 0.3s;
}

.sort-filter:focus {
  outline: none;
  border-color: var(--link-color);
}

.loading, .error-message, .empty-state {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: var(--primary-text);
}

.error-message {
  color: #e74c3c;
}

.empty-state {
  color: var(--secondary-text);
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.post-card {
  background: var(--primary-bg);
  padding: 24px;
  border-radius: 8px;
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
  color: var(--primary-text);
  font-size: 20px;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--secondary-text);
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

.post-preview {
  color: var(--secondary-text);
  line-height: 1.6;
  margin: 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.btn-page {
  padding: 10px 20px;
  background: var(--secondary-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: var(--primary-text);
  transition: all 0.3s;
}

.btn-page:hover:not(:disabled) {
  background: var(--border-color);
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: var(--secondary-text);
  font-size: 14px;
}

@media (max-width: 768px) {
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .header-section {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>
