<template>
  <div class="bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4">

      <!-- Compound Results -->
      <div v-if="isCompoundResult">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 font-roboto">
          Compound Search Results
        </h2>

        <!-- No Results -->
        <div v-if="!results.length" class="text-center py-12">
          <p class="text-gray-500">No compounds found matching your search</p>
        </div>

        <!-- Results Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="item in results" :key="item.compoundId"
            class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
            <!-- Card Header -->
            <div class="bg-lightbg px-4 py-3 flex justify-between items-center">
              <span class="font-medium text-gray-800 truncate" :title="item.commonName">
                {{ item.commonName }}
              </span>
              <span class="text-sm text-gray-500 bg-white px-2 py-1 rounded whitespace-nowrap">
                {{ item.cas || 'No CAS' }}
              </span>
            </div>

            <!-- Structure Image -->
            <div class="h-48 p-4 flex items-center justify-center bg-white">
              <img :src="getImageUrl(item.fileSource)" :alt="item.commonName"
                class="max-h-full max-w-full object-contain">
            </div>

            <!-- Card Info -->
            <div class="px-4 py-3 border-t border-gray-100">
              <p class="text-sm text-darktext mb-2">
                <span class="font-medium">Formula:</span> {{ item.molecularFormula || 'N/A' }}
              </p>

              <!-- Similarity for structure search -->
              <p v-if="searchType === 'smiles' && item.similarity" class="text-sm text-darktext">
                <span class="font-medium">Similarity:</span> {{ formatSimilarity(item.similarity) }}
              </p>
            </div>

            <!-- View Details Button -->
            <router-link :to="`/compound/${item.compoundId}`"
              class="block w-full text-center bg-primary text-white py-3 hover:bg-green-700 transition font-medium">
              View Details
            </router-link>
          </div>
        </div>
      </div>

      <!-- Mushroom Name Results -->
      <div v-else-if="searchType === 'mushroom_name'">
        <!-- Results Header Card - 独立标题卡片 -->
        <div v-if="results.length" class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden mb-8">
          <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 class="font-bold text-gray-800 text-lg mb-1">Mushroom Search Results</h2>
              <p class="text-gray-600 text-sm">
                Results for your query: "<span class="font-medium text-primary">{{ route.query.q }}</span>"
              </p>
            </div>
            <div class="mt-2 sm:mt-0">
              <span
                class="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-primary/10 text-primary">
                {{ results.length }} result{{ results.length > 1 ? 's' : '' }} found
              </span>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="!results.length" class="text-center py-12">
          <p class="text-gray-500">No fungi found matching your search</p>
        </div>

        <!-- Results Content - 移除了标题的蘑菇卡片 -->
        <div v-else v-for="fungus in results" :key="fungus.fungusInfo.fungusId" class="mb-8">
          <!-- Mushroom Card -->
          <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
            <!-- Card Content -->
            <div class="p-6">
              <!-- Mushroom Info Header -->
              <div class="bg-cardbg p-4 rounded-lg mb-6">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between">
                  <h3 class="text-xl font-bold text-primary mb-2 md:mb-0" v-html="fungus.fungusInfo.fungusName">
                  </h3>
                  <span class="text-gray-600">
                    NCBI ID: {{ fungus.fungusInfo.ncbiTaxonomyId }}
                  </span>
                </div>
              </div>

              <!-- Taxonomy Info -->
              <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
                <div class="text-center p-3 bg-gray-50 rounded">
                  <span class="block text-xs text-gray-500 font-medium mb-1">Phylum</span>
                  <span class="font-medium">{{ fungus.fungusInfo.phylum }}</span>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded">
                  <span class="block text-xs text-gray-500 font-medium mb-1">Class</span>
                  <span class="font-medium">{{ fungus.fungusInfo.clazz }}</span>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded">
                  <span class="block text-xs text-gray-500 font-medium mb-1">Order</span>
                  <span class="font-medium">{{ fungus.fungusInfo.orderName }}</span>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded">
                  <span class="block text-xs text-gray-500 font-medium mb-1">Family</span>
                  <span class="font-medium">{{ fungus.fungusInfo.family }}</span>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded">
                  <span class="block text-xs text-gray-500 font-medium mb-1">Genus</span>
                  <span class="font-medium">{{ fungus.fungusInfo.genus }}</span>
                </div>
              </div>

              <!-- Known Compounds Table -->
              <h4 class="font-bold text-gray-700 mb-4">Known Compounds</h4>
              <div v-if="fungus.compounds && fungus.compounds.length" class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Compound Name</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">CAS</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Formula</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Details</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="cpd in fungus.compounds" :key="cpd.compound_id">
                      <td class="px-4 py-3 text-sm text-gray-900">{{ cpd.common_name }}</td>
                      <td class="px-4 py-3 text-sm text-gray-500">{{ cpd.cas || 'N/A' }}</td>
                      <td class="px-4 py-3 text-sm text-gray-500">{{ cpd.molecular_formula }}</td>
                      <td class="px-4 py-3">
                        <router-link :to="`/compound/${cpd.compound_id}`"
                          class="text-primary hover:text-green-700 font-medium">
                          Details
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-4 text-gray-500">
                No compounds found for this fungus
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Family/Genus Results -->
      <div v-else-if="['family', 'genus'].includes(searchType)">
        <!-- Results Header Card - 统一格式的标题卡片 -->
        <div v-if="results.length" class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden mb-8">
          <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 class="font-bold text-gray-800 text-lg mb-1 capitalize">
                {{ searchType }} Search Results
              </h2>
              <p class="text-gray-600 text-sm">
                Results for your query: "<span class="font-medium text-primary">{{ route.query.q }}</span>"
              </p>
            </div>
            <div class="mt-2 sm:mt-0">
              <span
                class="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-primary/10 text-primary">
                {{ results.length }} result{{ results.length > 1 ? 's' : '' }} found
              </span>
            </div>
          </div>
        </div>

        <div v-if="!results.length" class="text-center py-12">
          <p class="text-gray-500">No fungi found matching your search</p>
        </div>

        <div v-else>
          <!-- 移除了原来的标题区域 -->
          <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
            <!-- Card Content -->
            <div class="p-6">
              <!-- Taxonomy Summary -->
              <div v-if="results.length > 0" class="flex flex-wrap gap-4 mb-6 pb-4 border-b">
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">Phylum:</span>
                  <span class="font-medium">{{ results[0].phylum }}</span>
                </div>
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">Class:</span>
                  <span class="font-medium">{{ results[0].clazz }}</span>
                </div>
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">Order:</span>
                  <span class="font-medium">{{ results[0].orderName }}</span>
                </div>
                <div v-if="searchType === 'genus'" class="flex items-center">
                  <span class="text-sm text-gray-500 mr-2">Family:</span>
                  <span class="font-medium">{{ results[0].family }}</span>
                </div>
              </div>

              <!-- Results Table -->
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th v-if="searchType === 'family'"
                        class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Genus
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Fungus Name
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        NCBI ID
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Detail
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                    <tr v-for="item in results" :key="item.fungusId">
                      <td v-if="searchType === 'family'" class="px-4 py-3 text-sm font-medium">
                        {{ item.genus }}
                      </td>
                      <td class="px-4 py-3 text-sm" v-html="item.fungusName">
                      </td>
                      <td class="px-4 py-3 text-sm text-gray-500">
                        {{ item.ncbiTaxonomyId }}
                      </td>
                      <td class="px-4 py-3">
                        <router-link :to="`/fungus/${item.fungusId}`"
                          class="text-primary hover:text-green-700 font-medium">
                          Details
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-500">Loading results...</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import * as api from '../api'

