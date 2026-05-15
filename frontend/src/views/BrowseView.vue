<template>
  <div class="bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Title -->
      <h1 class="text-3xl font-bold text-center text-gray-900 mb-8 font-roboto">
        Browse Database
      </h1>

      <!-- Tab Buttons -->
      <div class="flex justify-center mb-8">
        <button @click="activeTab = 'compounds'" :class="[
          'px-6 py-3 border border-r-0 rounded-l-lg font-medium transition-colors duration-300',
          activeTab === 'compounds'
            ? 'bg-primary text-white'
            : 'bg-white text-gray-700 hover:bg-gray-50'
        ]">
          Compounds Overview
        </button>
        <button @click="activeTab = 'mushrooms'" :class="[
          'px-6 py-3 border rounded-r-lg font-medium transition-colors duration-300',
          activeTab === 'mushrooms'
            ? 'bg-primary text-white'
            : 'bg-white text-gray-700 hover:bg-gray-50'
        ]">
          Mushrooms Overview
        </button>
      </div>

      <!-- 添加的搜索框 -->
      <div class="mb-6" :style="{ width: '100%' }">
        <div v-if="activeTab === 'compounds'" class="flex items-center gap-3">
          <div class="flex-grow">
            <input v-model="compoundSearchQuery" type="text" @keyup.enter="searchCompounds"
              :placeholder="'Search by compound name... (e.g., Alpha-Amanitin)'"
              class="w-full rounded-lg border border-gray-300 p-3 focus:ring-2 focus:ring-primary focus:border-primary transition" />
          </div>
          <button @click="searchCompounds" :disabled="!compoundSearchQuery.trim()" :class="[
            'px-6 py-3 font-medium rounded-lg transition whitespace-nowrap',
            compoundSearchQuery.trim()
              ? 'bg-primary text-white hover:bg-green-700'
              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
          ]">
            Search Compounds
          </button>
        </div>
        <div v-if="activeTab === 'mushrooms'" class="flex items-center gap-3">
          <div class="flex-grow">
            <input v-model="mushroomSearchQuery" type="text" @keyup.enter="searchMushrooms"
              :placeholder="'Search by mushroom name... (e.g., Amanita pantherina)'"
              class="w-full rounded-lg border border-gray-300 p-3 focus:ring-2 focus:ring-primary focus:border-primary transition" />
          </div>
          <button @click="searchMushrooms" :disabled="!mushroomSearchQuery.trim()" :class="[
            'px-6 py-3 font-medium rounded-lg transition whitespace-nowrap',
            mushroomSearchQuery.trim()
              ? 'bg-primary text-white hover:bg-green-700'
              : 'bg-gray-200 text-gray-500 cursor-not-allowed'
          ]">
            Search Mushrooms
          </button>
        </div>
      </div>

      <!-- Compounds Table -->
      <div v-if="activeTab === 'compounds'" class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-lightbg">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  #
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Compound Name
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Formula
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  CAS
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in compoundsData.records" :key="item.compoundId" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ index + 1 + (compoundsCurrentPage - 1) * pageSize }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ item.commonName }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.molecularFormula }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.cas || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <router-link :to="`/compound/${item.compoundId}`"
                    class="text-primary hover:text-green-700 font-medium">
                    Details
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="compoundsData.total > pageSize" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-500">
              Showing {{ (compoundsCurrentPage - 1) * pageSize + 1 }} to
              {{ Math.min(compoundsCurrentPage * pageSize, compoundsData.total) }} of
              {{ compoundsData.total }} compounds
            </div>
            <div class="flex space-x-2">
              <button @click="prevCompoundsPage" :disabled="compoundsCurrentPage <= 1" :class="[
                'px-3 py-1 rounded border',
                compoundsCurrentPage <= 1
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              ]">
                Previous
              </button>
              <button @click="nextCompoundsPage" :disabled="compoundsCurrentPage >= compoundsData.pages" :class="[
                'px-3 py-1 rounded border',
                compoundsCurrentPage >= compoundsData.pages
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              ]">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mushrooms Table -->
      <div v-if="activeTab === 'mushrooms'" class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-lightbg">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  #
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mushroom Name
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  NCBI Tax ID
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in mushroomsData.records" :key="item.fungusId" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ index + 1 + (mushroomsCurrentPage - 1) * pageSize }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" v-html="item.fungusName">
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.ncbiTaxonomyId }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <router-link :to="`/fungus/${item.fungusId}`" class="text-primary hover:text-green-700 font-medium">
                    Details
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination for Mushrooms -->
        <div v-if="mushroomsData.total > pageSize" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-500">
              Showing {{ (mushroomsCurrentPage - 1) * pageSize + 1 }} to
              {{ Math.min(mushroomsCurrentPage * pageSize, mushroomsData.total) }} of
              {{ mushroomsData.total }} mushrooms
            </div>
            <div class="flex space-x-2">
              <button @click="prevMushroomsPage" :disabled="mushroomsCurrentPage <= 1" :class="[
                'px-3 py-1 rounded border',
                mushroomsCurrentPage <= 1
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              ]">
                Previous
              </button>
              <button @click="nextMushroomsPage" :disabled="mushroomsCurrentPage >= mushroomsData.pages" :class="[
                'px-3 py-1 rounded border',
                mushroomsCurrentPage >= mushroomsData.pages
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              ]">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-500">Loading data...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as api from '../api'

