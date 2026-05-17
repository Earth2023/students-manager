<template>
  <div class="app-container">
    <div class="page-container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <h2 style="margin: 0;">控制台</h2>
        <ClassSwitcher />
      </div>

      <!-- 统计卡片 -->
      <el-row :gutter="20" style="margin-bottom: 24px;">
        <el-col :xs="24" :sm="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ classesStore.list.length }}</div>
              <div class="stat-label">所带班级</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ students.length }}</div>
              <div class="stat-label">当前班级学生</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-value">{{ totalRecords }}</div>
              <div class="stat-label">档案记录总数</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 数据概览 -->
      <el-row :gutter="20" style="margin-bottom: 24px;">
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover">
            <template #header>性别分布</template>
            <div v-if="students.length === 0" style="text-align: center; padding: 20px; color: #909399;">
              暂无数据
            </div>
            <div v-else style="padding: 8px 0;">
              <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span>男</span>
                  <span>{{ maleCount }} 人 ({{ malePercent }}%)</span>
                </div>
                <el-progress :percentage="malePercent" :stroke-width="16" color="#409eff" />
              </div>
              <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span>女</span>
                  <span>{{ femaleCount }} 人 ({{ femalePercent }}%)</span>
                </div>
                <el-progress :percentage="femalePercent" :stroke-width="16" color="#f56c6c" />
              </div>
              <div v-if="unknownCount > 0">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span>未知</span>
                  <span>{{ unknownCount }} 人 ({{ unknownPercent }}%)</span>
                </div>
                <el-progress :percentage="unknownPercent" :stroke-width="16" color="#909399" />
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover">
            <template #header>档案记录类型分布</template>
            <div v-if="totalRecords === 0" style="text-align: center; padding: 20px; color: #909399;">
              暂无数据
            </div>
            <div v-else style="padding: 8px 0;">
              <div v-for="(count, type) in allRecordsCount" :key="type" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span>{{ type }}</span>
                  <span>{{ count }} 条</span>
                </div>
                <el-progress
                  :percentage="Math.round(count / totalRecords * 100)"
                  :stroke-width="16"
                  :color="typeColor(type)"
                />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 当前班级学生列表 -->
      <el-card>
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <span v-if="classesStore.currentClass">
              {{ classesStore.currentClass.name }} - 学生列表
            </span>
            <span v-else>请选择一个班级</span>
            <el-space>
              <el-button size="small" @click="handleExport" :disabled="students.length === 0">
                <el-icon><Download /></el-icon> 导出 CSV
              </el-button>
              <el-button type="primary" size="small" @click="$router.push('/students/new')">
                <el-icon><Plus /></el-icon> 添加学生
              </el-button>
            </el-space>
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
          <el-button @click="$router.push('/settings')">
            <el-icon><Setting /></el-icon> 个人设置
          </el-button>
        </el-space>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from "vue"
import { ElMessage } from "element-plus"
import ClassSwitcher from "../components/ClassSwitcher.vue"
import StudentCard from "../components/StudentCard.vue"
import { useAuthStore } from "../stores/auth"
import { useClassesStore } from "../stores/classes"
import { classesApi, studentsApi, recordsApi } from "../api"

const authStore = useAuthStore()
const classesStore = useClassesStore()
const students = ref([])
const totalRecords = ref(0)
const allRecordsCount = ref({})

const maleCount = computed(() => students.value.filter((s) => s.gender === "男").length)
const femaleCount = computed(() => students.value.filter((s) => s.gender === "女").length)
const unknownCount = computed(() => students.value.length - maleCount.value - femaleCount.value)
const malePercent = computed(() => students.value.length ? Math.round(maleCount.value / students.value.length * 100) : 0)
const femalePercent = computed(() => students.value.length ? Math.round(femaleCount.value / students.value.length * 100) : 0)
const unknownPercent = computed(() => students.value.length ? Math.round(unknownCount.value / students.value.length * 100) : 0)

function typeColor(type) {
  const map = { 学业: "#409eff", 行为: "#e6a23c", 健康: "#67c23a", 其他: "#909399" }
  return map[type] || "#909399"
}

async function loadClassData(classId) {
  if (!classId) {
    students.value = []
    totalRecords.value = 0
    allRecordsCount.value = {}
    return
  }
  try {
    const ids = await classesApi.studentIds(classId)
    const promises = ids.map((id) => studentsApi.get(id).catch(() => null))
    students.value = (await Promise.all(promises)).filter(Boolean)
    let count = 0
    const typeCount = {}
    for (const s of students.value) {
      try {
        const records = await recordsApi.list(s.id)
        count += records.length
        for (const r of records) {
          typeCount[r.record_type] = (typeCount[r.record_type] || 0) + 1
        }
      } catch { /* ignore */ }
    }
    totalRecords.value = count
    allRecordsCount.value = typeCount
  } catch {
    students.value = []
    totalRecords.value = 0
    allRecordsCount.value = {}
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
    await loadClassData(classesStore.currentClassId)
  }
})

watch(() => classesStore.currentClassId, (classId) => {
  loadClassData(classId)
})

async function handleExport() {
  if (!classesStore.currentClassId) {
    ElMessage.warning("请先选择班级")
    return
  }
  try {
    const blob = await studentsApi.exportCsv(classesStore.currentClassId)
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${classesStore.currentClass?.name || "students"}.csv`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success("导出成功")
  } catch {
    ElMessage.error("导出失败")
  }
}
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
