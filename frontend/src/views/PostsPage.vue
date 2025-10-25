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
          <div class="post-card-content">
            <div class="post-header">
              <h2>{{ post.title }}</h2>
              <div class="post-category">{{ post.category || '未分类' }}</div>
            </div>
            
            <div class="post-meta">
              <div class="author-info">
                <span class="author-avatar">🎵</span>
                <router-link :to="`/author/${post.author_id}`" class="author-link" @click.stop>
                  {{ post.author?.username || '未知' }}
                </router-link>
              </div>
              <div class="post-stats">
                <span class="views">👁️ {{ post.views || 0 }}</span>
                <span class="date">📅 {{ formatDate(post.created_at) }}</span>
              </div>
            </div>
            
            <p class="post-preview">{{ getPreview(post.content) }}</p>
            
            <div class="post-footer">
              <div class="read-more">
                <span>阅读更多</span>
                <span class="arrow">→</span>
              </div>
            </div>
          </div>
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
    let url = `/api/posts?skip=${skip}&limit=${pageSize}`;
    
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
  border-radius: var(--radius-xs);
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
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xs);
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
  border-radius: var(--radius-xs);
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
  border-radius: var(--radius-xs);
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
  gap: 30px;
  margin-bottom: 50px;
  padding: 20px 0;
}

.post-card {
  background: var(--primary-bg);
  padding: 0;
  border-radius: var(--radius-xl);
  box-shadow: 0 8px 32px var(--shadow);
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.post-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.post-card:hover::before {
  opacity: 0.05;
}

.post-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px var(--shadow-hover);
  border-color: var(--accent-text);
}

.post-card-content {
  position: relative;
  z-index: 2;
  padding: 30px;
  background: var(--primary-bg);
  border-radius: var(--radius-lg);
  margin: 2px;
}

.post-header {
  margin-bottom: 20px;
  position: relative;
}

.post-card h2 {
  margin: 0 0 8px 0;
  color: var(--primary-text);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.3;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.post-category {
  display: inline-block;
  background: var(--gradient-accent);
  color: white;
  padding: 4px 12px;
  border-radius: var(--radius-xs);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 0;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-avatar {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  box-shadow: 0 2px 8px var(--shadow);
}

.author-link {
  color: var(--accent-text);
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.author-link:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.post-stats {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: var(--secondary-text);
}

.views, .date {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-preview {
  color: var(--secondary-text);
  line-height: 1.7;
  margin: 0 0 20px 0;
  font-size: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.read-more {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--accent-text);
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.read-more:hover {
  color: var(--link-hover);
  transform: translateX(5px);
}

.arrow {
  transition: transform 0.3s ease;
}

.read-more:hover .arrow {
  transform: translateX(3px);
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
  border-radius: var(--radius-xs);
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

/* 响应式设计 - 平板 */
@media (max-width: 1024px) {
  .posts-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .search-section {
    flex-direction: column;
    gap: 12px;
  }
  
  .search-input,
  .category-filter,
  .sort-filter {
    width: 100%;
    min-width: auto;
  }
}

/* 响应式设计 - 手机 */
@media (max-width: 768px) {
  .posts-container {
    padding: 20px 0;
  }
  
  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .btn-create {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .search-section {
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .post-card {
    padding: 20px;
  }
  
  .post-card h2 {
    font-size: 18px;
  }
  
  .post-meta {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .pagination {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .btn-page {
    padding: 8px 16px;
    font-size: 13px;
  }
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
