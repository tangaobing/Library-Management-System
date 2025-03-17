import request from './request'

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise} - 返回Promise对象
 */
export function login(username, password) {
  return request({
    url: '/auth/login',
    method: 'post',
    data: { username, password }
  })
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @returns {Promise} - 返回Promise对象
 */
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getUsers(params) {
  return request({
    url: '/users',
    method: 'get',
    params
  })
}

/**
 * 获取当前登录用户信息
 * @returns {Promise} - 返回Promise对象
 */
export function getCurrentUser() {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

/**
 * 获取用户详情
 * @param {number} id - 用户ID
 * @returns {Promise} - 返回Promise对象
 */
export function getUser(id) {
  return request({
    url: `/users/${id}`,
    method: 'get'
  })
}

/**
 * 创建用户
 * @param {Object} data - 用户数据
 * @returns {Promise} - 返回Promise对象
 */
export function createUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}

/**
 * 更新用户
 * @param {number} id - 用户ID
 * @param {Object} data - 用户数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateUser(id, data) {
  return request({
    url: `/users/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 * @param {number} id - 用户ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteUser(id) {
  return request({
    url: `/users/${id}`,
    method: 'delete'
  })
} 