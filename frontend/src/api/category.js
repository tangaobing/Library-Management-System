import request from '@/api/request'

/**
 * 获取分类列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getCategories(params = {}) {
  return request({
    url: '/categories',
    method: 'get',
    params: {
      ...params,
      tree: params.tree ? 'true' : 'false'
    }
  })
}

/**
 * 获取分类树
 * @returns {Promise} - 返回Promise对象
 */
export function getCategoryTree() {
  return request({
    url: '/categories',
    method: 'get',
    params: { tree: 'true' }
  })
}

/**
 * 获取分类详情
 * @param {number} id - 分类ID
 * @returns {Promise} - 返回Promise对象
 */
export function getCategory(id) {
  return request({
    url: `/categories/${id}`,
    method: 'get'
  })
}

/**
 * 创建分类
 * @param {Object} data - 分类数据
 * @returns {Promise} - 返回Promise对象
 */
export function createCategory(data) {
  return request({
    url: '/categories',
    method: 'post',
    data
  })
}

/**
 * 更新分类
 * @param {number} id - 分类ID
 * @param {Object} data - 分类数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateCategory(id, data) {
  return request({
    url: `/categories/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除分类
 * @param {number} id - 分类ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteCategory(id) {
  return request({
    url: `/categories/${id}`,
    method: 'delete'
  })
} 