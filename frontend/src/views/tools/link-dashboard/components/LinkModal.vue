<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ link ? '编辑链接' : '添加链接' }}</h2>
        <button @click="$emit('close')" class="btn-close">✕</button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="link-title">网站标题 *</label>
          <input 
            id="link-title"
            v-model="formData.title"
            type="text"
            placeholder="例如：GitHub、哔哩哔哩、MDN"
            required
            maxlength="100"
          />
        </div>

        <div class="form-group">
          <label for="link-url">网站地址 *</label>
          <input 
            id="link-url"
            v-model="formData.url"
            type="url"
            placeholder="https://example.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="link-description">描述</label>
          <textarea 
            id="link-description"
            v-model="formData.description"
            rows="3"
            placeholder="可选，简单描述这个网站"
            maxlength="300"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="link-category">分类 *</label>
          <select 
            id="link-category"
            v-model="formData.category_id"
            required
          >
            <option value="" disabled>请选择分类</option>
            <option 
              v-for="category in categories" 
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <p v-if="categories.length === 0" class="hint-text">
            ⚠️ 请先创建分类
          </p>
        </div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="btn-cancel">
            取消
          </button>
          <button type="submit" class="btn-submit" :disabled="categories.length === 0">
            {{ link ? '保存修改' : '添加链接' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';

const props = defineProps({
  link: {
    type: Object,
    default: null
  },
  categories: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['save', 'close']);

const formData = reactive({
  title: '',
  url: '',
  description: '',
  category_id: ''
});

onMounted(() => {
  if (props.link) {
    formData.title = props.link.title;
    formData.url = props.link.url;
    formData.description = props.link.description || '';
    formData.category_id = props.link.category_id;
  }
});

const handleSubmit = () => {
  if (!formData.title.trim()) {
    alert('请输入网站标题');
    return;
  }
  if (!formData.url.trim()) {
    alert('请输入网站地址');
    return;
  }
  if (!formData.category_id) {
    alert('请选择分类');
    return;
  }

  // 确保 URL 格式正确
  let url = formData.url.trim();
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  emit('save', {
    title: formData.title.trim(),
    url: url,
    description: formData.description.trim(),
    category_id: formData.category_id
  });
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--primary-bg);
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  background: var(--primary-bg);
  z-index: 10;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: var(--primary-text);
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--secondary-text);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.3s;
}

.btn-close:hover {
  background: var(--secondary-bg);
  color: var(--primary-text);
}

form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-text);
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  background: var(--secondary-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--primary-text);
  font-size: 14px;
  font-family: inherit;
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
  min-height: 80px;
}

.hint-text {
  margin: 8px 0 0 0;
  font-size: 13px;
  color: #ff6b6b;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-cancel {
  background: var(--secondary-bg);
  color: var(--primary-text);
  border: 1px solid var(--border-color);
}

.btn-cancel:hover {
  background: var(--border-color);
}

.btn-submit {
  background: var(--link-color);
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: var(--link-hover);
}

.btn-submit:disabled {
  background: var(--border-color);
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 768px) {
  .modal-content {
    max-width: 100%;
    max-height: 100vh;
  }
}
</style>
