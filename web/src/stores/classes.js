import { computed, ref } from "vue"
import { defineStore } from "pinia"
import { classesApi } from "../api"

export const useClassesStore = defineStore("classes", () => {
  const list = ref([])
  const currentClassId = ref(null)

  const currentClass = computed(() => list.value.find((c) => c.id === currentClassId.value) || null)

  async function fetchClasses() {
    list.value = await classesApi.list()
  }

  async function createClass(data) {
    const cls = await classesApi.create(data)
    list.value.push(cls)
    return cls
  }

  function switchClass(classId) {
    currentClassId.value = classId
  }

  return { list, currentClassId, currentClass, fetchClasses, createClass, switchClass }
})
