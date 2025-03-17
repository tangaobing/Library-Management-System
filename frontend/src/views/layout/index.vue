<template>
  <div class="layout-container" :class="{ 'is-collapsed': isCollapse }">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="logo">
        <div class="logo-text-container" v-if="!isCollapse">
          <div class="logo-icon-left">
            <el-icon><Reading /></el-icon>
          </div>
          <h1 class="logo-title">
            <span class="logo-char" v-for="(char, index) in '图书管理系统'" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">{{ char }}</span>
          </h1>
          <div class="logo-underline"></div>
        </div>
        <div class="logo-icon" v-else>
          <el-icon><Reading /></el-icon>
        </div>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        :collapse="isCollapse"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <!-- 首页 -->
        <el-menu-item index="/dashboard">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        
        <!-- 图书管理 -->
        <el-menu-item index="/books">
          <el-icon><Reading /></el-icon>
          <span>图书管理</span>
        </el-menu-item>
        
        <!-- 分类管理 -->
        <el-menu-item index="/categories">
          <el-icon><Files /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        
        <!-- 借阅管理 -->
        <el-menu-item index="/borrows">
          <el-icon><Tickets /></el-icon>
          <span>借阅管理</span>
        </el-menu-item>
        
        <!-- 用户管理 -->
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <!-- 主要内容区域 -->
    <el-container class="main-container">
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-left">
          <div class="collapse-btn-wrapper" @click="toggleCollapse">
            <el-icon class="collapse-btn">
              <Expand v-if="isCollapse" />
              <Fold v-else />
            </el-icon>
            <span class="collapse-text">{{ isCollapse ? '展开菜单' : '收起菜单' }}</span>
          </div>
        </div>
        <div class="header-right">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="user-info">
              {{ userInfo?.username || '用户' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 内容区域 -->
      <el-main class="content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessageBox } from 'element-plus'
import { House, Reading, Files, Tickets, User, Expand, Fold, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 侧边栏折叠状态
const isCollapse = ref(false)

// 切换折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
  // 保存折叠状态到本地存储，以便刷新页面后保持状态
  localStorage.setItem('sidebarCollapsed', isCollapse.value ? '1' : '0')
}

// 用户信息
const userInfo = computed(() => userStore.userInfo)

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 处理下拉菜单命令
const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      router.push('/login')
    }).catch(() => {})
  } else if (command === 'profile') {
    router.push('/profile')
  }
}

// 监听窗口大小变化，在小屏幕上自动折叠侧边栏
const handleResize = () => {
  if (window.innerWidth < 768) {
    isCollapse.value = true
  }
}

// 组件挂载时检查用户信息和侧边栏状态
onMounted(async () => {
  if (userStore.token && !userStore.userInfo) {
    await userStore.fetchCurrentUser()
  }
  
  // 从本地存储中恢复侧边栏状态
  const savedCollapsed = localStorage.getItem('sidebarCollapsed')
  if (savedCollapsed !== null) {
    isCollapse.value = savedCollapsed === '1'
  }
  
  // 初始检查
  handleResize()
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize)
})

// 组件卸载时移除监听
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.layout-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  position: relative;
  background-color: #ffffff;
  
  &.is-collapsed {
    .sidebar {
      width: 48px !important;
    }
    
    .main-container {
      margin-left: 48px;
    }

    .logo {
      padding: 0 12px;
    }

    .logo-icon {
      font-size: 20px;
    }
  }
}

.sidebar {
  height: 100%;
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
  background-color: #304156;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  z-index: 100;
  flex-shrink: 0;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 200px;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 200px;
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
  height: 100vh;
}

.content {
  flex: 1;
  padding: 24px;
  background-color: #f5f7fa;
  height: calc(100vh - 60px);
  overflow-y: auto;
  overflow-x: hidden;
}

:deep(.el-main) {
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.header {
  position: relative;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: linear-gradient(135deg, #24243e 0%, #302b63 50%, #0f0c29 100%);
  overflow: hidden;
  z-index: 1;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    z-index: -1;
    animation: headerGlow 10s infinite alternate;
  }

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: -150%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transform: skewX(-25deg);
    animation: headerShine 6s infinite;
  }
  
  .header-left {
    position: relative;
    z-index: 2;
    .collapse-btn-wrapper {
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 8px 16px;
      border-radius: 8px;
      color: #ffffff;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(5px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .collapse-text {
        margin-left: 8px;
        font-size: 14px;
        background: linear-gradient(120deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 500;
      }

      .collapse-btn {
        font-size: 18px;
        color: #ffffff;
      }
    }
  }
  
  .header-right {
    position: relative;
    z-index: 2;
    .user-info {
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 6px 16px;
      border-radius: 8px;
      color: #ffffff;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(5px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }
      
      .el-icon {
        margin-left: 8px;
        font-size: 14px;
      }
    }
  }
}

@keyframes headerGlow {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

@keyframes headerShine {
  0% {
    left: -150%;
  }
  50% {
    left: 150%;
  }
  100% {
    left: 150%;
  }
}

/* Logo样式优化 */
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2b3648;
  overflow: hidden;
  position: relative;
  transition: all 0.3s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo-text-container {
  display: flex;
  align-items: center;
  padding: 0 16px;
  width: 100%;
}

.logo-icon-left {
  font-size: 20px;
  color: #409EFF;
  margin-right: 8px;
}

.logo-title {
  margin: 0;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
  display: flex;
}

.logo-char {
  display: inline-block;
  animation: logoCharFloat 0.3s ease-in-out both;
  opacity: 0;
}

.logo-underline {
  position: absolute;
  bottom: 0;
  left: 16px;
  right: 16px;
  height: 2px;
  background: linear-gradient(90deg, #409EFF, transparent);
}

.logo-icon {
  font-size: 24px;
  color: #409EFF;
}

/* 菜单样式优化 */
:deep(.el-menu) {
  border: none;
  padding: 0;
  width: 100% !important;
}

:deep(.el-menu--collapse) {
  width: 48px !important;
}

:deep(.el-menu-item) {
  margin: 0;
  border-radius: 0;
  height: 50px;
  line-height: 50px;
  padding: 0 12px !important;
  
  .el-icon {
    margin-right: 12px;
  }
  
  &:hover {
    background-color: #263445 !important;
  }
  
  &.is-active {
    background: linear-gradient(90deg, #1a6fc9, #6e48aa) !important;
    color: #ffffff !important;
    font-weight: bold;
    box-shadow: none;
    
    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 3px;
      background: #ffffff;
      box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
    }
    
    .el-icon {
      color: #ffffff !important;
    }
    
    span {
      color: #ffffff !important;
    }
  }
}

@keyframes logoCharFloat {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

// 响应式布局
@media screen and (max-width: 768px) {
  .layout-container {
    .sidebar {
      transform: translateX(0);
      transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1);
    }
    
    .main-container {
      margin-left: 0;
    }
    
    &.is-collapsed {
      .sidebar {
        transform: translateX(-64px);
      }
      
      .main-container {
        margin-left: 0;
      }
    }
  }
}
</style> 