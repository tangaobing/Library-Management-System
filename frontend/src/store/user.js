import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { login as loginApi, getCurrentUser, updateUser } from '@/api/user'

/**
 * 用户状态管理
 * 使用Pinia管理用户登录状态、令牌和用户信息
 */
export const useUserStore = defineStore('user', () => {
  // 状态定义
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)

  /**
   * 用户登录
   * @param {string} username - 用户名
   * @param {string} password - 密码
   * @returns {Promise} - 登录结果
   */
  const login = async (username, password) => {
    try {
      console.log('尝试登录:', username)
      const res = await loginApi(username, password)
      
      // 登录成功处理
      if (res.code === 200 || res.code === 0) {
        console.log('登录响应:', res)
        
        // 保存token到状态和本地存储
        token.value = res.data.access_token
        localStorage.setItem('token', res.data.access_token)
        
        // 保存用户信息
        userInfo.value = res.data.user
        console.log('用户信息已保存:', userInfo.value)
        
        console.log('登录成功:', res.data.user.username)
        return res.data
      } else {
        console.error('登录响应错误:', res)
        throw new Error(res.message || '登录失败')
      }
    } catch (error) {
      console.error('登录异常:', error)
      throw error
    }
  }

  /**
   * 用户登出
   * 清除token和用户信息
   */
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    console.log('用户已登出')
  }

  /**
   * 获取当前用户信息
   * @returns {Promise} - 用户信息
   */
  const fetchCurrentUser = async () => {
    try {
      // 如果已有用户信息，直接返回
      if (userInfo.value) {
        return userInfo.value
      }
      
      const res = await getCurrentUser()
      if (res.code === 200 || res.code === 0) {
        userInfo.value = res.data
        return res.data
      } else {
        throw new Error(res.message || '获取用户信息失败')
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  /**
   * 更新用户信息
   * @param {Object} data - 要更新的用户数据
   * @returns {Promise} - 更新结果
   */
  const updateUserInfo = async (data) => {
    try {
      if (!userInfo.value || !userInfo.value.id) {
        throw new Error('用户未登录')
      }
      
      const res = await updateUser(userInfo.value.id, data)
      if (res.code === 0 || res.code === 200) {
        // 更新本地用户信息
        userInfo.value = { ...userInfo.value, ...data }
        ElMessage.success('更新成功')
        return res.data
      } else {
        throw new Error(res.message || '更新失败')
      }
    } catch (error) {
      ElMessage.error(error.message || '更新失败')
      throw error
    }
  }

  return {
    token,
    userInfo,
    login,
    logout,
    fetchCurrentUser,
    updateUserInfo
  }
}) 