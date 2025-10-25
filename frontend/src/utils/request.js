import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 10000
});

// 请求拦截器 - 自动添加 token
request.interceptors.request.use(
  config => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器 - 统一处理错误
request.interceptors.response.use(
  response => response,
  error => {
    // Token 过期或未授权,自动跳转登录
    if (error.response?.status === 401) {
      console.log('🔒 检测到 401 错误,开始处理...');
      
      const authStore = useAuthStore();
      authStore.logout();
      console.log('✅ Token 已清除');
      
      // 跳转到登录页并显示消息
      router.push({
        path: '/login',
        query: { message: '登录已过期,请重新登录' }
      });
      console.log('✅ 已跳转到登录页');
    }
    
    // 请求超时
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      console.error('⏱️ 请求超时:', error);
      error.message = '请求超时,请检查网络连接后重试';
    }
    
    // 网络错误
    if (error.message === 'Network Error') {
      console.error('🌐 网络错误:', error);
      error.message = '网络连接失败,请检查网络设置';
    }
    
    // 其他错误
    console.error('响应错误:', error);
    return Promise.reject(error);
  }
);

export default request;
