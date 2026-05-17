<template>
  <div class="app-container">
    <div class="page-container">
      <h2 style="margin-bottom: 24px;">个人设置</h2>

      <el-row :gutter="24">
        <!-- 个人信息 -->
        <el-col :span="12">
          <el-card shadow="never">
            <template #header>
              <span>个人信息</span>
            </template>
            <el-form ref="profileFormRef" :model="profileForm" :rules="profileRules" label-width="100px">
              <el-form-item label="用户名">
                <el-input :model-value="authStore.teacher?.username" disabled />
              </el-form-item>
              <el-form-item label="姓名" prop="name">
                <el-input v-model="profileForm.name" />
              </el-form-item>
              <el-form-item label="联系电话" prop="phone">
                <el-input v-model="profileForm.phone" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="profileSubmitting" @click="handleUpdateProfile">
                  保存
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- 修改密码 -->
        <el-col :span="12">
          <el-card shadow="never">
            <template #header>
              <span>修改密码</span>
            </template>
            <el-form ref="pwdFormRef" :model="pwdForm" :rules="pwdRules" label-width="100px">
              <el-form-item label="原密码" prop="old_password">
                <el-input v-model="pwdForm.old_password" type="password" show-password />
              </el-form-item>
              <el-form-item label="新密码" prop="new_password">
                <el-input v-model="pwdForm.new_password" type="password" show-password />
              </el-form-item>
              <el-form-item label="确认密码" prop="confirm_password">
                <el-input v-model="pwdForm.confirm_password" type="password" show-password />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="pwdSubmitting" @click="handleChangePassword">
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { ElMessage } from "element-plus"
import { useAuthStore } from "../stores/auth"
import { authApi } from "../api"

const authStore = useAuthStore()
const profileFormRef = ref(null)
const pwdFormRef = ref(null)
const profileSubmitting = ref(false)
const pwdSubmitting = ref(false)

const profileForm = reactive({
  name: "",
  phone: "",
})

const profileRules = {}

const pwdForm = reactive({
  old_password: "",
  new_password: "",
  confirm_password: "",
})

const validateConfirm = (rule, value, callback) => {
  if (value && value !== pwdForm.new_password) {
    callback(new Error("两次密码输入不一致"))
  } else {
    callback()
  }
}

const pwdRules = {
  old_password: [{ required: true, message: "请输入原密码", trigger: "blur" }],
  new_password: [{ required: true, min: 6, message: "密码至少6位", trigger: "blur" }],
  confirm_password: [{ required: true, validator: validateConfirm, trigger: "blur" }],
}

onMounted(async () => {
  if (authStore.teacher) {
    profileForm.name = authStore.teacher.name
    profileForm.phone = authStore.teacher.phone || ""
  }
})

async function handleUpdateProfile() {
  const valid = await profileFormRef.value.validate().catch(() => false)
  if (!valid) return
  profileSubmitting.value = true
  try {
    const data = await authApi.updateProfile({
      name: profileForm.name,
      phone: profileForm.phone,
    })
    authStore.teacher = data
    ElMessage.success("个人信息已更新")
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "更新失败")
  } finally {
    profileSubmitting.value = false
  }
}

async function handleChangePassword() {
  const valid = await pwdFormRef.value.validate().catch(() => false)
  if (!valid) return
  pwdSubmitting.value = true
  try {
    await authApi.changePassword({
      old_password: pwdForm.old_password,
      new_password: pwdForm.new_password,
    })
    ElMessage.success("密码已修改")
    pwdForm.old_password = ""
    pwdForm.new_password = ""
    pwdForm.confirm_password = ""
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "修改失败")
  } finally {
    pwdSubmitting.value = false
  }
}
</script>
