import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/archive',
    name: 'Archive',
    component: () => import('../views/ArchivePage.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutPage.vue')
  },
  {
    path: '/tools',
    name: 'Tools',
    component: () => import('../views/ToolsPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tools/links',
    name: 'LinkDashboard',
    component: () => import('../views/tools/link-dashboard/LinkDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tools/sync-room',
    name: 'SyncRoomList',
    component: () => import('../views/SyncRoomList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tools/sync-room/:id',
    name: 'SyncRoomPlayer',
    component: () => import('../views/SyncRoomPlayer.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfilePage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/posts',
    name: 'Posts',
    component: () => import('../views/PostsPage.vue')
  },
  {
    path: '/posts/new',
    name: 'PostNew',
    component: () => import('../views/PostEditorPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetailPage.vue')
  },
  {
    path: '/posts/:id/edit',
    name: 'PostEdit',
    component: () => import('../views/PostEditorPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/author/:id',
    name: 'Author',
    component: () => import('../views/AuthorPage.vue')
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/AdminUsersPage.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/rooms',
    name: 'AdminRooms',
    component: () => import('../views/AdminRooms.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫 - 检查认证状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  console.log('🛡️ 路由守卫检查:', {
    to: to.path,
    requiresAuth,
    hasToken: !!token
  });

  if (requiresAuth && !token) {
    console.log('⚠️ 需要认证但没有 token,跳转到登录页');
    // 跳转到登录页并显示消息
    next({
      path: '/login',
      query: { message: '请先登录' }
    });
  } else {
    next();
  }
});

export default router;
