<template>
  <div class="profile-container">
    <div class="page-header">
      <el-button @click="router.back()" :icon="ArrowLeft">返回</el-button>
    </div>
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span class="title">个人信息</span>
          <el-button type="primary" :icon="Edit" @click="handleEdit" v-if="!isEditing">
            编辑资料
          </el-button>
          <div v-else>
            <el-button type="success" :icon="Check" @click="handleSave" style="margin-right: 12px">
              保存
            </el-button>
            <el-button :icon="Close" @click="handleCancel">
              取消
            </el-button>
          </div>
        </div>
      </template>
      
      <div class="profile-content">
        <div class="avatar-container">
          <el-avatar :size="120" :src="userInfo?.avatar || defaultAvatar" class="avatar">
            {{ userInfo?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <el-upload
            v-if="isEditing"
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-button type="primary" class="change-avatar-btn">
              更换头像
            </el-button>
          </el-upload>
        </div>

        <div class="info-container">
          <el-form 
            ref="formRef"
            :model="formData" 
            :rules="rules"
            label-width="100px" 
            :disabled="!isEditing"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="formData.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入手机号码" />
            </el-form-item>
            <el-form-item label="个人简介" prop="bio">
              <el-input
                v-model="formData.bio"
                type="textarea"
                :rows="4"
                placeholder="请输入个人简介"
              />
            </el-form-item>
          </el-form>
        </div>

        <div class="stats-container">
          <div class="stat-item">
            <div class="stat-value">{{ userStats.borrowCount || 0 }}</div>
            <div class="stat-label">借阅次数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ userStats.currentBorrows || 0 }}</div>
            <div class="stat-label">当前借阅</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ userStats.overdueTimes || 0 }}</div>
            <div class="stat-label">逾期次数</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
import { Edit, Check, Close, ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const isEditing = ref(false)
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const userInfo = computed(() => userStore.userInfo)

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 用户统计数据
const userStats = reactive({
  borrowCount: 15,
  currentBorrows: 2,
  overdueTimes: 0
})

const formData = reactive({
  username: userInfo.value?.username || '',
  email: userInfo.value?.email || '',
  phone: userInfo.value?.phone || '',
  bio: userInfo.value?.bio || ''
})

const handleEdit = () => {
  isEditing.value = true
}

const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 调用store中的更新方法
    await userStore.updateUserInfo({
      ...formData,
      id: userInfo.value?.id
    })
    
    isEditing.value = false
    ElMessage.success('保存成功')
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('表单验证失败，请检查输入')
    }
  }
}

const handleCancel = () => {
  formRef.value?.resetFields()
  // 重置表单数据
  Object.assign(formData, {
    username: userInfo.value?.username || '',
    email: userInfo.value?.email || '',
    phone: userInfo.value?.phone || '',
    bio: userInfo.value?.bio || ''
  })
  isEditing.value = false
}

const handleAvatarSuccess = (res) => {
  if (res.code === 0) {
    userStore.updateAvatar(res.data.url)
    ElMessage.success('头像更新成功')
  }
}

const beforeAvatarUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJpgOrPng) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
  }
  return isJpgOrPng && isLt2M
}
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 24px;
  
  .page-header {
    margin-bottom: 20px;
    .el-button {
      padding: 8px 16px;
      font-size: 14px;
      
      .el-icon {
        margin-right: 6px;
      }
      
      &:hover {
        transform: translateX(-2px);
      }
    }
  }
  
  .profile-card {
    max-width: 800px;
    margin: 0 auto;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .title {
        font-size: 18px;
        font-weight: 600;
        background: linear-gradient(120deg, #1a6fc9, #6e48aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
    }
  }
  
  .profile-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 20px 0;
    
    .avatar-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      
      .avatar {
        border: 4px solid #fff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }
      }
      
      .change-avatar-btn {
        margin-top: 8px;
      }
    }
    
    .info-container {
      padding: 0 20px;
    }
    
    .stats-container {
      display: flex;
      justify-content: space-around;
      padding: 24px;
      background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
      border-radius: 8px;
      margin-top: 20px;
      
      .stat-item {
        text-align: center;
        padding: 16px 24px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .stat-value {
          font-size: 24px;
          font-weight: 600;
          color: #1a6fc9;
          margin-bottom: 8px;
        }
        
        .stat-label {
          font-size: 14px;
          color: #666;
        }
      }
    }
  }
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  
  &:hover {
    box-shadow: 0 0 0 1px #1a6fc9 inset;
  }
  
  &.is-focus {
    box-shadow: 0 0 0 1px #1a6fc9 inset;
  }
}
</style> 