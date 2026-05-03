<template>
  <template v-if="isAuthPage">
    <router-view />
  </template>
  <template v-else>
    <AppHeader />
    <router-view />
  </template>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import AppHeader from "./components/AppHeader.vue"

const route = useRoute()
const isAuthPage = computed(() => route.path === "/login" || route.path === "/register")
</script>
