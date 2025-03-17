<template>
  <div>
    <h2>Radio Test</h2>
    <el-radio-group v-model="selected">
      <el-radio :value="1" label="选项1" />
      <el-radio :value="2" label="选项2" />
      <el-radio :value="3" label="选项3" />
    </el-radio-group>
    <p>选中的值: {{ selected }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selected = ref(1)
</script> 