<template>
  <div class="app-container">
    <AppHeader />
    <div class="page-container">
      <el-button text @click="$router.push('/students')" style="margin-bottom: 16px;">
        <el-icon><ArrowLeft /></el-icon> 返回学生列表
      </el-button>

      <el-card v-if="student" shadow="never">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>
              <el-avatar :size="40" style="margin-right: 12px; vertical-align: middle;">
                {{ student.name.charAt(0) }}
              </el-avatar>
              <strong style="font-size: 18px;">{{ student.name }}</strong>
              <el-tag style="margin-left: 12px;" size="small">{{ student.student_no }}</el-tag>
            </span>
            <el-space>
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
          <el-descriptions-item label="联系电话">{{ student.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家庭住址">{{ student.address || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家长姓名">{{ student.parent_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家长电话">{{ student.parent_phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ student.notes || '-' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ElMessage, ElMessageBox } from "element-plus"
import AppHeader from "../components/AppHeader.vue"
import { studentsApi } from "../api"

const route = useRoute()
const router = useRouter()
const student = ref(null)

onMounted(async () => {
  try {
    student.value = await studentsApi.get(route.params.id)
  } catch {
    ElMessage.error("获取学生信息失败")
    router.push("/students")
  }
})

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
