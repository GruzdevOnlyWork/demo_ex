import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/test/:testId/start',
    name: 'StartTest',
    component: () => import('../views/TestView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/test/:attemptId/take',
    name: 'TakeTest',
    component: () => import('../views/TakeTestView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/test/:attemptId/result',
    name: 'TestResult',
    component: () => import('../views/ResultView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/HistoryView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/modules',
    name: 'Modules',
    component: () => import('../views/ModulesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/modules/:id',
    name: 'ModuleDetail',
    component: () => import('../views/ModuleDetailView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && auth.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
