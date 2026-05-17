<template>
  <div class="app-container">
    <div class="page-container">
      <el-button text @click="$router.push(`/students/${studentId}`)" style="margin-bottom: 16px;">
        <el-icon><ArrowLeft /></el-icon> 返回学生详情
      </el-button>

      <el-card style="margin-bottom: 24px;">
        <template #header>
          <span style="font-size: 16px; font-weight: 500;">
            添加档案记录 - {{ studentName }}
          </span>
        </template>

        <el-form ref="formRef" :model="recordForm" :rules="recordRules" label-width="80px" style="max-width: 600px;">
          <el-form-item label="类型" prop="record_type">
            <el-select v-model="recordForm.record_type" style="width: 100%">
              <el-option v-for="t in types" :key="t" :label="t" :value="t" />
            </el-select>
          </el-form-item>
          <el-form-item label="标题" prop="title">
            <el-input v-model="recordForm.title" placeholder="记录标题" />
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input v-model="recordForm.content" type="textarea" :rows="4" placeholder="记录内容" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="submitting" @click="handleAddRecord">提交记录</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card>
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 16px; font-weight: 500;">
              档案时间线 ({{ records.length }} 条)
            </span>
          </div>
        </template>
        <div v-if="records.length === 0" style="text-align: center; padding: 40px; color: #909399;">
          暂无档案记录
        </div>
        <RecordTimeline :records="records" @delete="handleDeleteRecord" @edit="handleEditRecord" />
      </el-card>

      <!-- 编辑记录对话框 -->
      <el-dialog v-model="editDialogVisible" title="编辑档案记录" width="500px">
        <el-form ref="editFormRef" :model="editForm" :rules="recordRules" label-width="80px">
          <el-form-item label="类型" prop="record_type">
            <el-select v-model="editForm.record_type" style="width: 100%">
              <el-option v-for="t in types" :key="t" :label="t" :value="t" />
            </el-select>
          </el-form-item>
          <el-form-item label="标题" prop="title">
            <el-input v-model="editForm.title" placeholder="记录标题" />
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input v-model="editForm.content" type="textarea" :rows="4" placeholder="记录内容" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="editSubmitting" @click="handleSaveEdit">保存</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ElMessage, ElMessageBox } from "element-plus"
import RecordTimeline from "../components/RecordTimeline.vue"
import { recordsApi, studentsApi } from "../api"

const route = useRoute()
const router = useRouter()
const studentId = route.params.id
const studentName = ref("")
const formRef = ref(null)
const editFormRef = ref(null)
const submitting = ref(false)
const editSubmitting = ref(false)
const records = ref([])
const editDialogVisible = ref(false)
const editingRecordId = ref(null)
const types = ["学业", "行为", "健康", "其他"]

const recordForm = reactive({
  record_type: "其他",
  title: "",
  content: "",
})

const editForm = reactive({
  record_type: "其他",
  title: "",
  content: "",
})

const recordRules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  content: [{ required: true, message: "请输入内容", trigger: "blur" }],
}

onMounted(async () => {
  try {
    const student = await studentsApi.get(studentId)
    studentName.value = student.name
  } catch {
    ElMessage.error("获取学生信息失败")
    router.push("/students")
    return
  }
  await loadRecords()
})

async function loadRecords() {
  try {
    records.value = await recordsApi.list(studentId)
  } catch {
    records.value = []
  }
}

async function handleAddRecord() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    await recordsApi.create(studentId, {
      title: recordForm.title,
      content: recordForm.content,
      record_type: recordForm.record_type,
    })
    ElMessage.success("记录添加成功")
    recordForm.title = ""
    recordForm.content = ""
    recordForm.record_type = "其他"
    await loadRecords()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "添加失败")
  } finally {
    submitting.value = false
  }
}

async function handleDeleteRecord(recordId) {
  try {
    await ElMessageBox.confirm("确定删除此记录？", "确认", {
      type: "warning",
      confirmButtonText: "删除",
      cancelButtonText: "取消",
    })
    await recordsApi.delete(studentId, recordId)
    ElMessage.success("删除成功")
    await loadRecords()
  } catch {
    // cancelled
  }
}

function handleEditRecord(record) {
  editingRecordId.value = record.id
  editForm.record_type = record.record_type
  editForm.title = record.title
  editForm.content = record.content
  editDialogVisible.value = true
}

async function handleSaveEdit() {
  const valid = await editFormRef.value.validate().catch(() => false)
  if (!valid) return
  editSubmitting.value = true
  try {
    await recordsApi.update(studentId, editingRecordId.value, {
      title: editForm.title,
      content: editForm.content,
      record_type: editForm.record_type,
    })
    ElMessage.success("记录已更新")
    editDialogVisible.value = false
    await loadRecords()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "更新失败")
  } finally {
    editSubmitting.value = false
  }
}
</script>
