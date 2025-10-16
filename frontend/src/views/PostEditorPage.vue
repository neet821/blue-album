<template>
  <div class="editor-container">
    <div class="container">
      <h1>{{ isEditMode ? '编辑文章' : '写新文章' }}</h1>

      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else class="editor-form">
        <div class="form-group">
          <label>标题</label>
          <input 
            v-model="form.title" 
            type="text" 
            placeholder="请输入文章标题"
            required
          />
        </div>

        <div class="form-group">
          <label>分类</label>
          <select v-model="form.category">
            <option value="未分类">未分类</option>
            <option value="技术">技术</option>
            <option value="生活">生活</option>
            <option value="随笔">随笔</option>
            <option value="教程">教程</option>
            <option value="其他">其他</option>
          </select>
        </div>

        <div class="form-group">
          <label>内容 (支持 Markdown)</label>
          <textarea 
            v-model="form.content" 
            placeholder="支持 Markdown 格式...&#10;&#10;# 标题&#10;## 二级标题&#10;**粗体** *斜体*&#10;- 列表项&#10;```代码块```"
            rows="20"
          ></textarea>
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="form-actions">
          <button @click="savePost" class="btn-save" :disabled="saving">
            {{ saving ? '保存中...' : '保存' }}
          </button>
          <button @click="cancel" class="btn-cancel">取消</button>
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

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  title: '',
  content: '',
  category: '未分类'
});

const loading = ref(false);
const saving = ref(false);
const error = ref('');

const postId = route.params.id;
const isEditMode = computed(() => !!postId);

async function fetchPost() {
  if (!isEditMode.value) return;
  
  loading.value = true;
  try {
    const response = await axios.get(`http://localhost:8000/api/posts/${postId}`);
    const post = response.data;
    
    // 权限检查
    if (post.author_id !== authStore.currentUser?.id && authStore.currentUser?.role !== 'admin') {
      alert('您没有权限编辑此文章');
      router.push('/posts');
      return;
    }
    
    form.value.title = post.title;
    form.value.content = post.content || '';
    form.value.category = post.category || '未分类';
  } catch (err) {
    error.value = '获取文章失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function savePost() {
  // 验证
  if (!form.value.title.trim()) {
    error.value = '请输入标题';
    return;
  }
  
  error.value = '';
  saving.value = true;
  
  try {
    if (isEditMode.value) {
      // 更新文章
      await axios.put(
        `http://localhost:8000/api/posts/${postId}`,
        form.value,
        {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        }
      );
      alert('文章更新成功');
      router.push(`/posts/${postId}`);
    } else {
      // 创建新文章
      const response = await axios.post(
        'http://localhost:8000/api/posts',
        form.value,
        {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        }
      );
      alert('文章发布成功');
      router.push(`/posts/${response.data.id}`);
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '保存失败';
    console.error(err);
  } finally {
    saving.value = false;
  }
}

function cancel() {
  if (isEditMode.value) {
    router.push(`/posts/${postId}`);
  } else {
    router.push('/posts');
  }
}

onMounted(() => {
  // 检查是否登录
  if (!authStore.isAuthenticated) {
    alert('请先登录');
    router.push('/login');
    return;
  }
  
  // 检查是否是管理员（只有管理员能创建/编辑文章）
  if (authStore.currentUser?.role !== 'admin') {
    alert('只有管理员可以发布文章');
    router.push('/');
    return;
  }
  
  fetchPost();
});
</script>

<style scoped>
.editor-container {
  padding: 40px 0;
  min-height: 80vh;
}

h1 {
  margin-bottom: 30px;
  color: var(--primary-text);
}

.loading {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: var(--primary-text);
}

.editor-form {
  background: var(--primary-bg);
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--secondary-text);
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
  font-family: inherit;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--link-color);
}

.form-group textarea {
  resize: vertical;
  min-height: 400px;
}

.error-message {
  padding: 12px;
  background: rgba(255, 68, 68, 0.1);
  color: #e74c3c;
  border: 1px solid rgba(255, 68, 68, 0.3);
  border-radius: 4px;
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.btn-save,
.btn-cancel {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save {
  background: #2ecc71;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #27ae60;
}

.btn-save:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
}

.btn-cancel:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .editor-form {
    padding: 24px;
  }
}
</style>
