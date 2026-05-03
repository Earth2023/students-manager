<template>
  <el-menu mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/">
      <el-icon><School /></el-icon>
      <span style="margin-left: 6px; font-weight: bold; font-size: 16px;">学生信息管理系统</span>
    </el-menu-item>

    <el-menu-item index="/students">学生管理</el-menu-item>

    <div style="flex: 1" />

    <el-dropdown v-if="authStore.teacher" style="line-height: 60px; margin-right: 20px; cursor: pointer;">
      <span>
        {{ authStore.teacher.name }}
        <el-icon><ArrowDown /></el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </el-menu>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push("/login")
}
</script>
