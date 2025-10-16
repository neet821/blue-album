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
    component: () => import('../views/ToolsPage.vue')
  },
  {
    path: '/tools/links',
    name: 'LinkDashboard',
    component: () => import('../views/tools/link-dashboard/LinkDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfilePage.vue')
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
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
