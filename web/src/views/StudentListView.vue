<template>
  <div class="app-container">
    <div class="page-container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 8px;">
        <h2 style="margin: 0;">学生管理</h2>
        <el-space wrap>
          <ClassSwitcher />
          <el-button @click="showImportDialog = true">
            <el-icon><Upload /></el-icon> 批量导入
          </el-button>
          <el-button @click="handleExport" :disabled="students.length === 0">
            <el-icon><Download /></el-icon> 导出 CSV
          </el-button>
          <el-button type="primary" @click="$router.push('/students/new')">
            <el-icon><Plus /></el-icon> 添加学生
          </el-button>
        </el-space>
      </div>

      <!-- 搜索与筛选 -->
      <el-card style="margin-bottom: 20px;">
        <el-form :model="searchForm" inline>
          <el-form-item label="搜索">
            <el-input
              v-model="searchForm.q"
              placeholder="按姓名或学号搜索"
              clearable
              style="width: 220px;"
              @keyup.enter="handleSearch"
              @clear="handleSearch"
            />
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="searchForm.gender" placeholder="全部" clearable style="width: 100px;" @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
          <el-form-item v-if="total > pageSize" style="float: right;">
            <span style="font-size: 13px; color: #909399;">共 {{ total }} 条</span>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 加载状态 -->
      <div v-if="loading" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        <p style="color: #909399; margin-top: 8px;">加载中...</p>
      </div>

      <!-- 学生列表 -->
      <template v-else>
        <div v-if="students.length === 0" style="text-align: center; padding: 60px; color: #909399;">
          <el-icon :size="48" style="margin-bottom: 12px;"><UserFilled /></el-icon>
          <p>暂无学生数据</p>
        </div>
        <StudentCard v-for="s in students" :key="s.id" :student="s" />

        <!-- 分页 -->
        <div v-if="total > pageSize" style="display: flex; justify-content: center; margin-top: 20px;">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="handlePageChange"
          />
        </div>
      </template>

      <!-- 批量导入对话框 -->
      <el-dialog v-model="showImportDialog" title="批量导入学生" width="500px">
        <el-form>
          <el-form-item label="目标班级">
            <el-select v-model="importClassId" placeholder="请选择班级" style="width: 100%">
              <el-option v-for="cls in classesStore.list" :key="cls.id" :label="cls.name" :value="cls.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="CSV 文件">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :show-file-list="true"
              accept=".csv"
              :limit="1"
              :on-change="handleFileChange"
            >
              <el-button type="primary">
                <el-icon><Upload /></el-icon> 选择文件
              </el-button>
              <template #tip>
                <div style="font-size: 12px; color: #909399; margin-top: 4px;">
                  CSV 列顺序：学号,姓名,性别,出生日期,联系电话,家庭住址,家长姓名,家长电话,备注
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
        <div v-if="importResult" style="margin-top: 12px; padding: 12px; background: #f5f7fa; border-radius: 6px;">
          <p><el-tag type="success">成功: {{ importResult.success }}</el-tag>
          <el-tag v-if="importResult.failed > 0" type="danger" style="margin-left: 8px;">失败: {{ importResult.failed }}</el-tag></p>
          <div v-if="importResult.errors.length > 0" style="margin-top: 8px;">
            <p style="font-weight: 500; color: #f56c6c;">错误详情：</p>
            <ul style="font-size: 12px; color: #606266; max-height: 150px; overflow-y: auto;">
              <li v-for="(err, i) in importResult.errors" :key="i">{{ err }}</li>
            </ul>
          </div>
        </div>
        <template #footer>
          <el-button @click="showImportDialog = false">关闭</el-button>
          <el-button type="primary" :loading="importing" @click="handleImport" :disabled="!importFile || !importClassId">
            开始导入
          </el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import { ElMessage } from "element-plus"
import ClassSwitcher from "../components/ClassSwitcher.vue"
import StudentCard from "../components/StudentCard.vue"
import { useClassesStore } from "../stores/classes"
import { studentsApi, classesApi } from "../api"

const classesStore = useClassesStore()
const students = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const searchForm = ref({ q: "", gender: "" })

// 导入相关
const showImportDialog = ref(false)
const importClassId = ref(null)
const importFile = ref(null)
const importing = ref(false)
const importResult = ref(null)

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
    const params = {
      q: searchForm.value.q,
      gender: searchForm.value.gender || undefined,
      class_id: classesStore.currentClassId || undefined,
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (!params.q) delete params.q
    if (!params.gender) delete params.gender
    if (!params.class_id) delete params.class_id
    const res = await studentsApi.search(params)
    students.value = res.items
    total.value = res.total
  } catch {
    students.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  currentPage.value = 1
  await loadStudents()
}

async function resetSearch() {
  searchForm.value.q = ""
  searchForm.value.gender = ""
  currentPage.value = 1
  await loadStudents()
}

async function handlePageChange(page) {
  currentPage.value = page
  await loadStudents()
}

// 切换班级时重新加载
watch(() => classesStore.currentClassId, () => {
  if (!searchForm.value.q) loadStudents()
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

function handleFileChange(uploadFile) {
  importFile.value = uploadFile.raw
  uploadFile.status = "ready"
}

async function handleImport() {
  if (!importFile.value || !importClassId.value) return
  importing.value = true
  importResult.value = null
  try {
    const res = await studentsApi.importCsv(importFile.value, importClassId.value)
    importResult.value = res
    if (res.success > 0) {
      ElMessage.success(`成功导入 ${res.success} 名学生`)
      await loadStudents()
    }
    if (res.failed > 0) {
      ElMessage.warning(`${res.failed} 条导入失败`)
    }
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "导入失败")
  } finally {
    importing.value = false
  }
}
</script>
