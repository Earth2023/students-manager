<template>
  <el-select
    v-model="currentId"
    placeholder="选择班级"
    style="width: 200px"
    @change="handleChange"
  >
    <el-option
      v-for="cls in classesStore.list"
      :key="cls.id"
      :label="`${cls.name} (${cls.grade || '未设置年级'})`"
      :value="cls.id"
    />
  </el-select>
  <el-button type="primary" link @click="showCreate = true">
    <el-icon><Plus /></el-icon> 新建班级
  </el-button>

  <el-dialog v-model="showCreate" title="新建班级" width="400px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="班级名称">
        <el-input v-model="form.name" placeholder="如：三年级一班" />
      </el-form-item>
      <el-form-item label="年级">
        <el-input v-model="form.grade" placeholder="如：三年级" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showCreate = false">取消</el-button>
      <el-button type="primary" @click="handleCreate">确定创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from "vue"
import { useClassesStore } from "../stores/classes"

const classesStore = useClassesStore()
const currentId = ref(classesStore.currentClassId)
const showCreate = ref(false)
const form = ref({ name: "", grade: "" })

watch(() => classesStore.currentClassId, (val) => {
  currentId.value = val
})

function handleChange(val) {
  classesStore.switchClass(val)
}

async function handleCreate() {
  await classesStore.createClass(form.value)
  form.value = { name: "", grade: "" }
  showCreate.value = false
}
</script>
