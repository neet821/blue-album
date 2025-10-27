// API 配置工具
// 自动检测环境并设置正确的API基础URL

// 获取API基础URL
function getApiBaseUrl() {
    // 开发环境：使用Vite代理
    if (import.meta.env.DEV) {
        return ''; // 使用相对路径，通过Vite代理转发
    }

    // 生产环境：使用当前域名
    if (import.meta.env.PROD) {
        return window.location.origin;
    }

    // 默认回退
    return '';
}

// 导出API基础URL
export const API_BASE_URL = getApiBaseUrl();

// 导出完整的API端点
export const API_ENDPOINTS = {
    // 认证相关
    LOGIN: '/api/auth/login',
    REGISTER: '/api/users/register',
    USER_INFO: '/api/users/me',

    // 文章相关
    POSTS: '/api/posts',
    POST_DETAIL: (id) => `/api/posts/${id}`,
    POSTS_BY_AUTHOR: (authorId) => `/api/posts?author_id=${authorId}`,

    // 用户相关
    USER_DETAIL: (userId) => `/api/users/${userId}`,

    // 分类相关
    CATEGORIES: '/api/categories',

    // 链接相关
    LINKS: '/api/links',

    // 同步观影相关
    SYNC_ROOMS: '/api/sync-rooms',
    SYNC_ROOM_BY_CODE: (code) => `/api/sync-rooms/code/${code}`,
    SYNC_ROOM_DETAIL: (id) => `/api/sync-rooms/${id}`,
    SYNC_ROOM_JOIN: (id) => `/api/sync-rooms/${id}/join`,
    SYNC_ROOM_JOIN_BY_CODE: (code) => `/api/sync-rooms/code/${code}/join`,
    SYNC_ROOM_LEAVE: (id) => `/api/sync-rooms/${id}/leave`,
    SYNC_ROOM_MEMBERS: (id) => `/api/sync-rooms/${id}/members`,
    SYNC_ROOM_MESSAGES: (id) => `/api/sync-rooms/${id}/messages`,

    // 管理员相关
    ADMIN_USERS: '/api/admin/users',
    ADMIN_USER_DETAIL: (id) => `/api/admin/users/${id}`,
    ADMIN_SYNC_ROOMS: '/api/admin/sync-rooms',
    ADMIN_SYNC_ROOM_DETAIL: (id) => `/api/admin/sync-rooms/${id}`,
};

// 创建axios实例
import axios from 'axios';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(
    (config) => {
        const token = sessionStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器 - 处理错误
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // 401错误自动登出
        if (error.response?.status === 401) {
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('user');
            // 可以在这里触发路由跳转到登录页
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
