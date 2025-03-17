<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">图书管理</div>
      <div class="page-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>添加图书
        </el-button>
      </div>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form class="search-form" :model="searchForm" inline>
        <el-form-item>
          <el-input
            v-model="searchForm.search"
            placeholder="搜索图书名称、作者、ISBN"
            clearable
            style="width: 300px;"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-select
            v-model="searchForm.category_id"
            placeholder="选择分类"
            clearable
            style="width: 200px;"
          >
            <el-option
              v-for="item in categories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select
            v-model="searchForm.status"
            placeholder="图书状态"
            clearable
            style="width: 150px;"
          >
            <el-option label="可借阅" value="available" />
            <el-option label="已借出" value="borrowed" />
            <el-option label="已预约" value="reserved" />
            <el-option label="丢失" value="lost" />
          </el-select>
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
        <el-table
          v-loading="loading"
          :data="bookList"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="书名" min-width="150" show-overflow-tooltip />
          <el-table-column prop="author" label="作者" min-width="120" show-overflow-tooltip />
          <el-table-column prop="isbn" label="ISBN" width="120" show-overflow-tooltip />
          <el-table-column prop="category_name" label="分类" width="120" />
          <el-table-column prop="publisher" label="出版社" min-width="150" show-overflow-tooltip />
          <el-table-column prop="publish_date" label="出版日期" width="120" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <div class="status-tag" :class="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="left">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button
                  type="primary"
                  size="small"
                  @click="handleEdit(row)"
                >
                  <el-icon><Edit /></el-icon>编辑
                </el-button>
                <el-dropdown trigger="click">
                  <el-button size="small">
                    <el-icon><More /></el-icon>更多
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-if="row.status === 'available'" @click="handleBorrow(row)">
                        <el-icon><Promotion /></el-icon>借阅
                      </el-dropdown-item>
                      <el-dropdown-item @click="handleDelete(row)">
                        <el-icon><Delete /></el-icon>删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.per_page"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    
    <!-- 借阅对话框 -->
    <el-dialog
      v-model="borrowDialogVisible"
      title="借阅图书"
      width="500px"
    >
      <el-form
        ref="borrowFormRef"
        :model="borrowForm"
        :rules="borrowRules"
        label-width="100px"
      >
        <el-form-item label="图书名称">
          <span>{{ selectedBook?.title }}</span>
        </el-form-item>
        <el-form-item label="借阅人" prop="user_id" v-if="showUserSelect">
          <el-select
            v-model="borrowForm.user_id"
            placeholder="请选择借阅人"
            filterable
          >
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="user.name || user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="借阅天数" prop="borrow_days">
          <el-input-number
            v-model="borrowForm.borrow_days"
            :min="1"
            :max="30"
          />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="borrowForm.remarks"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="borrowDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitBorrow">确认借阅</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBooks, deleteBook } from '@/api/book'
import { getCategories } from '@/api/category'
import { borrowBook } from '@/api/borrow'
import { getUsers } from '@/api/user'
import { Plus, Edit, Delete, Search, RefreshRight, More, Promotion } from '@element-plus/icons-vue'

const router = useRouter()

// 加载状态
const loading = ref(false)

// 图书列表
const bookList = ref([])

// 分类列表
const categories = ref([])

// 用户列表
const userList = ref([])

// 是否显示用户选择
const showUserSelect = ref(true)

// 搜索表单
const searchForm = reactive({
  search: '',
  category_id: '',
  status: ''
})

// 分页信息
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0
})

// 借阅对话框
const borrowDialogVisible = ref(false)
const borrowFormRef = ref(null)
const selectedBook = ref(null)
const borrowForm = reactive({
  book_id: '',
  user_id: '',
  borrow_days: 14,
  remarks: ''
})
const borrowRules = {
  user_id: [
    { required: true, message: '请选择借阅人', trigger: 'change' }
  ],
  borrow_days: [
    { required: true, message: '请输入借阅天数', trigger: 'blur' },
    { type: 'number', min: 1, max: 30, message: '借阅天数应为1-30天', trigger: 'blur' }
  ]
}

// 获取图书列表
const fetchBooks = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      ...searchForm
    }
    
    const res = await getBooks(params)
    bookList.value = res.data.books
    pagination.total = res.data.total
  } catch (error) {
    console.error('获取图书列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const res = await getUsers()
    userList.value = res.data.users
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchBooks()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.page = 1
  fetchBooks()
}

// 添加图书
const handleAdd = () => {
  console.log('点击添加图书按钮')
  router.push('/books/add')
}

// 编辑图书
const handleEdit = (row) => {
  router.push(`/books/edit/${row.id}`)
}

// 删除图书
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除图书《${row.title}》吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteBook(row.id)
      ElMessage.success('删除成功')
      fetchBooks()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 借阅图书
const handleBorrow = (row) => {
  selectedBook.value = row
  borrowForm.book_id = row.id
  borrowForm.user_id = ''
  borrowDialogVisible.value = true
  fetchUsers()
}

// 提交借阅
const submitBorrow = () => {
  borrowFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      await borrowBook(borrowForm)
      ElMessage.success('借阅成功')
      borrowDialogVisible.value = false
      fetchBooks()
    } catch (error) {
      console.error('借阅图书失败:', error)
    }
  })
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.per_page = size
  fetchBooks()
}

// 页码变化
const handleCurrentChange = (page) => {
  pagination.page = page
  fetchBooks()
}

// 获取状态类型
const getStatusType = (status) => {
  const map = {
    available: 'success',
    borrowed: 'warning',
    reserved: 'info',
    lost: 'danger'
  }
  return map[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const map = {
    available: '可借阅',
    borrowed: '已借出',
    reserved: '已预约',
    lost: '丢失'
  }
  return map[status] || status
}

// 组件挂载时获取数据
onMounted(() => {
  fetchBooks()
  fetchCategories()
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.page-container {
  background-color: transparent;
}

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
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: $spacing-large;
  background-color: white;
  padding: $spacing-medium;
  border-radius: $border-radius-base;
  box-shadow: $box-shadow-light;
}
</style> 