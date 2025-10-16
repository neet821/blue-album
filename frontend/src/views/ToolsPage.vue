<template>
  <div class="tools-page">
    <div class="container">
      <h1>在线工具</h1>
      <p class="subtitle">实用工具集合，提升你的工作效率</p>

      <div class="tools-grid">
        <!-- 网站聚合工具 -->
        <div class="tool-card" @click="navigateTo('/tools/links')">
          <div class="tool-icon">🔖</div>
          <h2>网站收藏管理</h2>
          <p>管理你的网站收藏，分类整理，快速访问</p>
          <div class="tool-meta">
            <span class="badge">核心功能</span>
            <span class="badge">已登录可用</span>
          </div>
        </div>

        <!-- 多人音视频同步工具 -->
        <div class="tool-card" @click="navigateTo('/tools/sync-room')">
          <div class="tool-icon">🎬</div>
          <h2>多人同步观影</h2>
          <p>和朋友一起在线同步观看视频，实时互动</p>
          <div class="tool-meta">
            <span class="badge">核心功能</span>
            <span class="badge">WebSocket</span>
          </div>
        </div>

        <!-- 预留：未来工具 -->
        <div class="tool-card coming-soon">
          <div class="tool-icon">🔧</div>
          <h2>更多工具</h2>
          <p>敬请期待...</p>
          <div class="tool-meta">
            <span class="badge disabled">即将上线</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.tools-page {
  padding: 40px 0;
  min-height: 80vh;
}

h1 {
  margin-bottom: 12px;
  color: var(--primary-text);
  text-align: center;
}

.subtitle {
  text-align: center;
  color: var(--secondary-text);
  font-size: 16px;
  margin-bottom: 50px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.tool-card {
  background: var(--primary-bg);
  padding: 40px 30px;
  border-radius: 12px;
  border: 2px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.tool-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px var(--shadow-hover);
  border-color: var(--link-color);
}

.tool-card.coming-soon {
  opacity: 0.6;
  cursor: not-allowed;
}

.tool-card.coming-soon:hover {
  transform: none;
  border-color: var(--border-color);
}

.tool-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.tool-card h2 {
  margin: 0 0 12px 0;
  color: var(--primary-text);
  font-size: 24px;
}

.tool-card p {
  color: var(--secondary-text);
  line-height: 1.6;
  margin-bottom: 20px;
}

.tool-meta {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  background: var(--link-color);
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.disabled {
  background: var(--border-color);
  color: var(--secondary-text);
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style>

