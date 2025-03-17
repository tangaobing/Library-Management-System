import request from './request'

/**
 * 获取借阅记录列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getBorrows(params) {
  return request({
    url: '/borrows',
    method: 'get',
    params
  })
}

/**
 * 获取借阅记录详情
 * @param {number} id - 借阅记录ID
 * @returns {Promise} - 返回Promise对象
 */
export function getBorrow(id) {
  return request({
    url: `/borrows/${id}`,
    method: 'get'
  })
}

/**
 * 借阅图书
 * @param {Object} data - 借阅数据
 * @returns {Promise} - 返回Promise对象
 */
export function borrowBook(data) {
  return request({
    url: '/borrows',
    method: 'post',
    data
  })
}

/**
 * 归还图书
 * @param {number} id - 借阅记录ID
 * @param {boolean} isLost - 是否丢失
 * @returns {Promise} - 返回Promise对象
 */
export function returnBook(id, isLost = false) {
  return request({
    url: `/borrows/${id}/return`,
    method: 'post',
    data: { is_lost: isLost }
  })
}

/**
 * 支付罚款
 * @param {number} borrowId - 借阅记录ID
 * @returns {Promise} - 返回Promise对象
 */
export function payFine(borrowId) {
  return request({
    url: '/borrows/pay-fine',
    method: 'post',
    data: { borrow_id: borrowId }
  })
}

/**
 * 检查逾期借阅
 * @returns {Promise} - 返回Promise对象
 */
export function checkOverdue() {
  return request({
    url: '/borrows/check-overdue',
    method: 'post'
  })
}

/**
 * 删除借阅记录
 * @param {number} id - 借阅记录ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteBorrow(id) {
  return request({
    url: `/borrows/${id}`,
    method: 'delete'
  })
} 