<template>
  <div class="app-container">
    <AppHeader />
    <div class="page-container">
      <el-button text @click="goBack" style="margin-bottom: 16px;">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>

      <el-card shadow="never">
        <template #header>
          <span>{{ isEdit ? '编辑学生信息' : '添加新学生' }}</span>
        </template>

        <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" style="max-width: 600px;">
          <el-form-item label="学号" prop="student_no">
            <el-input v-model="form.student_no" placeholder="请输入学号" :disabled="isEdit" />
          </el-form-item>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-select v-model="form.gender" placeholder="请选择" style="width: 100%">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item label="出生日期" prop="birth_date">
            <el-date-picker v-model="form.birth_date" type="date" placeholder="选择日期" style="width: 100%" value-format="YYYY-MM-DD" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="form.phone" placeholder="联系电话" />
          </el-form-item>
          <el-form-item label="家庭住址">
            <el-input v-model="form.address" placeholder="家庭住址" />
          </el-form-item>
          <el-form-item label="家长姓名">
            <el-input v-model="form.parent_name" placeholder="家长姓名" />
          </el-form-item>
          <el-form-item label="家长电话">
            <el-input v-model="form.parent_phone" placeholder="家长电话" />
          </el-form-item>
          <el-form-item v-if="!isEdit" label="所属班级">
            <el-select v-model="form.classId" placeholder="请选择班级" style="width: 100%">
              <el-option v-for="cls in classesStore.list" :key="cls.id" :label="cls.name" :value="cls.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.notes" type="textarea" :rows="3" placeholder="备注信息" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="submitting" @click="handleSubmit">
              {{ isEdit ? '保存修改' : '添加学生' }}
            </el-button>
            <el-button @click="goBack">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import AppHeader from "../components/AppHeader.vue"
import { useClassesStore } from "../stores/classes"
import { studentsApi } from "../api"

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)
const classesStore = useClassesStore()

const isEdit = computed(() => route.name === "StudentEdit")

const form = reactive({
  student_no: "",
  name: "",
  gender: "",
  birth_date: null,
  phone: "",
  address: "",
  parent_name: "",
  parent_phone: "",
  notes: "",
  classId: null,
})

const rules = {
  student_no: [{ required: true, message: "请输入学号", trigger: "blur" }],
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
}

onMounted(async () => {
  await classesStore.fetchClasses()
  if (!isEdit.value && classesStore.currentClassId) {
    form.classId = classesStore.currentClassId
  }
  if (isEdit.value) {
    try {
      const data = await studentsApi.get(route.params.id)
      Object.assign(form, {
        student_no: data.student_no,
        name: data.name,
        gender: data.gender,
        birth_date: data.birth_date,
        phone: data.phone,
        address: data.address,
        parent_name: data.parent_name,
        parent_phone: data.parent_phone,
        notes: data.notes,
      })
    } catch {
      ElMessage.error("获取学生信息失败")
      router.push("/students")
    }
  }
})

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    const payload = { ...form }
    delete payload.classId
    if (isEdit.value) {
      await studentsApi.update(route.params.id, payload)
      ElMessage.success("保存成功")
      router.push(`/students/${route.params.id}`)
    } else {
      await studentsApi.create(payload, form.classId ? { class_id: form.classId } : {})
      ElMessage.success("添加成功")
      router.push("/")
    }
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "操作失败")
  } finally {
    submitting.value = false
  }
}

function goBack() {
  if (isEdit.value) {
    router.push(`/students/${route.params.id}`)
  } else {
    router.push("/")
  }
}
</script>
