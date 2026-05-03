<template>
  <el-card shadow="hover" class="student-card" @click="$router.push(`/students/${student.id}`)">
    <div class="card-content">
      <el-avatar :size="48">{{ student.name.charAt(0) }}</el-avatar>
      <div class="card-info">
        <div class="card-name">{{ student.name }}</div>
        <div class="card-meta">
          <span>学号：{{ student.student_no }}</span>
          <span v-if="student.gender"> | {{ student.gender }}</span>
        </div>
      </div>
      <el-icon class="card-arrow"><ArrowRight /></el-icon>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  student: { type: Object, required: true },
})
</script>

<style scoped>
.student-card {
  margin-bottom: 12px;
  cursor: pointer;
}
.card-content {
  display: flex;
  align-items: center;
  gap: 12px;
}
.card-info {
  flex: 1;
}
.card-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}
.card-meta {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
.card-arrow {
  color: #c0c4cc;
}
</style>
