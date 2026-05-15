<template>
  <nav class="bg-[#166534] shadow-md border-b border-gray-100 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-24">
        <div class="flex items-center">
          <router-link to="/"
            class="font-pacifico text-white text-5xl hover:opacity-90 transition-opacity duration-200">
            PMMdb
          </router-link>
        </div>

        <div class="hidden sm:flex sm:items-center sm:space-x-8">
          <router-link v-for="item in navItems" :key="item.name" :to="item.path" :class="[
            'px-3 py-2 rounded-md text-m font-medium transition-colors duration-200',
            $route.name === item.name
              ? 'text-primary bg-white'
              : 'text-gray-100 hover:text-white hover:bg-white/20'
          ]">
            {{ item.name }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
const navItems = [
  { name: 'Home', path: '/' },
  { name: 'Search', path: '/search' },
  { name: 'Browse', path: '/browse' },
  { name: 'Submit', path: '/submit' },
  { name: 'Download', path: '/download' },
  { name: 'Statistics', path: '/statistics' },
  { name: 'Help', path: '/help' }
]
</script>