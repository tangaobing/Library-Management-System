<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">借阅管理</div>
      <div class="page-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>新增借阅
        </el-button>
      </div>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :model="searchForm" class="search-form" inline>
        <el-form-item label="图书名称">
          <el-input 
            v-model="searchForm.bookTitle" 
            placeholder="请输入图书名称" 
            clearable
          >
            <template #prefix>
              <el-icon><Reading /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="借阅人">
          <el-input 
            v-model="searchForm.userName" 
            placeholder="请输入借阅人" 
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="借阅状态">
          <el-radio-group v-model="searchForm.status">
            <el-radio label="">全部</el-radio>
            <el-radio label="borrowing">借阅中</el-radio>
            <el-radio label="returned">已归还</el-radio>
            <el-radio label="overdue">逾期</el-radio>
            <el-radio label="lost">丢失</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item class="search-actions">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><RefreshRight /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 表格 -->
    <div class="table-container">
      <div class="data-table">
        <el-table :data="borrows" style="width: 100%" border>
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="book_title" label="图书名称" align="left" />
          <el-table-column prop="username" label="借阅人" align="left" />
          <el-table-column prop="borrow_date" label="借阅日期" align="center">
            <template #default="scope">
              <el-tooltip 
                :content="formatFullDateTime(scope.row.borrow_date)" 
                placement="top" 
                effect="light"
              >
                <span>{{ formatShortDateTime(scope.row.borrow_date) }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="应还日期" align="center">
            <template #default="scope">
              <el-tooltip 
                :content="formatFullDateTime(scope.row.due_date)" 
                placement="top" 
                effect="light"
              >
                <span>{{ formatShortDateTime(scope.row.due_date) }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="return_date" label="实际归还日期" align="center">
            <template #default="scope">
              <el-tooltip 
                v-if="scope.row.return_date"
                :content="formatFullDateTime(scope.row.return_date)" 
                placement="top" 
                effect="light"
              >
                <span>{{ formatShortDateTime(scope.row.return_date) }}</span>
              </el-tooltip>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" align="center">
            <template #default="scope">
              <div class="status-tag" :class="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" align="left">
            <template #default="scope">
              <!-- 当有多个操作按钮时使用下拉菜单 -->
              <div v-if="hasMultipleActions(scope.row)" class="table-actions">
                <el-dropdown trigger="click">
                  <el-button type="primary" size="small">
                    <el-icon><More /></el-icon>操作
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-if="scope.row.status === 'borrowing' || scope.row.status === 'overdue'" @click="handleReturn(scope.row)">
                        <el-icon><Check /></el-icon> 归还
                      </el-dropdown-item>
                      <el-dropdown-item v-if="scope.row.status === 'overdue' && !scope.row.fine_paid" @click="handlePayFine(scope.row)">
                        <el-icon><Money /></el-icon> 缴纳罚款
                      </el-dropdown-item>
                      <el-dropdown-item @click="handleDelete(scope.row)">
                        <el-icon><Delete /></el-icon> 删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <!-- 当只有一个操作按钮时直接显示 -->
              <div v-else class="table-actions">
                <el-button 
                  v-if="scope.row.status === 'borrowing' || scope.row.status === 'overdue'" 
                  type="success" 
                  size="small" 
                  @click="handleReturn(scope.row)"
                >
                  <el-icon><Check /></el-icon>归还
                </el-button>
                <el-button 
                  v-if="scope.row.status === 'overdue' && !scope.row.fine_paid" 
                  type="warning" 
                  size="small" 
                  @click="handlePayFine(scope.row)"
                >
                  <el-icon><Money /></el-icon>缴纳罚款
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(scope.row)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新增借阅对话框 -->
    <el-dialog v-model="dialogVisible" title="新增借阅" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="图书" required>
          <div v-if="books.length > 0">
            <el-select 
              v-model="form.bookId" 
              placeholder="请选择图书" 
              style="width: 100%"
              filterable
            >
              <el-option 
                v-for="item in books" 
                :key="item.id" 
                :label="item.title" 
                :value="item.id" 
              />
            </el-select>
          </div>
          <div v-else class="empty-tip">暂无可借阅图书</div>
        </el-form-item>
        <el-form-item label="借阅人" required>
          <div v-if="users.length > 0">
            <el-select 
              v-model="form.userId" 
              placeholder="请选择借阅人" 
              style="width: 100%"
              filterable
            >
              <el-option 
                v-for="item in users" 
                :key="item.id" 
                :label="item.name" 
                :value="item.id" 
              />
            </el-select>
          </div>
          <div v-else class="empty-tip">暂无用户数据</div>
        </el-form-item>
        <el-form-item label="借阅日期">
          <el-date-picker v-model="form.borrowDate" type="date" placeholder="选择借阅日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="应还日期">
          <el-date-picker v-model="form.returnDate" type="date" placeholder="选择应还日期" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBorrows, borrowBook, returnBook, payFine, deleteBorrow } from '@/api/borrow'
import { getBooks } from '@/api/book'
import { getUsers } from '@/api/user'
import { ArrowDown, Check, Delete, Money, Plus, Search, RefreshRight, More, Reading, User } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = ref({
  bookTitle: '',
  userName: '',
  status: ''
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 借阅数据
const borrows = ref([])

// 图书列表
const books = ref([])

// 用户列表
const users = ref([])

// 对话框相关
const dialogVisible = ref(false)
const form = ref({
  bookId: null,
  userId: null,
  borrowDate: new Date(),
  returnDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000) // 默认14天后
})

// 获取借阅记录
const fetchBorrows = async () => {
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      book_title: searchForm.value.bookTitle,
      user_name: searchForm.value.userName,
      status: searchForm.value.status
    }
    const res = await getBorrows(params)
    borrows.value = res.data.borrows
    total.value = res.data.total
  } catch (error) {
    console.error('获取借阅记录失败:', error)
    ElMessage.error('获取借阅记录失败')
  }
}

