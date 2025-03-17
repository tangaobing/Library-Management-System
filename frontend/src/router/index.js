import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/layout/index.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页', icon: 'House', requiresAuth: true }
      },
      {
        path: 'books',
        name: 'Books',
        component: () => import('@/views/books/index.vue'),
        meta: { title: '图书管理', icon: 'Reading', requiresAuth: true }
      },
      {
        path: 'books/add',
        name: 'AddBook',
        component: () => import('@/views/books/add.vue'),
        meta: { title: '添加图书', requiresAuth: true, hidden: true }
      },
      {
        path: 'books/edit/:id',
        name: 'EditBook',
        component: () => import('@/views/books/edit.vue'),
        meta: { title: '编辑图书', requiresAuth: true, hidden: true }
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/views/categories/index.vue'),
        meta: { title: '分类管理', icon: 'Files', requiresAuth: true }
      },
      {
        path: 'borrows',
        name: 'Borrows',
        component: () => import('@/views/borrows/index.vue'),
        meta: { title: '借阅管理', icon: 'Tickets', requiresAuth: true }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/index.vue'),
        meta: { title: '用户管理', icon: 'User', requiresAuth: true, roles: ['admin'] }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: {
          title: '个人信息',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 获取用户状态
  const userStore = useUserStore()
  const token = userStore.token
  
  // 打印调试信息
  console.log('路由守卫 - 目标路由:', to.path)
  console.log('路由守卫 - 当前token:', token)
  
  // 判断页面是否需要登录权限
  if (to.meta.requiresAuth) {
    // 如果需要登录权限但没有token，则重定向到登录页
    if (!token) {
      console.log('路由守卫 - 未登录，重定向到登录页')
      next({ 
        path: '/login', 
        query: { redirect: to.fullPath } 
      })
      return
    }
    
    // 如果需要特定角色权限，则检查用户角色
    if (to.meta.roles && to.meta.roles.length > 0) {
      const userRole = userStore.userInfo?.role
      if (!userRole || !to.meta.roles.includes(userRole)) {
        console.log('路由守卫 - 无权限访问')
        next({ path: '/dashboard' })
        return
      }
    }
  }
  
  // 如果已登录且要访问登录页，则重定向到首页
  if (to.path === '/login' && token) {
    console.log('路由守卫 - 已登录，重定向到首页')
    next({ path: '/dashboard' })
    return
  }
  
  // 其他情况正常放行
  next()
})

export default router 