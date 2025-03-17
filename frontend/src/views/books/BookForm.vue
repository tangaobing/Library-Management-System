<template>
  <div class="page-container">
    <div class="page-title">{{ isEdit ? '编辑图书' : '新增图书' }}</div>
    
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="book-form"
    >
      <el-form-item label="书名" prop="title">
        <el-input v-model="form.title" placeholder="请输入书名" />
      </el-form-item>
      
      <el-form-item label="作者" prop="author">
        <el-input v-model="form.author" placeholder="请输入作者" />
      </el-form-item>
      
      <el-form-item label="ISBN" prop="isbn">
        <div class="input-with-button">
          <el-input v-model="form.isbn" placeholder="请输入ISBN" />
          <el-button type="primary" link @click="fillExampleISBN">填入示例</el-button>
        </div>
        <div class="form-tip">
          ISBN格式必须是10位或13位数字。您可以输入带连字符的格式（如978-7-115-54608-1）或纯数字格式（如9787115546081），系统会自动处理。
        </div>
      </el-form-item>
      
      <el-form-item label="分类" prop="category_id">
        <el-select v-model="form.category_id" placeholder="请选择分类">
          <el-option
            v-for="item in categories"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="出版社" prop="publisher">
        <el-input v-model="form.publisher" placeholder="请输入出版社" />
      </el-form-item>
      
      <el-form-item label="出版日期" prop="publish_date">
        <el-date-picker
          v-model="form.publish_date"
          type="date"
          placeholder="选择出版日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      
      <el-form-item label="价格" prop="price">
        <el-input-number v-model="form.price" :min="0" />
      </el-form-item>
      
      <el-form-item label="状态" prop="status">
        <el-select v-model="form.status" placeholder="请选择状态">
          <el-option label="可借阅" value="available" />
          <el-option label="已借出" value="borrowed" />
          <el-option label="已预约" value="reserved" />
          <el-option label="丢失" value="lost" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="位置信息" prop="location">
        <el-input v-model="form.location" placeholder="请输入图书位置信息" />
      </el-form-item>
      
      <el-form-item label="封面URL" prop="cover_url">
        <el-input v-model="form.cover_url" placeholder="请输入图书封面URL" />
      </el-form-item>
      
      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="请输入图书描述"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBook, createBook, updateBook, checkIsbnExists } from '@/api/book'
import { getCategories } from '@/api/category'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)

// 判断是否为编辑模式
const isEdit = computed(() => !!route.params.id)

// 表单数据
const form = reactive({
  title: '',
  author: '',
  isbn: '',
  category_id: '',
  publisher: '',
  publish_date: '',
  price: null,
  location: '',
  description: '',
  status: 'available',
  cover_url: ''
})

// 保存原始ISBN，用于编辑时比较
const originalIsbn = ref('');

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入书名', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在1到100个字符', trigger: 'blur' }
  ],
  author: [
    { required: true, message: '请输入作者', trigger: 'blur' }
  ],
  isbn: [
    { required: true, message: '请输入ISBN', trigger: 'blur' },
    { 
      validator: async (rule, value, callback) => {
        if (!value) {
          callback();
          return;
        }
        
        // 移除所有连字符和空格
        const cleanedValue = value.replace(/[-\s]/g, '');
        
        // 检查是否为10位或13位数字
        if (!/^\d{10}$|^\d{13}$/.test(cleanedValue)) {
          callback(new Error('ISBN格式不正确，必须是10位或13位数字'));
          return;
        }
        
        // 自动格式化ISBN
        form.isbn = cleanedValue;
        
        try {
          // 如果是编辑模式，且ISBN没有变化，则不检查唯一性
          if (isEdit.value && originalIsbn.value === cleanedValue) {
            callback();
            return;
          }
          
          // 检查ISBN是否已存在
          const res = await checkIsbnExists(cleanedValue);
          if (res.data && res.data.exists) {
            callback(new Error('该ISBN已存在，请输入其他ISBN'));
          } else {
            callback();
          }
        } catch (error) {
          console.error('检查ISBN失败:', error);
          // 如果API调用失败，仍然允许提交，后端会再次验证
          callback();
        }
      }, 
      trigger: 'blur' 
    }
  ],
  category_id: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  publisher: [
    { required: true, message: '请输入出版社', trigger: 'blur' }
  ],
  publish_date: [
    { required: true, message: '请选择出版日期', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能小于0', trigger: 'blur' }
  ]
}

// 分类列表
const categories = ref([])

// 获取分类列表
const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
    ElMessage.error('获取分类列表失败')
  }
}

// 获取图书详情
const fetchBookDetail = async () => {
  try {
    const res = await getBook(route.params.id)
    
    // 只提取表单需要的字段
    const bookData = {
      title: res.data.title || '',
      author: res.data.author || '',
      isbn: res.data.isbn || '',
      category_id: res.data.category_id || '',
      publisher: res.data.publisher || '',
      publish_date: res.data.publish_date || '',
      price: res.data.price || null,
      location: res.data.location || '',
      description: res.data.description || '',
      status: res.data.status || 'available',
      cover_url: res.data.cover_url || ''
    };
    
    // 保存原始ISBN
    originalIsbn.value = res.data.isbn || '';
    
    // 将处理后的数据赋值给表单
    Object.assign(form, bookData)
  } catch (error) {
    console.error('获取图书详情失败:', error)
    ElMessage.error('获取图书详情失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 创建一个新对象，只包含后端需要的字段
        const apiData = {
          title: form.title,
          author: form.author,
          isbn: form.isbn || null,
          publisher: form.publisher || null,
          publish_date: form.publish_date ? form.publish_date.split('T')[0] : null,
          description: form.description || '',
          category_id: form.category_id || null,
          location: form.location || '',
          status: form.status || 'available',
          cover_url: form.cover_url || '',
          price: form.price || null
        };
        
        // 打印提交的数据，用于调试
        console.log('提交的图书数据:', apiData);
        
        if (isEdit.value) {
          await updateBook(route.params.id, apiData)
          ElMessage.success('更新成功')
        } else {
          await createBook(apiData)
          ElMessage.success('创建成功')
        }
        router.push('/books')
      } catch (error) {
        console.error('保存失败:', error)
        // 打印详细的错误信息
        if (error.response) {
          console.error('错误响应:', error.response.data)
          // 尝试解析错误消息
          let errorMsg = '保存失败';
          try {
            if (error.response.data.message) {
              // 尝试解析JSON字符串
              if (typeof error.response.data.message === 'string' && 
                  error.response.data.message.startsWith('{') && 
                  error.response.data.message.endsWith('}')) {
                const errorObj = JSON.parse(error.response.data.message.replace(/'/g, '"'));
                errorMsg = Object.entries(errorObj)
                  .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
                  .join('\n');
              } else {
                errorMsg = error.response.data.message;
              }
            }
          } catch (e) {
            console.error('解析错误消息失败:', e);
            errorMsg = error.response.data.message || '保存失败';
          }
          ElMessage.error(errorMsg);
        } else {
          ElMessage.error('保存失败')
        }
      }
    }
  })
}

// 取消
const handleCancel = () => {
  router.back()
}

// 填入示例ISBN
const fillExampleISBN = () => {
  form.isbn = '9787115546081'; // Python编程：从入门到实践
}

onMounted(() => {
  fetchCategories()
  if (isEdit.value) {
    fetchBookDetail()
  }
})
</script>

<style scoped>
.book-form {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  padding: 0 20px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.4;
}

.input-with-button {
  display: flex;
  align-items: center;
}

.input-with-button .el-input {
  flex: 1;
  margin-right: 10px;
}
</style> 