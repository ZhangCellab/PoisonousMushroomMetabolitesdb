<template>
  <div class="bg-gray-50 py-8">
    <div v-if="fungusDetail" class="max-w-7xl mx-auto px-4">

      <!-- Breadcrumb Navigation -->
      <div class="mb-8">
        <nav class="flex" aria-label="Breadcrumb">
          <ol class="inline-flex items-center space-x-1 md:space-x-3">
            <li class="inline-flex items-center">
              <router-link to="/" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-primary">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
                Home
              </router-link>
            </li>
            <li>
              <div class="flex items-center">
                <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd" />
                </svg>
                <router-link to="/browse" class="ml-1 text-sm font-medium text-gray-700 hover:text-primary md:ml-2">
                  Browse
                </router-link>
              </div>
            </li>
            <li aria-current="page">
              <div class="flex items-center">
                <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd" />
                </svg>
                <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2"
                  v-html="fungusDetail.fungusInfo.fungusName">
                </span>
              </div>
            </li>
          </ol>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden mb-8">
        <!-- Card Header -->
        <div class="bg-lightbg px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-800 mb-1" v-html="fungusDetail.fungusInfo.fungusName">
            </h1>
            <p class="text-gray-600 text-sm">
              NCBI Taxonomy ID: {{ fungusDetail.fungusInfo.ncbiTaxonomyId }}
            </p>
          </div>
          <div class="mt-2 sm:mt-0">
            <span
              class="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-primary/10 text-primary">
              Mushroom Details
            </span>
          </div>
        </div>

        <!-- Card Content -->
        <div class="p-6">
          <!-- Taxonomy Info -->
          <div class="bg-cardbg p-4 rounded-lg mb-6">
            <h2 class="font-bold text-gray-700 mb-4">Taxonomic Classification</h2>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div class="text-center p-3 bg-white rounded">
                <span class="block text-xs text-gray-500 font-medium mb-1">Phylum</span>
                <span class="font-medium">{{ fungusDetail.fungusInfo.phylum || 'N/A' }}</span>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <span class="block text-xs text-gray-500 font-medium mb-1">Class</span>
                <span class="font-medium">{{ fungusDetail.fungusInfo.clazz || 'N/A' }}</span>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <span class="block text-xs text-gray-500 font-medium mb-1">Order</span>
                <span class="font-medium">{{ fungusDetail.fungusInfo.orderName || 'N/A' }}</span>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <span class="block text-xs text-gray-500 font-medium mb-1">Family</span>
                <span class="font-medium">{{ fungusDetail.fungusInfo.family || 'N/A' }}</span>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <span class="block text-xs text-gray-500 font-medium mb-1">Genus</span>
                <span class="font-medium">{{ fungusDetail.fungusInfo.genus || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- Associated Compounds Section -->
          <div>
            <div class="flex items-center justify-between mb-6">
              <h2 class="font-bold text-gray-700 text-lg">Associated Compounds</h2>
              <span class="text-sm text-gray-500">
                {{ fungusDetail.compounds ? fungusDetail.compounds.length : 0 }} compounds found
              </span>
            </div>

            <div v-if="fungusDetail.compounds && fungusDetail.compounds.length > 0">
              <!-- Desktop Table -->
              <div class="hidden md:block overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        #
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Compound Name
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        CAS Number
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Molecular Formula
                      </th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Details
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(compound, index) in fungusDetail.compounds" :key="compound.compound_id"
                      class="hover:bg-gray-50">
                      <td class="px-4 py-3 text-sm text-gray-500">
                        {{ index + 1 }}
                      </td>
                      <td class="px-4 py-3">
                        <div class="text-sm font-medium text-gray-900">
                          {{ compound.common_name || 'Unnamed Compound' }}
                        </div>
                        <div v-if="compound.otherName" class="text-xs text-gray-500 mt-1">
                          {{ compound.otherName }}
                        </div>
                      </td>
                      <td class="px-4 py-3 text-sm text-gray-500">
                        {{ compound.cas || 'N/A' }}
                      </td>
                      <td class="px-4 py-3 text-sm text-gray-500">
                        {{ compound.molecular_formula || 'N/A' }}
                      </td>
                      <td class="px-4 py-3">
                        <router-link :to="`/compound/${compound.compound_id}`"
                          class="text-primary hover:text-green-700 font-medium">
                          Details
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Mobile Cards -->
              <div class="md:hidden space-y-4">
                <div v-for="(compound, index) in fungusDetail.compounds" :key="compound.compound_id"
                  class="bg-white border border-gray-200 rounded-lg p-4">
                  <div class="flex justify-between items-start mb-3">
                    <div>
                      <h3 class="font-bold text-gray-900 text-sm">{{ compound.common_name || 'Unnamed Compound' }}</h3>
                      <p v-if="compound.otherName" class="text-xs text-gray-500 mt-1">{{ compound.otherName }}</p>
                    </div>
                    <span class="text-xs text-gray-400">
                      #{{ index + 1 }}
                    </span>
                  </div>

                  <div class="grid grid-cols-2 gap-3 text-sm mb-4">
                    <div>
                      <span class="block text-gray-500 text-xs">CAS Number</span>
                      <span class="font-medium">{{ compound.cas || 'N/A' }}</span>
                    </div>
                    <div>
                      <span class="block text-gray-500 text-xs">Formula</span>
                      <span class="font-medium">{{ compound.molecular_formula || 'N/A' }}</span>
                    </div>
                  </div>

                  <router-link :to="`/compound/${compound.compound_id}`"
                    class="w-full text-center block bg-primary text-white py-2 text-sm rounded hover:bg-green-700">
                    View Details
                  </router-link>
                </div>
              </div>
            </div>

            <!-- No Compounds Found -->
            <div v-else class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-900">No Compounds Found</h3>
              <p class="mt-2 text-sm text-gray-500">
                No compounds are currently associated with this mushroom species.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="text-center py-12">
      <p class="text-gray-500">Loading mushroom details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">Mushroom Not Found</h3>
      <p class="mt-2 text-sm text-gray-500">
        The requested mushroom could not be found.
      </p>
      <div class="mt-6">
        <router-link to="/browse"
          class="inline-flex items-center px-4 py-2 bg-primary text-white text-sm font-medium rounded hover:bg-green-700">
          Browse All Mushrooms
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import * as api from '../api'

const route = useRoute()
const loading = ref(true)
const error = ref(false)
const fungusDetail = ref(null)

const loadFungusDetail = async () => {
  loading.value = true
  error.value = false

  try {
    const response = await api.getFungusDetail(route.params.id)

    if (response.data) {
      fungusDetail.value = response.data

      // 确保 compounds 数组存在
      if (!fungusDetail.value.compounds || !Array.isArray(fungusDetail.value.compounds)) {
        fungusDetail.value.compounds = []
      }
    } else {
      error.value = true
    }
  } catch (err) {
    console.error('Failed to load fungus details:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFungusDetail()
})

watch(() => route.params.id, () => {
  loadFungusDetail()
})
</script>