const router = useRouter()
const activeTab = ref('compounds')
const loading = ref(false)
const pageSize = 10

// 分开管理两个tab的页码
const compoundsCurrentPage = ref(1)
const mushroomsCurrentPage = ref(1)

// 添加的搜索框变量
const compoundSearchQuery = ref('')
const mushroomSearchQuery = ref('')

const compoundsData = ref({
  records: [],
  total: 0,
  pages: 0
})

const mushroomsData = ref({
  records: [],
  total: 0,
  pages: 0
})

const loadCompounds = async (page = 1) => {
  loading.value = true
  try {
    const response = await api.listCompounds(page)
    if (response.data) {
      compoundsData.value = response.data
    }
  } catch (error) {
    console.error('Failed to load compounds:', error)
  } finally {
    loading.value = false
  }
}

const loadMushrooms = async (page = 1) => {
  loading.value = true
  try {
    const response = await api.listFungi(page)
    if (response.data) {
      mushroomsData.value = response.data
    }
  } catch (error) {
    console.error('Failed to load mushrooms:', error)
  } finally {
    loading.value = false
  }
}

// 添加的搜索函数
const searchCompounds = () => {
  if (!compoundSearchQuery.value.trim()) return

  // 跳转到搜索结果页面，使用compound_name作为搜索类型
  router.push({
    path: '/results',
    query: {
      type: 'compound_name',
      q: compoundSearchQuery.value.trim()
    }
  })
}

const searchMushrooms = () => {
  if (!mushroomSearchQuery.value.trim()) return

  // 跳转到搜索结果页面，使用mushroom_name作为搜索类型
  router.push({
    path: '/results',
    query: {
      type: 'mushroom_name',
      q: mushroomSearchQuery.value.trim()
    }
  })
}

const prevCompoundsPage = () => {
  if (compoundsCurrentPage.value > 1) {
    compoundsCurrentPage.value--
    loadCompounds(compoundsCurrentPage.value)
  }
}

const nextCompoundsPage = () => {
  if (compoundsCurrentPage.value < compoundsData.value.pages) {
    compoundsCurrentPage.value++
    loadCompounds(compoundsCurrentPage.value)
  }
}

const prevMushroomsPage = () => {
  if (mushroomsCurrentPage.value > 1) {
    mushroomsCurrentPage.value--
    loadMushrooms(mushroomsCurrentPage.value)
  }
}

const nextMushroomsPage = () => {
  if (mushroomsCurrentPage.value < mushroomsData.value.pages) {
    mushroomsCurrentPage.value++
    loadMushrooms(mushroomsCurrentPage.value)
  }
}

onMounted(() => {
  loadCompounds()
  loadMushrooms()
})

watch(activeTab, (newTab) => {
  if (newTab === 'compounds' && compoundsData.value.records.length === 0) {
    loadCompounds()
  } else if (newTab === 'mushrooms' && mushroomsData.value.records.length === 0) {
    loadMushrooms()
  }
})
</script>