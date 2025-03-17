<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">分类管理</div>
      <div class="page-actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>添加分类
        </el-button>
      </div>
    </div>
    
    <div class="table-container">
      <div class="data-table">
        <el-table 
          :data="categories" 
          style="width: 100%" 
          row-key="id" 
          border 
          default-expand-all
        >
          <el-table-column prop="name" label="分类名称" />
          <el-table-column prop="code" label="分类编码" />
          <el-table-column prop="description" label="描述" />
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
      </div>
    </div>

    <!-- 添加/编辑分类对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogType === 'add' ? '添加分类' : '编辑分类'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="父级分类">
          <div v-if="parentCategories.length > 0">
            <el-radio-group v-model="form.parentId">
              <el-radio :value="0" label="无父级分类" />
              <el-radio 
                v-for="item in parentCategories" 
                :key="item.id" 
                :value="item.id"
                :label="item.name"
              />
            </el-radio-group>
          </div>
          <div v-else>
            <el-radio-group v-model="form.parentId">
              <el-radio :value="0" label="无父级分类" />
            </el-radio-group>
          </div>
        </el-form-item>
        <el-form-item label="分类名称">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="分类编码">
          <el-input v-model="form.code" placeholder="请输入分类编码" />
          <div class="form-tip">分类编码必须唯一，可以留空</div>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="请输入描述" />
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
import { getCategories, getCategory, createCategory, updateCategory, deleteCategory } from '@/api/category'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'

// 分类数据
const categories = ref([])

// 父级分类列表
const parentCategories = ref([])

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' 或 'edit'
const form = ref({
  id: null,
  name: '',
  code: '',
  description: '',
  parentId: 0
})

// 获取分类列表
const fetchCategories = async () => {
  try {
    const res = await getCategories({ tree: true })
    
    // 将后端返回的数据转换为前端需要的格式
    const transformCategory = (category) => {
      const result = {
        id: category.id,
        name: category.name,
        code: category.code,
        description: category.description,
        parentId: category.parent_id,
        level: category.level,
        sortOrder: category.sort_order,
        createdAt: category.created_at,
        updatedAt: category.updated_at
      };
      
      if (category.children && category.children.length > 0) {
        result.children = category.children.map(transformCategory);
      }
      
      return result;
    };
    
    categories.value = res.data.map(transformCategory);
    
    // 提取父级分类
    const parents = categories.value.filter(item => !item.parentId);
    parentCategories.value = parents;
  } catch (error) {
    console.error('获取分类列表失败:', error)
    ElMessage.error('获取分类列表失败')
  }
}

// 添加分类
const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    id: null,
    name: '',
    code: '',
    description: '',
    parentId: 0
  }
  dialogVisible.value = true
}

// 编辑分类
const handleEdit = async (row) => {
  dialogType.value = 'edit'
  try {
    const res = await getCategory(row.id)
    // 将后端返回的下划线命名法转换为前端的驼峰命名法
    form.value = {
      id: res.data.id,
      name: res.data.name,
      code: res.data.code,
      description: res.data.description,
      parentId: res.data.parent_id || 0, // 如果parent_id为null，则设置为0
      sortOrder: res.data.sort_order
    }
    dialogVisible.value = true
  } catch (error) {
    console.error('获取分类详情失败:', error)
    ElMessage.error('获取分类详情失败')
  }
}

// 删除分类
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除分类 "${row.name}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteCategory(row.id)
      ElMessage.success('删除成功')
      fetchCategories()
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
    // 基本验证
    if (!form.value.name) {
      ElMessage.warning('请输入分类名称');
      return;
    }
    
    // 创建一个新对象，避免直接修改form.value
    const categoryData = { ...form.value };
    
    // 如果parentId为0，将其设置为null
    if (categoryData.parentId === 0) {
      categoryData.parentId = null;
    }
    
    // 将驼峰命名法转换为下划线命名法
    const apiData = {
      name: categoryData.name,
      code: categoryData.code || null, // 如果code为空字符串，则设置为null
      description: categoryData.description || '',
      parent_id: categoryData.parentId,
      sort_order: categoryData.sortOrder || 0
    };
    
    // 打印提交的数据，用于调试
    console.log('提交的分类数据:', apiData);
    
    if (dialogType.value === 'add') {
      await createCategory(apiData)
      ElMessage.success('添加成功')
    } else {
      await updateCategory(categoryData.id, apiData)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    fetchCategories()
  } catch (error) {
    console.error('保存分类失败:', error)
    // 打印详细的错误信息
    if (error.response) {
      console.error('错误响应:', error.response.data)
      const errorMsg = error.response.data.message || '保存分类失败';
      ElMessage.error(errorMsg);
    } else {
      ElMessage.error('保存分类失败');
    }
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCategories()
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

.table-actions {
  display: flex;
  gap: $spacing-small;
}

.form-tip {
  font-size: $font-size-extra-small;
  color: $text-secondary;
  margin-top: $spacing-extra-small;
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