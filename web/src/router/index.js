import { createRouter, createWebHistory } from "vue-router"

import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import DashboardView from "../views/DashboardView.vue"
import StudentListView from "../views/StudentListView.vue"
import StudentDetailView from "../views/StudentDetailView.vue"
import StudentFormView from "../views/StudentFormView.vue"
import RecordsView from "../views/RecordsView.vue"
import SettingsView from "../views/SettingsView.vue"

const routes = [
  { path: "/login", name: "Login", component: LoginView, meta: { guest: true } },
  { path: "/register", name: "Register", component: RegisterView, meta: { guest: true } },
  { path: "/", name: "Dashboard", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/students", name: "StudentList", component: StudentListView, meta: { requiresAuth: true } },
  { path: "/students/new", name: "StudentNew", component: StudentFormView, meta: { requiresAuth: true } },
  { path: "/students/:id", name: "StudentDetail", component: StudentDetailView, meta: { requiresAuth: true } },
  { path: "/students/:id/edit", name: "StudentEdit", component: StudentFormView, meta: { requiresAuth: true } },
  { path: "/students/:id/records", name: "StudentRecords", component: RecordsView, meta: { requiresAuth: true } },
  { path: "/settings", name: "Settings", component: SettingsView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  if (to.meta.requiresAuth && !token) {
    next("/login")
  } else if (to.meta.guest && token) {
    next("/")
  } else {
    next()
  }
})

export default router
