import request from './request'

/**
 * 获取图书列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getBooks(params) {
  return request({
    url: '/books',
    method: 'get',
    params
  })
}

/**
 * 检查ISBN是否已存在
 * @param {string} isbn - ISBN编号
 * @returns {Promise} - 返回Promise对象
 */
export function checkIsbnExists(isbn) {
  return request({
    url: '/books/check-isbn',
    method: 'get',
    params: { isbn }
  })
}

/**
 * 获取图书详情
 * @param {number} id - 图书ID
 * @returns {Promise} - 返回Promise对象
 */
export function getBook(id) {
  return request({
    url: `/books/${id}`,
    method: 'get'
  })
}

/**
 * 创建图书
 * @param {Object} data - 图书数据
 * @returns {Promise} - 返回Promise对象
 */
export function createBook(data) {
  return request({
    url: '/books',
    method: 'post',
    data
  })
}

/**
 * 更新图书
 * @param {number} id - 图书ID
 * @param {Object} data - 图书数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateBook(id, data) {
  return request({
    url: `/books/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除图书
 * @param {number} id - 图书ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteBook(id) {
  return request({
    url: `/books/${id}`,
    method: 'delete'
  })
} 