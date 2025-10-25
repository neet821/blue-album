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

        <!-- 管理员工具 - 只有管理员可见 -->
        <div v-if="isAdmin" class="admin-tools-section">
          <h2 class="section-title">
            <span class="icon">👑</span>
            管理员工具
          </h2>
          
          <div class="admin-tools-grid">
            <!-- 用户管理 -->
            <div class="tool-card admin-tool" @click="navigateTo('/admin/users')">
              <div class="tool-icon">👥</div>
              <h3>用户管理</h3>
              <p>管理系统用户，分配权限</p>
              <div class="tool-meta">
                <span class="badge admin">管理员专用</span>
              </div>
            </div>

            <!-- 房间管理 -->
            <div class="tool-card admin-tool" @click="navigateTo('/admin/rooms')">
              <div class="tool-icon">🏠</div>
              <h3>房间管理</h3>
              <p>查看和管理所有同步观影房间</p>
              <div class="tool-meta">
                <span class="badge admin">管理员专用</span>
              </div>
            </div>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

const router = useRouter();
const isAdmin = ref(false);

// 检查用户是否为管理员
const checkAdminStatus = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      isAdmin.value = false;
      return;
    }

    const response = await axios.get('/api/users/me', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    isAdmin.value = response.data.role === 'admin';
  } catch (error) {
    console.error('检查管理员状态失败:', error);
    isAdmin.value = false;
  }
};

onMounted(() => {
  checkAdminStatus();
});

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
  border-radius: var(--radius-md);
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

/* 管理员工具区域 */
.admin-tools-section {
  grid-column: 1 / -1;
  margin-top: 40px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--radius-lg);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.section-title {
  color: white;
  font-size: 24px;
  margin-bottom: 25px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.section-title .icon {
  font-size: 32px;
}

.admin-tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.tool-card.admin-tool {
  background: white;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.tool-card.admin-tool:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.tool-card.admin-tool h3 {
  font-size: 20px;
  margin: 15px 0 10px;
  color: #333;
}

.tool-card.admin-tool p {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
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
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 500;
}

.badge.disabled {
  background: var(--border-color);
  color: var(--secondary-text);
}

.badge.admin {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .admin-tools-grid {
    grid-template-columns: 1fr;
  }
  
  .admin-tools-section {
    padding: 20px;
  }
}
</style>

