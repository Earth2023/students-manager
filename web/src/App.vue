<template>
  <router-view v-if="!isAuthPage" />
  <router-view v-else />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import AppHeader from "./components/AppHeader.vue"

const route = useRoute()
const isAuthPage = computed(() => route.path === "/login" || route.path === "/register")
</script>