const route = useRoute()
const loading = ref(false)
const results = ref([])
const searchType = ref('')

const isCompoundResult = computed(() => {
  return ['compound_name', 'cas', 'smiles'].includes(searchType.value)
})

const fetchResults = async () => {
  loading.value = true
  searchType.value = route.query.type || ''
  const query = route.query.q || ''

  if (!query) {
    results.value = []
    loading.value = false
    return
  }

  try {
    let response
    switch (searchType.value) {
      case 'compound_name':
        response = await api.searchCompoundByName(query)
        break
      case 'cas':
        response = await api.searchCompoundByCas(query)
        break
      case 'smiles':
        response = await api.searchBySmiles(query)
        // 结构搜索返回数据需要处理
        if (response.data && Array.isArray(response.data)) {
          results.value = response.data
        }
        loading.value = false
        return
      case 'mushroom_name':
        response = await api.searchFungusByName(query)
        break
      case 'genus':
        response = await api.searchFungusByGenus(query)
        break
      case 'family':
        response = await api.searchFungusByFamily(query)
        break
      default:
        response = null
    }

    if (response && response.data) {
      results.value = Array.isArray(response.data) ? response.data : [response.data]
    } else {
      results.value = []
    }
  } catch (error) {
    console.error('Search Failed:', error)
    results.value = []
  } finally {
    loading.value = false
  }
}

const baseURL = import.meta.env.BASE_URL
const getImageUrl = (source) => {
  return source ? `${baseURL}images/${source}.png` : '${baseURL}images/placeholder.png'
}

const formatSimilarity = (val) => {
  if (val === null || val === undefined || val < 0) return 'N/A'

  const num = parseFloat(val)

  if (num > 1.0) return '⭐⭐⭐⭐⭐'
  if (num >= 0.90) return '⭐⭐⭐⭐⭐'
  if (num >= 0.80) return '⭐⭐⭐⭐'
  if (num >= 0.70) return '⭐⭐⭐'
  if (num >= 0.60) return '⭐⭐'
  return '⭐'
}

onMounted(() => {
  fetchResults()
})

watch(() => route.query, () => {
  fetchResults()
})
</script>