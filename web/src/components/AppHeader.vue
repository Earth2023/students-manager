<template>
  <el-menu mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/">
      <el-icon><School /></el-icon>
      <span style="margin-left: 6px; font-weight: bold; font-size: 16px;">学生信息管理系统</span>
    </el-menu-item>

    <el-menu-item index="/students">学生管理</el-menu-item>

    <div style="flex: 1" />

    <!-- 暗色模式切换 -->
    <el-tooltip :content="isDark ? '切换亮色模式' : '切换暗色模式'" placement="bottom">
      <el-button
        :icon="isDark ? Sunny : Moon"
        @click="toggleDark"
        text
        style="margin-right: 12px; border: none; font-size: 18px; margin-top: 13px;"
      />
    </el-tooltip>

    <el-dropdown v-if="authStore.teacher" style="line-height: 60px; margin-right: 20px; cursor: pointer;">
      <span>
        {{ authStore.teacher.name }}
        <el-icon><ArrowDown /></el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="$router.push('/settings')">
            <el-icon><Setting /></el-icon> 个人设置
          </el-dropdown-item>
          <el-dropdown-item divided @click="handleLogout">
            <el-icon><SwitchButton /></el-icon> 退出登录
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </el-menu>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { Moon, Sunny, Setting, SwitchButton } from "@element-plus/icons-vue"
import { useAuthStore } from "../stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const isDark = ref(localStorage.getItem("dark-mode") === "true")
const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem("dark-mode", isDark.value)
  applyDarkMode(isDark.value)
}

function applyDarkMode(dark) {
  document.documentElement.classList.toggle("dark", dark)
}

onMounted(() => {
  applyDarkMode(isDark.value)
})

function handleLogout() {
  authStore.logout()
  router.push("/login")
}
</script>
