import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/workspace' },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { guest: true },
    },
    {
      path: '/workspace',
      component: () => import('../views/workspace/WorkspaceView.vue'),
      meta: { auth: true },
    },
    {
      path: '/profile',
      component: () => import('../views/profile/ProfileView.vue'),
      meta: { auth: true, student: true },
    },
    { path: '/unavailable', component: () => import('../views/system/UnavailableView.vue') },
    { path: '/design-preview', component: () => import('../views/design/SelectedDesignView.vue') },
    { path: '/:pathMatch(.*)*', component: () => import('../views/system/NotFoundView.vue') },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to) => {
  if (!to.meta.auth && !to.meta.guest) return
  const auth = useAuthStore()
  await auth.restore()
  if (to.meta.auth && auth.connectionError) return '/unavailable'
  if (to.meta.auth && !auth.user) return '/login'
  if (to.meta.student && auth.user?.role !== 'student') return '/workspace'
  if (to.meta.guest && auth.user && !auth.connectionError) return '/workspace'
})
