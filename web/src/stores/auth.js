import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { authApi } from "../api"

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || "")
  const teacher = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(username, password) {
    const res = await authApi.login({ username, password })
    token.value = res.access_token
    localStorage.setItem("token", res.access_token)
    await fetchTeacher()
  }

  async function register(data) {
    const res = await authApi.register(data)
    token.value = res.access_token
    localStorage.setItem("token", res.access_token)
    await fetchTeacher()
  }

  async function fetchTeacher() {
    teacher.value = await authApi.me()
  }

  function logout() {
    token.value = ""
    teacher.value = null
    localStorage.removeItem("token")
  }

  return { token, teacher, isLoggedIn, login, register, fetchTeacher, logout }
})
