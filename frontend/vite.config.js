import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // --- 添加 server 配置 ---
  server: {
    proxy: {
      // 字符串简写写法
      // '/api': 'http://127.0.0.1:8000',

      // 选项写法，更灵活
      '/api': {
        target: 'http://127.0.0.1:8000', // 目标后端服务地址
        changeOrigin: true,             // 改变源，后端服务器收到的请求头中的host会是目标地址
        // 如果你的后端 API 路径本身不包含 /api，可以用 rewrite
        // rewrite: (path) => path.replace(/^\/api/, '') 
      }
    }
  }
})
