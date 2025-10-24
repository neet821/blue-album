<template>
  <div class="link-card">
    <a :href="link.url" target="_blank" rel="noopener noreferrer" class="link-content">
      <!-- Favicon -->
      <div class="link-icon">
        <img 
          v-if="faviconUrl" 
          :src="faviconUrl" 
          :alt="link.title"
          @error="onFaviconError"
        />
        <span v-else>🔗</span>
      </div>

      <!-- 标题和描述 -->
      <div class="link-info">
        <h3 class="link-title">{{ link.title }}</h3>
        <p v-if="link.description" class="link-description">{{ link.description }}</p>
        <p class="link-url">{{ displayUrl }}</p>
      </div>
    </a>

    <!-- 操作按钮 -->
    <div class="link-actions">
      <button @click.stop="$emit('edit', link)" class="btn-edit" title="编辑">
        ✏️
      </button>
      <button @click.stop="$emit('delete', link.id)" class="btn-delete" title="删除">
        🗑️
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  link: {
    type: Object,
    required: true
  }
});

defineEmits(['edit', 'delete']);

const faviconError = ref(false);

// 获取 favicon URL
const faviconUrl = computed(() => {
  if (faviconError.value) return null;
  try {
    const url = new URL(props.link.url);
    return `${url.origin}/favicon.ico`;
  } catch {
    return null;
  }
});

// 简化显示的 URL
const displayUrl = computed(() => {
  try {
    const url = new URL(props.link.url);
    return url.hostname.replace('www.', '');
  } catch {
    return props.link.url;
  }
});

const onFaviconError = () => {
  faviconError.value = true;
};
</script>

<style scoped>
.link-card {
  position: relative;
  background: var(--primary-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 4px var(--shadow);
}

.link-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px var(--shadow);
  border-color: var(--link-color);
}

.link-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  text-decoration: none;
  color: var(--primary-text);
}

.link-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--secondary-bg);
  border-radius: 8px;
  font-size: 24px;
}

.link-icon img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.link-info {
  flex: 1;
  min-width: 0;
}

.link-title {
  margin: 0 0 6px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.link-description {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: var(--secondary-text);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.link-url {
  margin: 0;
  font-size: 12px;
  color: var(--link-color);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.link-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 0 16px 12px;
  opacity: 0;
  transition: opacity 0.3s;
}

.link-card:hover .link-actions {
  opacity: 1;
}

.btn-edit,
.btn-delete {
  padding: 6px 12px;
  background: var(--secondary-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-edit:hover {
  background: var(--link-color);
  border-color: var(--link-color);
}

.btn-delete:hover {
  background: #ff4444;
  border-color: #ff4444;
}

@media (max-width: 768px) {
  .link-actions {
    opacity: 1;
  }
}
</style>
