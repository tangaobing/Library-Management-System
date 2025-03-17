<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
// 组件逻辑
</script>

<style lang="scss">
@use '@/assets/styles/index' as *;

// 全局样式
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $text-primary;
  height: 100vh;
}

.app-container {
  width: 100%;
  height: 100%;
}
</style> 