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
          <span v-if="record.updated_at && record.updated_at !== record.created_at" style="margin-left: 8px; font-size: 11px; color: #c0c4cc;">
            已编辑
          </span>
          <el-button text type="primary" size="small" @click="handleEdit(record)" style="margin-left: 8px;">
            编辑
          </el-button>
          <el-button text type="danger" size="small" @click="handleDelete(record.id)">
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
const emit = defineEmits(["delete", "edit"])

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

function handleEdit(record) {
  emit("edit", record)
}
</script>

<style scoped>
.record-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
