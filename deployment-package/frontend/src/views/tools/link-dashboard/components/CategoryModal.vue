<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ category ? '编辑分类' : '新建分类' }}</h2>
        <button @click="$emit('close')" class="btn-close">✕</button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="category-name">分类名称 *</label>
          <input 
            id="category-name"
            v-model="formData.name"
            type="text"
            placeholder="例如：开发工具、学习资源、娱乐休闲"
            required
            maxlength="50"
          />
        </div>

        <div class="form-group">
          <label for="category-description">描述</label>
          <textarea 
            id="category-description"
            v-model="formData.description"
            rows="3"
            placeholder="可选，描述这个分类的用途"
            maxlength="200"
          ></textarea>
        </div>

        <div class="form-actions">
          <button 
            v-if="category" 
            type="button" 
            @click="handleDelete" 
            class="btn-delete-category"
          >
            🗑️ 删除分类
          </button>
          <div class="form-actions-right">
            <button type="button" @click="$emit('close')" class="btn-cancel">
              取消
            </button>
            <button type="submit" class="btn-submit">
              {{ category ? '保存修改' : '创建分类' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';

const props = defineProps({
  category: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['save', 'close', 'delete']);

const formData = reactive({
  name: '',
  description: ''
});

onMounted(() => {
  if (props.category) {
    formData.name = props.category.name;
    formData.description = props.category.description || '';
  }
});

const handleSubmit = () => {
  if (!formData.name.trim()) {
    alert('请输入分类名称');
    return;
  }
  emit('save', {
    name: formData.name.trim(),
    description: formData.description.trim()
  });
};

const handleDelete = () => {
  emit('delete', props.category.id);
  emit('close');
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
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
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
.form-group textarea {
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
.form-group textarea:focus {
  outline: none;
  border-color: var(--link-color);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
}

.form-actions-right {
  display: flex;
  gap: 12px;
}

.btn-cancel,
.btn-submit,
.btn-delete-category {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-delete-category {
  background: #ff4444;
  color: white;
}

.btn-delete-category:hover {
  background: #cc0000;
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

.btn-submit:hover {
  background: var(--link-hover);
}

@media (max-width: 768px) {
  .modal-content {
    max-width: 100%;
  }
}
</style>
