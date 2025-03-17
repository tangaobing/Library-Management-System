import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import router from '@/router'

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://localhost:5000', // 设置后端API地址
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // 允许跨域请求携带凭证
})

// 是否正在刷新token
let isRefreshing = false
// 重试队列
let requests = []

// 请求拦截器
service.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    
    // 如果请求不需要刷新令牌，则添加访问令牌
    if (!config.skipAuthRefresh && userStore.token) {
      config.headers['Authorization'] = `Bearer ${userStore.token}`
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果返回的不是二进制数据，则进行响应处理
    if (!(response.config.responseType === 'blob')) {
      if (res.code !== 0) {
        // 显示错误信息
        ElMessage({
          message: res.message || '请求失败',
          type: 'error',
          duration: 5 * 1000
        })

        // 处理特定错误码
        if (res.code === 401) {
          // token 过期或无效
          const userStore = useUserStore()
          userStore.logout()
          router.push('/login')
        }
        return Promise.reject(new Error(res.message || '请求失败'))
      }
      return res
    }
    return response
  },
  async error => {
    console.error('响应错误:', error)
    const { response } = error
    
    // 处理网络错误
    if (!response) {
      ElMessage({
        message: '网络连接失败，请检查网络设置',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(error)
    }

    // 如果是401错误，且不是刷新令牌请求，尝试刷新token
    if (response.status === 401 && !error.config.skipAuthRefresh) {
      const userStore = useUserStore()
      
      // 如果没有刷新令牌，直接登出
      if (!userStore.refreshToken) {
        userStore.logout()
        router.push('/login')
        return Promise.reject(error)
      }
      
      // 如果正在刷新，将请求加入队列
      if (isRefreshing) {
        return new Promise(resolve => {
          requests.push(token => {
            error.config.headers['Authorization'] = `Bearer ${token}`
            resolve(service(error.config))
          })
        })
      }
      
      isRefreshing = true
      
      try {
        // 尝试刷新token
        const newToken = await userStore.refreshAccessToken()
        
        // 执行队列中的请求
        requests.forEach(callback => callback(newToken))
        requests = []
        
        // 重试当前请求
        error.config.headers['Authorization'] = `Bearer ${newToken}`
        return service(error.config)
      } catch (refreshError) {
        console.error('刷新令牌失败:', refreshError)
        // 刷新失败，清空队列并登出
        requests = []
        userStore.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // 处理其他HTTP状态码错误
    const errorMessage = {
      400: '请求参数错误',
      401: '未授权，请重新登录',
      403: '拒绝访问',
      404: '请求错误，未找到该资源',
      405: '请求方法不被允许',
      408: '请求超时',
      422: '请求参数验证失败',
      500: '服务器内部错误',
      501: '服务未实现',
      502: '网关错误',
      503: '服务不可用',
      504: '网关超时',
      505: 'HTTP版本不受支持'
    }

    const message = errorMessage[response.status] || `请求失败: ${response.status}`
    
    ElMessage({
      message: response.data?.message || message,
      type: 'error',
      duration: 5 * 1000
    })

    return Promise.reject(error)
  }
)

export default service 