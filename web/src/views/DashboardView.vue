<template>
  <div class="app-container">
    <AppHeader />
    <div class="page-container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <h2 style="margin: 0;">控制台</h2>
        <ClassSwitcher />
      </div>

      <!-- 统计卡片 -->
      <el-row :gutter="20" style="margin-bottom: 24px;">
        <el-col :span="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ classesStore.list.length }}</div>
              <div class="stat-label">所带班级</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ students.length }}</div>
              <div class="stat-label">当前班级学生</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ totalRecords }}</div>
              <div class="stat-label">档案记录总数</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 当前班级学生列表 -->
      <el-card>
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span v-if="classesStore.currentClass">
              {{ classesStore.currentClass.name }} - 学生列表
            </span>
            <span v-else>请选择一个班级</span>
            <el-button type="primary" size="small" @click="$router.push('/students/new')">
              <el-icon><Plus /></el-icon> 添加学生
            </el-button>
          </div>
        </template>
        <div v-if="students.length === 0" style="text-align: center; padding: 40px; color: #909399;">
          暂无学生数据，请先选择班级或添加学生
        </div>
        <StudentCard v-for="s in students" :key="s.id" :student="s" />
      </el-card>

      <!-- 快捷操作 -->
      <el-card style="margin-top: 24px;">
        <template #header>快捷操作</template>
        <el-space wrap>
          <el-button @click="$router.push('/students')">
            <el-icon><Search /></el-icon> 查询学生
          </el-button>
          <el-button @click="$router.push('/students/new')">
            <el-icon><Plus /></el-icon> 录入新生
          </el-button>
        </el-space>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import AppHeader from "../components/AppHeader.vue"
import ClassSwitcher from "../components/ClassSwitcher.vue"
import StudentCard from "../components/StudentCard.vue"
import { useAuthStore } from "../stores/auth"
import { useClassesStore } from "../stores/classes"
import { classesApi, studentsApi, recordsApi } from "../api"

const authStore = useAuthStore()
const classesStore = useClassesStore()
const students = ref([])
const totalRecords = ref(0)

async function loadClassData(classId) {
  if (!classId) {
    students.value = []
    totalRecords.value = 0
    return
  }
  try {
    const ids = await classesApi.studentIds(classId)
    const promises = ids.map((id) => studentsApi.get(id).catch(() => null))
    students.value = (await Promise.all(promises)).filter(Boolean)
    let count = 0
    for (const s of students.value) {
      try {
        const records = await recordsApi.list(s.id)
        count += records.length
      } catch { /* ignore */ }
    }
    totalRecords.value = count
  } catch {
    students.value = []
    totalRecords.value = 0
  }
}

onMounted(async () => {
  if (!authStore.teacher) {
    await authStore.fetchTeacher()
  }
  await classesStore.fetchClasses()
  if (classesStore.list.length > 0) {
    if (!classesStore.currentClassId) {
      classesStore.switchClass(classesStore.list[0].id)
    }
    // 无论是刚选中还是已有选中，都主动加载数据
    await loadClassData(classesStore.currentClassId)
  }
})

// 切换班级时重新加载
watch(() => classesStore.currentClassId, (classId) => {
  loadClassData(classId)
})
</script>

<style scoped>
.stat-item {
  text-align: center;
  padding: 16px 0;
}
.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}
</style>
