<template>
  <div class="dashboard-container">
    <!-- 粒子背景效果 -->
    <div class="particles-container">
      <div v-for="i in 20" :key="i" class="particle"></div>
    </div>
    
    <!-- 波浪背景效果 -->
    <div class="wave-container">
      <div class="wave wave1"></div>
      <div class="wave wave2"></div>
      <div class="wave wave3"></div>
    </div>

    <div class="welcome-section">
      <h1 class="gradient-text">欢迎使用图书管理系统</h1>
      <div class="typewriter-container">
        <span class="typewriter-text">高效管理您的图书资源，提升阅读体验</span>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-container">
      <div class="stat-item book-stat">
        <div class="stat-icon-wrapper">
          <el-icon class="stat-icon"><Reading /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-title">图书总数</div>
          <div class="stat-value">{{ statistics.bookCount }}</div>
          <div class="stat-progress">
            <div class="progress-bar" :style="{ width: `${Math.min(statistics.bookCount / 10, 100)}%` }"></div>
          </div>
        </div>
      </div>
      
      <div class="stat-item borrow-stat">
        <div class="stat-icon-wrapper">
          <el-icon class="stat-icon"><Tickets /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-title">借阅总数</div>
          <div class="stat-value">{{ statistics.borrowCount }}</div>
          <div class="stat-progress">
            <div class="progress-bar" :style="{ width: `${Math.min(statistics.borrowCount / 10, 100)}%` }"></div>
          </div>
        </div>
      </div>
      
      <div class="stat-item user-stat">
        <div class="stat-icon-wrapper">
          <el-icon class="stat-icon"><User /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-title">用户总数</div>
          <div class="stat-value">{{ statistics.userCount }}</div>
          <div class="stat-progress">
            <div class="progress-bar" :style="{ width: `${Math.min(statistics.userCount / 10, 100)}%` }"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="data-cards-container">
      <el-row :gutter="10" class="mt-20">
        <el-col :span="12">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <div class="section-title-container">
                  <div class="section-title-icon">
                    <el-icon><Tickets /></el-icon>
                  </div>
                  <div class="section-title-wrapper">
                    <span class="section-title">最近借阅</span>
                    <div class="section-title-decoration"></div>
                  </div>
                </div>
                <div class="card-actions">
                  <el-input
                    v-model="borrowSearch"
                    placeholder="搜索图书/借阅人"
                    prefix-icon="Search"
                    clearable
                    @input="filterBorrows"
                    class="search-input"
                  />
                  <el-button
                    class="refresh-button"
                    circle
                    @click="handleRefresh"
                    :loading="borrowLoading"
                  >
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
            <div class="table-wrapper">
              <el-table 
                :data="paginatedBorrows" 
                stripe 
                style="width: 100%"
                :height="400"
                v-loading="borrowLoading"
                empty-text="暂无借阅记录"
              >
                <el-table-column prop="bookTitle" label="图书名称" min-width="120" show-overflow-tooltip />
                <el-table-column prop="userName" label="借阅人" width="100" />
                <el-table-column prop="borrowDate" label="借阅日期" width="100" />
                <el-table-column label="状态" width="80" fixed="right">
                  <template #default="scope">
                    <el-tag :type="getBorrowStatusType(scope.row.status || 'borrowing')">
                      {{ getBorrowStatusText(scope.row.status || 'borrowing') }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="borrowCurrentPage"
                  :page-size="borrowPageSize"
                  layout="prev, pager, next, jumper"
                  :total="filteredBorrows.length"
                  @current-change="handleBorrowPageChange"
                  background
                  hide-on-single-page
                />
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover" class="data-card">
            <template #header>
              <div class="card-header">
                <div class="section-title-container">
                  <div class="section-title-icon">
                    <el-icon><Reading /></el-icon>
                  </div>
                  <div class="section-title-wrapper">
                    <span class="section-title">热门图书</span>
                    <div class="section-title-decoration"></div>
                  </div>
                </div>
                <div class="card-actions">
                  <el-input
                    v-model="bookSearch"
                    placeholder="搜索图书"
                    prefix-icon="Search"
                    clearable
                    @input="filterBooks"
                    class="search-input"
                  />
                  <div class="sort-group">
                    <span class="sort-label">借阅次数</span>
                    <el-button
                      :type="currentSortOrder === 'count-desc' ? 'primary' : ''"
                      @click="handleSort"
                    >
                      <el-icon><Sort /></el-icon>
                      <span>排序</span>
                    </el-button>
                  </div>
                </div>
              </div>
            </template>
            <div class="table-wrapper">
              <el-table 
                :data="paginatedBooks" 
                stripe 
                style="width: 100%"
                :height="400"
                v-loading="bookLoading"
                empty-text="暂无热门图书数据"
              >
                <el-table-column prop="title" label="图书名称" min-width="120" show-overflow-tooltip />
                <el-table-column prop="category" label="分类" width="100">
                  <template #default="scope">
                    <el-tag 
                      :type="scope.row.category ? 'success' : 'info'"
                      effect="plain"
                    >
                      {{ scope.row.category || '待分类' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="借阅热度" width="160" fixed="right">
                  <template #default="scope">
                    <div class="heat-info">
                      <div class="heat-count">
                        <span class="count-number">{{ scope.row.borrowCount }}</span>
                        <span class="count-label">次借阅</span>
                      </div>
                      <div class="heat-bar-container">
                        <div 
                          class="heat-bar" 
                          :style="{ 
                            width: `${getHeatPercentage(scope.row.borrowCount)}%`,
                            backgroundColor: getHeatColor(scope.row.borrowCount)
                          }"
                        ></div>
                      </div>
                      <div class="heat-level">{{ getHeatLevel(scope.row.borrowCount) }}</div>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="bookCurrentPage"
                  :page-size="bookPageSize"
                  layout="prev, pager, next, jumper"
                  :total="filteredBooks.length"
                  @current-change="handleBookPageChange"
                  background
                  hide-on-single-page
                />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Reading, Tickets, User, Search, Refresh, Sort } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 统计数据
const statistics = ref({
  bookCount: 0,
  borrowCount: 0,
  userCount: 0
})

// 最近借阅
const recentBorrows = ref([])
const borrowSearch = ref('')
const filteredBorrows = ref([])
const borrowCurrentPage = ref(1)
const borrowPageSize = ref(5)
const borrowLoading = ref(false)

// 热门图书
const popularBooks = ref([])
const bookSearch = ref('')
const filteredBooks = ref([])
const bookCurrentPage = ref(1)
const bookPageSize = ref(5)
const bookLoading = ref(false)
const currentSortOrder = ref('count-desc')

// 获取统计数据
const fetchDashboardData = async () => {
  try {
    const [statsRes, recentRes, popularRes] = await Promise.all([
      axios.get('/api/dashboard/statistics'),
      axios.get('/api/dashboard/recent-borrows'),
      axios.get('/api/dashboard/popular-books')
    ])
    
    // 更新统计数据
    statistics.value = statsRes.data
    
    // 更新最近借阅
    recentBorrows.value = recentRes.data
    
    // 更新热门图书
    popularBooks.value = popularRes.data
  } catch (error) {
    console.error('获取仪表盘数据失败：', error)
    ElMessage.error('获取数据失败，请稍后重试')
  }
}

// 筛选借阅记录
const filterBorrows = () => {
  if (!borrowSearch.value) {
    filteredBorrows.value = [...recentBorrows.value]
  } else {
    const searchTerm = borrowSearch.value.toLowerCase()
    filteredBorrows.value = recentBorrows.value.filter(
      item => item.bookTitle.toLowerCase().includes(searchTerm) || 
             item.userName.toLowerCase().includes(searchTerm)
    )
  }
  borrowCurrentPage.value = 1
}

// 筛选图书
const filterBooks = () => {
  if (!bookSearch.value) {
    filteredBooks.value = [...popularBooks.value]
  } else {
    const searchTerm = bookSearch.value.toLowerCase()
    filteredBooks.value = popularBooks.value.filter(
      item => item.title.toLowerCase().includes(searchTerm)
    )
  }
  bookCurrentPage.value = 1
  sortBooks(currentSortOrder.value)
}

// 排序图书
const sortBooks = (order) => {
  currentSortOrder.value = order
  
  if (!filteredBooks.value.length) return
  
  filteredBooks.value.sort((a, b) => {
    if (order === 'count-desc') {
      return b.borrowCount - a.borrowCount
    }
    return a.borrowCount - b.borrowCount
  })
}

// 修改刷新功能
const handleRefresh = async () => {
  borrowLoading.value = true
  try {
    await fetchDashboardData()
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    borrowLoading.value = false
  }
}

// 修改排序功能
const handleSort = () => {
  currentSortOrder.value = currentSortOrder.value === 'count-desc' ? 'count-asc' : 'count-desc'
  sortBooks(currentSortOrder.value)
}

// 处理借阅分页
const handleBorrowPageChange = (page) => {
  borrowCurrentPage.value = page
}

// 处理图书分页
const handleBookPageChange = (page) => {
  bookCurrentPage.value = page
}

// 计算分页后的借阅记录
const paginatedBorrows = computed(() => {
  const start = (borrowCurrentPage.value - 1) * borrowPageSize.value
  const end = start + borrowPageSize.value
  return filteredBorrows.value.slice(start, end)
})

// 计算分页后的图书
const paginatedBooks = computed(() => {
  const start = (bookCurrentPage.value - 1) * bookPageSize.value
  const end = start + bookPageSize.value
  return filteredBooks.value.slice(start, end)
})

// 获取借阅状态类型
const getBorrowStatusType = (status) => {
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

// 获取借阅状态文本
const getBorrowStatusText = (status) => {
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
      return '借阅中'
  }
}

// 获取热度百分比
const getHeatPercentage = (count) => {
  // 找出最大借阅次数，用于计算相对热度
  const maxCount = Math.max(...popularBooks.value.map(book => book.borrowCount), 1)
  return Math.min(Math.round((count / maxCount) * 100), 100)
}

// 获取热度等级
const getHeatLevel = (count) => {
  if (count >= 10) return '非常热门'
  if (count >= 5) return '热门'
  if (count >= 3) return '较热门'
  if (count >= 1) return '一般'
  return '冷门'
}

// 获取热度颜色
const getHeatColor = (count) => {
  if (count >= 10) return '#ff4757'
  if (count >= 5) return '#ff7f50'
  if (count >= 3) return '#ffa502'
  if (count >= 1) return '#7bed9f'
  return '#70a1ff'
}

// 页面加载时获取数据
onMounted(async () => {
  await fetchDashboardData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  height: 100vh;
  background: linear-gradient(135deg, #1a6fc9 0%, #6e48aa 100%);
  background-size: 200% 200%;
  animation: gradientBG 15s ease infinite;
  position: relative;
  overflow: auto;
}

/* 粒子背景效果 */
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.particle {
  position: absolute;
  display: block;
  background-color: rgba(255, 255, 255, 0.8);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: particles 20s linear infinite;
}

.particle:nth-child(1) { top: 20%; left: 10%; animation-duration: 15s; animation-delay: 0s; }
.particle:nth-child(2) { top: 80%; left: 20%; animation-duration: 18s; animation-delay: 1s; }
.particle:nth-child(3) { top: 40%; left: 30%; animation-duration: 20s; animation-delay: 2s; }
.particle:nth-child(4) { top: 60%; left: 40%; animation-duration: 22s; animation-delay: 3s; }
.particle:nth-child(5) { top: 30%; left: 50%; animation-duration: 25s; animation-delay: 4s; }
.particle:nth-child(6) { top: 70%; left: 60%; animation-duration: 17s; animation-delay: 5s; }
.particle:nth-child(7) { top: 50%; left: 70%; animation-duration: 19s; animation-delay: 6s; }
.particle:nth-child(8) { top: 10%; left: 80%; animation-duration: 21s; animation-delay: 7s; }
.particle:nth-child(9) { top: 90%; left: 90%; animation-duration: 23s; animation-delay: 8s; }
.particle:nth-child(10) { top: 25%; left: 15%; animation-duration: 16s; animation-delay: 9s; }
.particle:nth-child(11) { top: 75%; left: 25%; animation-duration: 24s; animation-delay: 0.5s; }
.particle:nth-child(12) { top: 35%; left: 35%; animation-duration: 26s; animation-delay: 1.5s; }
.particle:nth-child(13) { top: 65%; left: 45%; animation-duration: 18s; animation-delay: 2.5s; }
.particle:nth-child(14) { top: 45%; left: 55%; animation-duration: 20s; animation-delay: 3.5s; }
.particle:nth-child(15) { top: 55%; left: 65%; animation-duration: 22s; animation-delay: 4.5s; }
.particle:nth-child(16) { top: 15%; left: 75%; animation-duration: 24s; animation-delay: 5.5s; }
.particle:nth-child(17) { top: 85%; left: 85%; animation-duration: 26s; animation-delay: 6.5s; }
.particle:nth-child(18) { top: 5%; left: 95%; animation-duration: 28s; animation-delay: 7.5s; }
.particle:nth-child(19) { top: 95%; left: 5%; animation-duration: 30s; animation-delay: 8.5s; }
.particle:nth-child(20) { top: 50%; left: 50%; animation-duration: 32s; animation-delay: 9.5s; }

@keyframes particles {
  0% {
    transform: scale(0) translate(0, 0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: scale(1) translate(100px, -100px);
    opacity: 0;
  }
}

/* 波浪背景效果 */
.wave-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 2;
  overflow: hidden;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255, 255, 255, 0.1)" fill-opacity="1" d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
  background-size: 1440px 100px;
  background-repeat: repeat-x;
}

.wave1 {
  animation: wave 30s linear infinite;
  z-index: 1;
  opacity: 0.3;
  animation-delay: 0s;
  bottom: 0;
}

.wave2 {
  animation: wave2 15s linear infinite;
  z-index: 2;
  opacity: 0.2;
  animation-delay: -5s;
  bottom: 10px;
}

.wave3 {
  animation: wave 30s linear infinite;
  z-index: 3;
  opacity: 0.1;
  animation-delay: -2s;
  bottom: 20px;
}

@keyframes wave {
  0% {
    background-position-x: 0;
  }
  100% {
    background-position-x: 1440px;
  }
}

@keyframes wave2 {
  0% {
    background-position-x: 0;
  }
  100% {
    background-position-x: -1440px;
  }
}

@keyframes gradientBG {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.welcome-section {
  text-align: center;
  margin-bottom: 20px;
  padding: 20px 0;
  position: relative;
  z-index: 10;
}

.gradient-text {
  font-size: 28px;
  margin-bottom: 4px;
}

.typewriter-container {
  height: 20px;
}

.typewriter-text {
  font-size: 14px;
}

/* 统计卡片样式 */
.stats-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin: 20px;
  position: relative;
  z-index: 10;
}

.stat-item {
  flex: 1;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
}

.stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
}

.book-stat::before {
  background: linear-gradient(90deg, #12c2e9, #c471ed);
}

.borrow-stat::before {
  background: linear-gradient(90deg, #f5576c, #f093fb);
}

.user-stat::before {
  background: linear-gradient(90deg, #ffd166, #ff9a3c);
}

.stat-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.book-stat .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(18, 194, 233, 0.2), rgba(196, 113, 237, 0.2));
  color: #12c2e9;
}

.borrow-stat .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(245, 87, 108, 0.2), rgba(240, 147, 251, 0.2));
  color: #f5576c;
}

