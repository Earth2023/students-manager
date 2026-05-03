import axios from "axios"

const http = axios.create({
  baseURL: "/api",
  timeout: 15000,
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token")
      window.location.href = "/login"
    }
    return Promise.reject(err)
  },
)

export const authApi = {
  login: (data) => http.post("/auth/login", data).then((r) => r.data),
  register: (data) => http.post("/auth/register", data).then((r) => r.data),
  me: () => http.get("/auth/me").then((r) => r.data),
}

export const classesApi = {
  list: () => http.get("/classes").then((r) => r.data),
  create: (data) => http.post("/classes", data).then((r) => r.data),
  studentIds: (classId) => http.get(`/classes/${classId}/students`).then((r) => r.data),
}

export const studentsApi = {
  search: (params) => http.get("/students/search", { params }).then((r) => r.data),
  create: (data, params) => http.post("/students", data, { params }).then((r) => r.data),
  get: (id) => http.get(`/students/${id}`).then((r) => r.data),
  update: (id, data) => http.put(`/students/${id}`, data).then((r) => r.data),
  delete: (id) => http.delete(`/students/${id}`),
}

export const recordsApi = {
  list: (studentId) => http.get(`/students/${studentId}/records`).then((r) => r.data),
  create: (studentId, data) => http.post(`/students/${studentId}/records`, data).then((r) => r.data),
  update: (studentId, recordId, data) =>
    http.put(`/students/${studentId}/records/${recordId}`, data).then((r) => r.data),
  delete: (studentId, recordId) => http.delete(`/students/${studentId}/records/${recordId}`),
}

export default http
