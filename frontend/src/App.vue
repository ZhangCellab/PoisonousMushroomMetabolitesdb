<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <NavBar />
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </main>
    <Footer v-if="shouldShowFooter" />
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const shouldShowFooter = computed(() => {
  // 在这里定义哪些路由不需要Footer
  const hideRoutes = ['/']
  return !hideRoutes.includes(route.path)
})
</script>