.user-stat .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(255, 209, 102, 0.2), rgba(255, 154, 60, 0.2));
  color: #ffd166;
}

.stat-icon {
  font-size: 24px;
  animation: pulse 2s infinite;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 6px;
}

.book-stat .stat-value {
  color: #12c2e9;
}

.borrow-stat .stat-value {
  color: #f5576c;
}

.user-stat .stat-value {
  color: #ffd166;
}

.stat-progress {
  height: 6px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.book-stat .progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #12c2e9, #c471ed);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.borrow-stat .progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #f5576c, #f093fb);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.user-stat .progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #ffd166, #ff9a3c);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* 数据卡片容器 */
.data-cards-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.data-card {
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
}

.table-wrapper {
  padding: 20px;
}

:deep(.el-card__body) {
  height: 100%;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #ebeef5;
}

.section-title-container {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.section-title-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1a6fc9, #6e48aa);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  animation: iconPulse 2s infinite;
}

.section-title-wrapper {
  position: relative;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  background: linear-gradient(135deg, #1a6fc9, #6e48aa);
  -webkit-background-clip: text;
  color: transparent;
  position: relative;
  padding-bottom: 4px;
}

.section-title-decoration {
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #1a6fc9, #6e48aa);
  transform-origin: left;
  animation: lineWidth 3s infinite;
}

@keyframes iconPulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(106, 72, 170, 0.4);
  }
  70% {
    transform: scale(1.1);
    box-shadow: 0 0 0 10px rgba(106, 72, 170, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(106, 72, 170, 0);
  }
}

@keyframes lineWidth {
  0% {
    transform: scaleX(0);
    opacity: 0;
  }
  50% {
    transform: scaleX(1);
    opacity: 1;
  }
  100% {
    transform: scaleX(0);
    opacity: 0;
  }
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: nowrap;
}

.search-input {
  width: 180px;
}

.sort-group {
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.sort-label {
  font-size: 14px;
  color: #606266;
  margin-right: 4px;
}

.el-table {
  flex: 1;
  overflow: hidden;
  
  .el-table__inner-wrapper {
    height: 100%;
  }
  
  .el-table__body-wrapper {
    overflow-y: auto;
  }
}

.pagination-container {
  padding-top: 8px;
  display: flex;
  justify-content: flex-end;
}

/* 热度信息样式 */
.heat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.heat-count {
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.count-number {
  font-size: 14px;
  font-weight: bold;
  color: #409EFF;
}

.count-label {
  font-size: 12px;
  color: #909399;
}

.heat-bar-container {
  width: 100%;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.heat-bar {
  height: 100%;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.heat-level {
  font-size: 11px;
  color: #909399;
  text-align: right;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .stats-container {
    margin: 0 5px 5px 5px;
  }
  
  .stat-item {
    margin-bottom: 10px;
  }
  
  .search-input {
    width: 100px;
  }
  
  .data-cards-container {
    padding: 0 5px 5px 5px;
  }
  
  .el-col {
    margin-bottom: 10px;
  }
}
</style>