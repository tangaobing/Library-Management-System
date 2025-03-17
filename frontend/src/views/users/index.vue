<template>
  <div class="page-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">用户管理</h2>
      <div class="page-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>添加用户
        </el-button>
      </div>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :inline="true" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="searchForm.role">
            <el-radio label="">全部</el-radio>
            <el-radio label="admin">管理员</el-radio>
            <el-radio label="librarian">图书管理员</el-radio>
            <el-radio label="reader">读者</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 数据表格 -->
    <div class="table-container">
      <el-table :data="users" class="data-table" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="username" label="用户名" align="left" />
        <el-table-column prop="name" label="姓名" align="left" />
        <el-table-column prop="email" label="邮箱" align="left" />
        <el-table-column prop="phone" label="电话" align="left" />
        <el-table-column prop="role" label="角色" align="center">
          <template #default="scope">
            <el-tag :type="getRoleTagType(scope.row.role)">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" align="center">
          <template #default="scope">
            <el-tooltip 
              :content="formatFullDateTime(scope.row.created_at)" 
              placement="top" 
              effect="light"
            >
              <span>{{ formatShortDateTime(scope.row.created_at) }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="left">
          <template #default="scope">
            <div class="table-actions">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row)">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
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
    </div>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogType === 'add' ? '添加用户' : '编辑用户'" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="form.role">
            <el-radio label="admin">管理员</el-radio>
            <el-radio label="librarian">图书管理员</el-radio>
            <el-radio label="reader">读者</el-radio>
          </el-radio-group>
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
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, getUser, createUser, updateUser, deleteUser } from '@/api/user'
import { Plus, Edit, Delete, Search, Refresh } from '@element-plus/icons-vue'

// 表单引用
const formRef = ref(null)

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' 或 'edit'
const form = ref({
  id: null,
  username: '',
  name: '',
  password: '',
  email: '',
  phone: '',
  role: 'reader'
})

// 表单验证规则
const rules = computed(() => ({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应在3到50个字符之间', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { max: 50, message: '姓名长度不能超过50个字符', trigger: 'blur' }
  ],
  password: [
    { required: dialogType.value === 'add', message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}))

// 搜索表单
const searchForm = ref({
  username: '',
  name: '',
  role: ''
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 用户数据
const users = ref([])

// 获取用户列表
const fetchUsers = async () => {
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      username: searchForm.value.username,
      name: searchForm.value.name,
      role: searchForm.value.role
    }
    
    console.log('搜索参数:', params)
    
    const res = await getUsers(params)
    users.value = res.data.users
    total.value = res.data.total
    
    console.log('获取到的用户数据:', res.data)
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败: ' + (error.response?.data?.message || error.message))
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    username: '',
    name: '',
    role: ''
  }
  currentPage.value = 1
  fetchUsers()
}

// 分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchUsers()
}

// 当前页变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchUsers()
}

// 添加用户
const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    id: null,
    username: '',
    name: '',
    password: '',
    email: '',
    phone: '',
    role: 'reader'
  }
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = async (row) => {
  dialogType.value = 'edit'
  try {
    const res = await getUser(row.id)
    console.log('获取到的用户详情:', res.data)
    
    // 确保所有必要的字段都存在
    form.value = {
      id: res.data.id,
      username: res.data.username || '',
      name: res.data.name || '',
      password: '', // 清空密码字段
      email: res.data.email || '',
      phone: res.data.phone || '',
      role: res.data.role || 'reader'
    }
    
    dialogVisible.value = true
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败: ' + (error.response?.data?.message || error.message))
  }
}

// 删除用户
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${row.name}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      fetchUsers()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败: ' + (error.response?.data?.message || error.message))
    }
  }).catch(() => {
    // 取消删除
  })
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    // 表单验证
    await formRef.value.validate()
    
    // 准备提交的数据
    const submitData = { ...form.value }
    console.log('原始表单数据:', submitData)
    
    // 如果是编辑模式且密码为空，则删除密码字段
    if (dialogType.value === 'edit' && !submitData.password) {
      delete submitData.password
    }
    
    // 删除id字段，因为后端API不接受此字段
    if (dialogType.value === 'edit') {
      const userId = submitData.id
      delete submitData.id
      
      // 删除其他可能不需要的字段
      delete submitData.created_at
      delete submitData.updated_at
      delete submitData.last_login
      
      console.log('提交的用户数据(编辑):', submitData)
      console.log('用户ID:', userId)
      
      await updateUser(userId, submitData)
      ElMessage.success('更新成功')
    } else {
      // 添加用户时也删除id字段
      delete submitData.id
      
      console.log('提交的用户数据(添加):', submitData)
      await createUser(submitData)
      ElMessage.success('添加成功')
    }
    
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    if (error.response) {
      console.error('保存用户失败:', error.response)
      console.error('错误详情:', error.response.data)
      ElMessage.error('保存用户失败: ' + (error.response.data.message || error.message))
    } else if (!error.message) {
      // 表单验证错误，不需要额外提示
      console.log('表单验证未通过')
    } else {
      console.error('保存用户失败:', error)
      ElMessage.error('保存用户失败: ' + error.message)
    }
  }
}

// 获取角色标签类型
const getRoleTagType = (role) => {
  switch (role) {
    case 'admin':
      return 'danger'
    case 'librarian':
      return 'warning'
    case 'reader':
      return 'primary'
    default:
      return 'info'
  }
}

// 获取角色文本
const getRoleText = (role) => {
  switch (role) {
    case 'admin':
      return '管理员'
    case 'librarian':
      return '图书管理员'
    case 'reader':
      return '读者'
    default:
      return '未知'
  }
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
  fetchUsers()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 10px;
}

.search-bar {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-start;
}

.search-buttons {
  margin-left: auto;
}

.table-container {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.data-table {
  flex: 1;
  margin-bottom: 20px;
}

.table-actions {
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  justify-content: flex-start;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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
  margin-right: 15px;
  margin-bottom: 5px;
}

/* 对话框样式 */
:deep(.el-dialog__header) {
  border-bottom: 1px solid #f0f0f0;
  padding: 15px 20px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}

:deep(.el-dialog__footer) {
  border-top: 1px solid #f0f0f0;
  padding: 15px 20px;
}
</style> 