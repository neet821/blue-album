import { defineStore } from 'pinia';
import apiClient, { API_ENDPOINTS } from '../utils/api.js';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },

  actions: {
    async register(username, email, password) {
      try {
        console.log('发送注册请求:', { username, email });
        const response = await apiClient.post(API_ENDPOINTS.REGISTER, {
          username,
          email,
          password,
        });

        console.log('注册响应:', response.data);

        // 注册成功后自动登录
        if (response.data) {
          await this.login(username, password);
        }
        return { success: true };
      } catch (error) {
        console.error('注册失败 - 完整错误:', error);
        console.error('错误响应:', error.response);
        console.error('错误数据:', error.response?.data);

        let errorMessage = '注册失败，请重试';

        if (error.response?.data?.detail) {
          // FastAPI 返回的错误信息
          if (typeof error.response.data.detail === 'string') {
            errorMessage = error.response.data.detail;
          } else if (Array.isArray(error.response.data.detail)) {
            // 验证错误
            errorMessage = error.response.data.detail.map(e => e.msg).join(', ');
          }
        } else if (error.message) {
          errorMessage = error.message;
        }

        return {
          success: false,
          message: errorMessage
        };
      }
    },

    async login(username, password) {
      try {
        // FastAPI 的 OAuth2PasswordRequestForm 需要使用 form-data 格式
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post(API_ENDPOINTS.LOGIN, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const { access_token } = response.data;

        // 保存 token
        this.token = access_token;
        localStorage.setItem('token', access_token);

        // 获取用户信息
        await this.fetchUserInfo();

        return { success: true };
      } catch (error) {
        console.error('登录失败:', error);
        return {
          success: false,
          message: error.response?.data?.detail || '登录失败，请检查用户名和密码'
        };
      }
    },

    async fetchUserInfo() {
      try {
        const response = await apiClient.get(API_ENDPOINTS.USER_INFO);

        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.logout();
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },

    // 初始化时检查 token 有效性
    async checkAuth() {
      if (this.token && !this.user) {
        await this.fetchUserInfo();
      }
    },
  },
});
