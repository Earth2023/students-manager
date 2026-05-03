<template>
  <el-timeline>
    <el-timeline-item
      v-for="record in records"
      :key="record.id"
      :timestamp="formatTime(record.created_at)"
      placement="top"
    >
      <el-card shadow="hover">
        <div class="record-header">
          <el-tag :type="tagType(record.record_type)" size="small">
            {{ record.record_type }}
          </el-tag>
          <strong style="margin-left: 8px;">{{ record.title }}</strong>
          <span style="margin-left: auto; font-size: 12px; color: #909399;">
            {{ record.teacher_name }}
          </span>
          <el-button text type="danger" size="small" @click="handleDelete(record.id)" style="margin-left: 8px;">
            删除
          </el-button>
        </div>
        <p style="margin: 8px 0 0; white-space: pre-wrap; color: #606266;">{{ record.content }}</p>
      </el-card>
    </el-timeline-item>
  </el-timeline>
</template>

<script setup>
const props = defineProps({
  records: { type: Array, required: true },
})
const emit = defineEmits(["delete"])

function tagType(type) {
  const map = { 学业: "primary", 行为: "warning", 健康: "success", 其他: "info" }
  return map[type] || "info"
}

function formatTime(t) {
  if (!t) return ""
  return new Date(t).toLocaleString("zh-CN")
}

function handleDelete(id) {
  emit("delete", id)
}
</script>

<style scoped>
.record-header {
  display: flex;
  align-items: center;
}
</style>