// 获取图书列表
const fetchBooks = async () => {
  try {
    const res = await getBooks({ status: 'available' })
    books.value = res.data.books
  } catch (error) {
    console.error('获取图书列表失败:', error)
    ElMessage.error('获取图书列表失败')
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const res = await getUsers()
    users.value = res.data.users
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  }
}

// 获取状态类型
const getStatusType = (status) => {
  switch (status) {
    case 'borrowing':
      return 'primary'
    case 'returned':
      return 'success'
    case 'overdue':
      return 'danger'
    case 'lost':
      return 'warning'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'borrowing':
      return '借阅中'
    case 'returned':
      return '已归还'
    case 'overdue':
      return '逾期'
    case 'lost':
      return '丢失'
    default:
      return '未知'
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchBorrows()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    bookTitle: '',
    userName: '',
    status: ''
  }
  currentPage.value = 1
  fetchBorrows()
}

// 分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchBorrows()
}

// 当前页变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchBorrows()
}

// 添加借阅
const handleAdd = () => {
  form.value = {
    bookId: null,
    userId: null,
    borrowDate: new Date(),
    returnDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000) // 默认14天后
  }
  fetchBooks()
  fetchUsers()
  dialogVisible.value = true
}

// 归还图书
const handleReturn = (row) => {
  ElMessageBox.confirm(
    `确定要归还图书 "${row.book_title}" 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(async () => {
    try {
      await returnBook(row.id)
      ElMessage.success('归还成功')
      fetchBorrows()
    } catch (error) {
      console.error('归还图书失败:', error)
      ElMessage.error('归还图书失败')
    }
  }).catch(() => {
    // 取消归还
  })
}

// 缴纳罚款
const handlePayFine = (row) => {
  ElMessageBox.confirm(
    `确定要为图书 "${row.book_title}" 缴纳罚款吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await payFine(row.id)
      ElMessage.success('缴纳罚款成功')
      fetchBorrows()
    } catch (error) {
      console.error('缴纳罚款失败:', error)
      ElMessage.error('缴纳罚款失败')
    }
  }).catch(() => {
    // 取消缴纳
  })
}

// 删除借阅记录
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除该借阅记录吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteBorrow(row.id)
      ElMessage.success('删除成功')
      fetchBorrows()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 提交表单
const submitForm = async () => {
  try {
    await borrowBook({
      book_id: form.value.bookId,
      user_id: form.value.userId,
      borrow_date: form.value.borrowDate,
      return_date: form.value.returnDate
    })
    ElMessage.success('添加成功')
    dialogVisible.value = false
    fetchBorrows()
  } catch (error) {
    console.error('添加借阅记录失败:', error)
    ElMessage.error('添加借阅记录失败')
  }
}

// 判断是否有多个操作按钮
const hasMultipleActions = (row) => {
  let actionCount = 0;
  
  // 归还按钮
  if (row.status === 'borrowing' || row.status === 'overdue') {
    actionCount++;
  }
  
  // 缴纳罚款按钮
  if (row.status === 'overdue' && !row.fine_paid) {
    actionCount++;
  }
  
  // 删除按钮始终存在
  actionCount++;
  
  return actionCount > 1;
}

// 格式化完整日期时间
const formatFullDateTime = (dateString) => {
  if (!dateString) return '暂无数据'
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 格式化简短日期时间
const formatShortDateTime = (dateString) => {
  if (!dateString) return '暂无数据'
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 组件挂载时获取数据
onMounted(() => {
  fetchBorrows()
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.table-container {
  background-color: white;
  border-radius: $border-radius-base;
  padding: $spacing-medium;
  box-shadow: $box-shadow-light;
  margin-bottom: $spacing-large;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  
  &.primary {
    background-color: rgba($primary-color, 0.1);
    color: $primary-color;
  }
  
  &.success {
    background-color: rgba($success, 0.1);
    color: $success;
  }
  
  &.warning {
    background-color: rgba($warning, 0.1);
    color: $warning;
  }
  
  &.info {
    background-color: rgba($info, 0.1);
    color: $info;
  }
  
  &.danger {
    background-color: rgba($danger, 0.1);
    color: $danger;
  }
}

.table-actions {
  display: flex;
  gap: $spacing-small;
  justify-content: flex-start;
  
  .el-button {
    padding: $spacing-extra-small $spacing-small;
    min-width: 50px;
    margin-left: 0;
  }
}

.empty-tip {
  color: $text-secondary;
  font-size: $font-size-base;
  padding: $spacing-base 0;
}

/* 修复选择框显示问题 */
:deep(.el-select .el-input__inner) {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

/* 调整单选按钮组的样式 */
:deep(.el-radio-group) {
  display: flex;
  flex-wrap: wrap;
}

:deep(.el-radio) {
  margin-right: $spacing-medium;
  margin-bottom: $spacing-small;
}

:deep(.el-dialog) {
  border-radius: $border-radius-large;
  overflow: hidden;
  
  .el-dialog__header {
    background-color: $bg-base;
    padding: $spacing-medium $spacing-large;
    
    .el-dialog__title {
      font-weight: $font-weight-bold;
      color: $text-primary;
    }
  }
  
  .el-dialog__body {
    padding: $spacing-large;
  }
  
  .el-dialog__footer {
    padding: $spacing-medium $spacing-large;
    border-top: 1px solid $border-lighter;
  }
}
</style> 