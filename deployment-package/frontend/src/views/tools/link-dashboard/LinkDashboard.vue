<template>
  <div class="link-dashboard">
    <div class="container-fluid">
      <!-- 顶部操作栏 -->
      <div class="dashboard-header">
        <div class="header-left">
          <button @click="goBack" class="btn-back">
            ← 返回工具列表
          </button>
          <h1>🔖 网站收藏管理</h1>
        </div>
        <div class="header-right">
          <button @click="showAddCategoryModal = true" class="btn-add">
            ＋ 新建分类
          </button>
          <button @click="showAddLinkModal = true" class="btn-add-link">
            ＋ 添加链接
          </button>
        </div>
      </div>

      <!-- 分类标签栏 -->
      <div class="categories-bar">
        <button 
          :class="['category-tab', { active: selectedCategory === null }]"
          @click="selectedCategory = null"
        >
          全部 ({{ totalLinks }})
        </button>
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="['category-tab', { active: selectedCategory === category.id }]"
          @click="selectedCategory = category.id"
          @contextmenu.prevent="editCategory(category)"
          :title="'右键编辑分类'"
        >
          {{ category.name }} ({{ category.link_count || 0 }})
        </button>
      </div>

      <!-- 链接卡片网格 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="filteredLinks.length === 0" class="empty-state">
        <p>{{ selectedCategory ? '该分类下暂无链接' : '还没有收藏任何网站，点击右上角"添加链接"开始收藏吧！' }}</p>
      </div>
      <div v-else class="links-grid">
        <LinkCard 
          v-for="link in filteredLinks" 
          :key="link.id"
          :link="link"
          @edit="editLink"
          @delete="deleteLink"
        />
      </div>
    </div>

    <!-- 添加分类弹窗 -->
    <CategoryModal 
      v-if="showAddCategoryModal || editingCategory"
      :category="editingCategory"
      @save="saveCategory"
      @delete="deleteCategory"
      @close="closeCategoryModal"
    />

    <!-- 添加/编辑链接弹窗 -->
    <LinkModal 
      v-if="showAddLinkModal || editingLink"
      :link="editingLink"
      :categories="categories"
      @save="saveLink"
      @close="closeLinkModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import LinkCard from './components/LinkCard.vue';
import CategoryModal from './components/CategoryModal.vue';
import LinkModal from './components/LinkModal.vue';
import request from '@/utils/request';

const router = useRouter();
const authStore = useAuthStore();

// 状态
const categories = ref([]);
const links = ref([]);
const selectedCategory = ref(null);
const loading = ref(true);
const showAddCategoryModal = ref(false);
const showAddLinkModal = ref(false);
const editingCategory = ref(null);
const editingLink = ref(null);

// 计算属性
const totalLinks = computed(() => links.value.length);
const filteredLinks = computed(() => {
  if (selectedCategory.value === null) {
    return links.value;
  }
  return links.value.filter(link => link.category_id === selectedCategory.value);
});

// 方法
const goBack = () => {
  router.push('/tools');
};

const fetchCategories = async () => {
  try {
    const response = await request.get('/categories');
    categories.value = response.data;
  } catch (error) {
    console.error('获取分类失败:', error);
  }
};

const fetchLinks = async () => {
  try {
    const response = await request.get('/links');
    links.value = response.data;
  } catch (error) {
    console.error('获取链接失败:', error);
  }
};

const loadData = async () => {
  loading.value = true;
  await Promise.all([fetchCategories(), fetchLinks()]);
  loading.value = false;
};

const closeCategoryModal = () => {
  showAddCategoryModal.value = false;
  editingCategory.value = null;
};

const saveCategory = async (categoryData) => {
  try {
    if (editingCategory.value) {
      // 编辑
      await request.put(`/categories/${editingCategory.value.id}`, categoryData);
    } else {
      // 新增
      await request.post('/categories', categoryData);
    }
    await fetchCategories();
    closeCategoryModal();
  } catch (error) {
    console.error('保存分类失败:', error);
    alert('保存失败，请重试');
  }
};

const closeLinkModal = () => {
  showAddLinkModal.value = false;
  editingLink.value = null;
};

const saveLink = async (linkData) => {
  try {
    if (editingLink.value) {
      // 编辑
      await request.put(`/links/${editingLink.value.id}`, linkData);
    } else {
      // 新增
      await request.post('/links', linkData);
    }
    await loadData();
    closeLinkModal();
  } catch (error) {
    console.error('保存链接失败:', error);
    alert('保存失败，请重试');
  }
};

const editLink = (link) => {
  editingLink.value = link;
};

const editCategory = (category) => {
  editingCategory.value = category;
  showAddCategoryModal.value = true;
};

const deleteCategory = async (categoryId) => {
  if (!confirm('删除分类将同时删除该分类下的所有链接，确定要继续吗？')) return;
  
  try {
    await request.delete(`/categories/${categoryId}`);
    await loadData();
    // 如果当前选中的分类被删除,切换到全部
    if (selectedCategory.value === categoryId) {
      selectedCategory.value = null;
    }
  } catch (error) {
    console.error('删除分类失败:', error);
    alert('删除失败，请重试');
  }
};

const deleteLink = async (linkId) => {
  if (!confirm('确定要删除这个链接吗？')) return;
  
  try {
    await request.delete(`/links/${linkId}`);
    await loadData();
  } catch (error) {
    console.error('删除链接失败:', error);
    alert('删除失败，请重试');
  }
};

onMounted(() => {
  // 检查登录状态
  if (!authStore.isAuthenticated) {
    alert('请先登录');
    router.push('/login');
    return;
  }
  loadData();
});
</script>

<style scoped>
.link-dashboard {
  min-height: 100vh;
  padding: 20px 0;
  background: var(--secondary-bg);
}

.container-fluid {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 顶部栏 */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--primary-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--shadow);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left h1 {
  margin: 0;
  color: var(--primary-text);
  font-size: 28px;
}

.btn-back {
  padding: 8px 16px;
  background: var(--secondary-bg);
  color: var(--primary-text);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-back:hover {
  background: var(--border-color);
}

.header-right {
  display: flex;
  gap: 12px;
}

.btn-add,
.btn-add-link {
  padding: 10px 20px;
  background: var(--link-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-add:hover,
.btn-add-link:hover {
  background: var(--link-hover);
  transform: translateY(-2px);
}

/* 分类标签栏 */
.categories-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 30px;
  padding: 15px;
  background: var(--primary-bg);
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 2px 8px var(--shadow);
}

.category-tab {
  padding: 8px 16px;
  background: var(--secondary-bg);
  color: var(--secondary-text);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
  transition: all 0.3s;
}

.category-tab:hover {
  border-color: var(--link-color);
  color: var(--link-color);
}

.category-tab.active {
  background: var(--link-color);
  color: white;
  border-color: var(--link-color);
}

/* 内容区域 */
.loading,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--secondary-text);
  font-size: 16px;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-left,
  .header-right {
    width: 100%;
    justify-content: center;
  }

  .header-left h1 {
    font-size: 20px;
  }

  .links-grid {
    grid-template-columns: 1fr;
  }

  .categories-bar {
    overflow-x: scroll;
  }
}
</style>
