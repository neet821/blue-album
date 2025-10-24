import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  
  // --- 添加路径别名 ---
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  
  // --- 添加 server 配置 ---
  server: {
    proxy: {
      // API代理配置
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      
      // ✅ WebSocket代理配置 - 关键!
      '/ws': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true  // 启用WebSocket代理
      }
    }
  }
})
