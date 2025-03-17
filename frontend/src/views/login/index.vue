<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-title">
        <h2>图书管理系统</h2>
      </div>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            :loading="loading"
            type="primary"
            class="login-button"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <!-- 测试账号提示 -->
        <div class="test-account">
          <p>测试账号：</p>
          <p>管理员：admin / admin123</p>
          <p>普通用户：user / user123</p>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 登录表单引用
const loginFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      console.log('开始登录...')
      await userStore.login(loginForm.username, loginForm.password)
      console.log('登录成功，准备跳转')
      ElMessage.success('登录成功')
      
      // 如果有重定向地址，则跳转到重定向地址
      const redirect = route.query.redirect || '/dashboard'
      console.log('跳转到:', redirect)
      
      // 使用replace而不是push，避免浏览器历史记录中出现登录页
      router.replace(redirect)
    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error(error.message || '登录失败，请检查用户名和密码')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style lang="scss" scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  
  .login-box {
    width: 350px;
    padding: 30px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    
    .login-title {
      text-align: center;
      margin-bottom: 30px;
      
      h2 {
        font-size: 24px;
        color: #303133;
      }
    }
    
    .login-form {
      .login-button {
        width: 100%;
      }
    }
    
    .test-account {
      margin-top: 20px;
      font-size: 12px;
      color: #909399;
      
      p {
        margin: 5px 0;
      }
    }
  }
}
</style> 