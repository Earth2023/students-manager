<template>
  <div class="app-container">
    <div class="page-container">
      <el-button text @click="$router.push('/students')" style="margin-bottom: 16px;">
        <el-icon><ArrowLeft /></el-icon> 返回学生列表
      </el-button>

      <el-card v-if="student" shadow="never">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <span style="display: flex; align-items: center; gap: 12px;">
              <el-avatar :size="48" :src="avatarUrl">
                {{ student.name.charAt(0) }}
              </el-avatar>
              <div>
                <strong style="font-size: 18px;">{{ student.name }}</strong>
                <el-tag style="margin-left: 12px;" size="small">{{ student.student_no }}</el-tag>
              </div>
            </span>
            <el-space wrap>
              <el-upload
                :show-file-list="false"
                :auto-upload="false"
                accept="image/jpeg,image/png,image/gif,image/webp"
                :on-change="handleAvatarChange"
              >
                <el-button size="small">
                  <el-icon><Camera /></el-icon> 上传头像
                </el-button>
              </el-upload>
              <el-button type="primary" @click="$router.push(`/students/${student.id}/edit`)">
                <el-icon><Edit /></el-icon> 编辑
              </el-button>
              <el-button @click="$router.push(`/students/${student.id}/records`)">
                <el-icon><Document /></el-icon> 档案记录
              </el-button>
              <el-button type="danger" @click="handleDelete">
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </el-space>
          </div>
        </template>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="学号">{{ student.student_no }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ student.gender || '-' }}</el-descriptions-item>
          <el-descriptions-item label="出生日期">{{ student.birth_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="所属班级">
            <template v-if="student.classes && student.classes.length > 0">
              <el-tag v-for="c in student.classes" :key="c.id" size="small" style="margin-right: 4px;">
                {{ c.grade ? c.grade + ' ' : '' }}{{ c.name }}
              </el-tag>
            </template>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ student.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家庭住址">{{ student.address || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家长姓名">{{ student.parent_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家长电话">{{ student.parent_phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ student.notes || '-' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 档案统计 -->
        <div v-if="stats" style="margin-top: 20px;">
          <el-divider />
          <h4 style="margin: 0 0 12px 0;">档案记录统计</h4>
          <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <el-tag v-for="(count, type) in stats.by_type" :key="type" :type="tagType(type)" size="large">
              {{ type }}: {{ count }} 条
            </el-tag>
            <el-tag type="info" size="large">总计: {{ stats.total }} 条</el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ElMessage, ElMessageBox } from "element-plus"
import { studentsApi } from "../api"

const route = useRoute()
const router = useRouter()
const student = ref(null)
const stats = ref(null)

const avatarUrl = computed(() => {
  if (student.value?.avatar) {
    return `/uploads/avatars/${student.value.avatar}`
  }
  return ""
})

function tagType(type) {
  const map = { 学业: "primary", 行为: "warning", 健康: "success", 其他: "info" }
  return map[type] || "info"
}

onMounted(async () => {
  try {
    student.value = await studentsApi.get(route.params.id)
    stats.value = await studentsApi.getStats(route.params.id)
  } catch {
    ElMessage.error("获取学生信息失败")
    router.push("/students")
  }
})

async function handleAvatarChange(uploadFile) {
  try {
    const updated = await studentsApi.uploadAvatar(route.params.id, uploadFile.raw)
    student.value = updated
    ElMessage.success("头像上传成功")
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "头像上传失败")
  }
}

async function handleDelete() {
  try {
    await ElMessageBox.confirm("确定要删除该学生吗？此操作不可恢复。", "确认删除", {
      type: "warning",
      confirmButtonText: "确认删除",
      cancelButtonText: "取消",
    })
    await studentsApi.delete(route.params.id)
    ElMessage.success("删除成功")
    router.push("/students")
  } catch {
    // cancelled
  }
}
</script>
