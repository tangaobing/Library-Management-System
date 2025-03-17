import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

/**
 * 创建axios实例
 * baseURL: 后端API基础URL
 * timeout: 请求超时时间，增加到15秒避免网络波动导致请求失败
 * withCredentials: 允许跨域请求携带cookie
 */
const service = axios.create({
  baseURL: 'http://localhost:5000/api',  // 后端服务器地址，添加/api前缀
  timeout: 15000,
  withCredentials: true  // 允许跨域携带cookie
})

/**
 * 请求拦截器
 * 在请求发送前处理请求配置
 */
service.interceptors.request.use(
  config => {
    // 从本地存储获取token
    const token = localStorage.getItem('token')
    if (token) {
      // 添加Bearer认证头
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // 确保请求头包含正确的Content-Type
    if (config.method === 'post' || config.method === 'put') {
      config.headers['Content-Type'] = 'application/json'
    }
    
    // 打印请求信息，方便调试
    console.log('请求URL:', config.baseURL + config.url)
    console.log('请求方法:', config.method)
    console.log('请求头:', config.headers)
    
    return config
  },
  error => {
    // 请求错误处理
    console.error('请求配置错误:', error)
    ElMessage.error('请求配置错误')
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 在接收到响应后统一处理响应数据
 */
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果后端返回的是文件流，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 打印响应数据，方便调试
    console.log('响应数据:', res)
    
    // 处理成功响应，兼容code=200和code=0
    if (res.code === 200 || res.code === 0) {
      return res
    }
    
    // 处理特定错误码
    if (res.code === 401 || response.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      localStorage.removeItem('token')
      router.replace({
        path: '/login',
        query: { redirect: router.currentRoute.value.fullPath }
      })
      return Promise.reject(new Error('未授权'))
    }
    
    // 其他错误情况
    ElMessage.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  error => {
    // 响应错误处理
    console.error('响应错误:', error)
    
    if (error.response) {
      const status = error.response.status
      const errMsg = error.response.data?.message || '未知错误'
      
      switch (status) {
        case 400:
          ElMessage.error(`请求参数错误: ${errMsg}`)
          break
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          localStorage.removeItem('token')
          router.replace({
            path: '/login',
            query: { redirect: router.currentRoute.value.fullPath }
          })
          break
        case 403:
          ElMessage.error(`访问被拒绝: ${errMsg}`)
          break
        case 404:
          ElMessage.error(`请求的资源不存在: ${errMsg}`)
          break
        case 500:
          ElMessage.error(`服务器错误: ${errMsg}`)
          break
        default:
          ElMessage.error(`请求失败(${status}): ${errMsg}`)
      }
    } else if (error.message.includes('timeout')) {
      ElMessage.error('请求超时，请重试')
    } else if (error.message.includes('Network Error')) {
      ElMessage.error('网络错误，请检查您的网络连接和后端服务是否正常运行')
    } else {
      ElMessage.error(error.message || '请求失败')
    }
    
    return Promise.reject(error)
  }
)

export default service 