<template>
  <div class="app-container">
    <div class="page-container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <h2 style="margin: 0;">学生管理</h2>
        <el-space>
          <ClassSwitcher />
          <el-button type="primary" @click="$router.push('/students/new')">
            <el-icon><Plus /></el-icon> 添加学生
          </el-button>
        </el-space>
      </div>

      <!-- 搜索 -->
      <el-card style="margin-bottom: 20px;">
        <el-form :model="searchForm" inline>
          <el-form-item label="搜索">
            <el-input
              v-model="searchForm.q"
              placeholder="按姓名或学号搜索"
              clearable
              style="width: 260px;"
              @keyup.enter="handleSearch"
              @clear="handleSearch"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 学生列表 -->
      <div v-if="loading" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      </div>
      <template v-else>
        <div v-if="students.length === 0" style="text-align: center; padding: 60px; color: #909399;">
          暂无学生数据
        </div>
        <StudentCard v-for="s in students" :key="s.id" :student="s" />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import ClassSwitcher from "../components/ClassSwitcher.vue"
import StudentCard from "../components/StudentCard.vue"
import { useClassesStore } from "../stores/classes"
import { studentsApi, classesApi } from "../api"

const classesStore = useClassesStore()
const students = ref([])
const loading = ref(false)
const searchForm = ref({ q: "" })

onMounted(async () => {
  await classesStore.fetchClasses()
  if (classesStore.list.length > 0) {
    if (!classesStore.currentClassId) {
      classesStore.switchClass(classesStore.list[0].id)
    }
    await loadStudents()
  }
})

async function loadStudents() {
  loading.value = true
  try {
    if (searchForm.value.q) {
      students.value = await studentsApi.search({ q: searchForm.value.q })
    } else if (classesStore.currentClassId) {
      const ids = await classesApi.studentIds(classesStore.currentClassId)
      const promises = ids.map((id) => studentsApi.get(id).catch(() => null))
      students.value = (await Promise.all(promises)).filter(Boolean)
    } else {
      students.value = []
    }
  } catch {
    students.value = []
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  await loadStudents()
}

async function resetSearch() {
  searchForm.value.q = ""
  await loadStudents()
}

// 切换班级时重新加载
watch(() => classesStore.currentClassId, () => {
  if (!searchForm.value.q) loadStudents()
})
</script>
