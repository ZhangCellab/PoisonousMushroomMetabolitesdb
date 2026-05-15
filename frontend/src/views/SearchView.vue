<template>
  <div class="py-12">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Title -->
      <h1 class="text-3xl font-bold text-center text-gray-900 mb-8 font-roboto">
        Search Our Database
      </h1>

      <!-- Text Search Card -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-8">
        <!-- Search Controls -->
        <div class="flex flex-col md:flex-row gap-4 mb-4">
          <!-- Search Type -->
          <select v-model="searchType"
            class="w-full md:w-1/4 rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition">
            <option value="compound_name">Compound Name</option>
            <option value="cas">CAS Number</option>
            <option value="family">Family</option>
            <option value="genus">Genus</option>
            <option value="mushroom_name">Species</option>
          </select>

          <!-- Search Input -->
          <div class="relative flex-grow">
            <input v-model="searchQuery" type="text" @keyup.enter="handleTextSearch"
              placeholder="Search by compound name, CAS number, or species..."
              class="w-full rounded-lg border-gray-300 border p-3 pl-4 focus:ring-2 focus:ring-primary focus:border-primary transition" />
          </div>

          <!-- Search Button -->
          <button @click="handleTextSearch"
            class="w-full md:w-auto px-8 py-3 bg-primary text-white font-medium rounded-lg hover:bg-green-700 transition">
            Search
          </button>
        </div>

        <!-- Examples -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-600 mt-4">
          <button @click="searchExample('compound_name', 'α-Amanitin')"
            class="bg-gray-50 p-2 rounded hover:bg-gray-100 transition text-left">
            Compound: e.g.: <span class="text-primary font-medium">α-Amanitin</span>
          </button>
          <button @click="searchExample('cas', '23109-05-9')"
            class="bg-gray-50 p-2 rounded hover:bg-gray-100 transition text-left">
            CAS Number: e.g.: <span class="text-primary font-medium">23109-05-9</span>
          </button>
          <button @click="searchExample('mushroom_name', 'Amanita pantherina')"
            class="bg-gray-50 p-2 rounded hover:bg-gray-100 transition text-left">
            Species: e.g.: <span class="text-primary font-medium">Amanita pantherina</span>
          </button>
          <div class="space-y-2">
            <button @click="searchExample('family', 'Amanitaceae')"
              class="w-full bg-gray-50 p-2 rounded hover:bg-gray-100 transition text-left">
              Family: e.g. <span class="text-primary font-medium">Amanitaceae</span>
            </button>
            <button @click="searchExample('genus', 'Amanita')"
              class="w-full bg-gray-50 p-2 rounded hover:bg-gray-100 transition text-left">
              Genus: e.g. <span class="text-primary font-medium">Amanita</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Structure Search Card -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <!-- Card Header -->
        <div class="bg-lightbg px-6 py-4 border-b border-gray-200">
          <h2 class="font-bold text-gray-800 text-lg">Structure Search</h2>
          <p class="text-sm text-gray-500 mt-1">Draw or import chemical structure to search for similar compounds</p>
        </div>

        <!-- Card Body -->
        <div class="p-6">
          <!-- Ketcher Editor -->
          <KetcherLocalEditor ref="ketcherEditor" width="100%" height="400px" @smiles-updated="handleSmilesUpdate"
            class="mb-6" />

          <!-- Similarity Search Button -->
          <div class="flex justify-between items-center mt-6">
            <div class="text-sm text-gray-500">
              Current SMILES: <code
                class="bg-gray-100 px-2 py-1 rounded text-xs max-w-xs truncate inline-block">{{ currentSmiles || 'Structure not drawn' }}</code>
            </div>
            <button @click="handleStructureSearch" :disabled="!currentSmiles" :class="[
              'px-8 py-3 font-medium rounded-lg transition',
              currentSmiles
                ? 'bg-accent text-white hover:bg-green-500 shadow-md hover:shadow-lg'
                : 'bg-gray-200 text-gray-500 cursor-not-allowed'
            ]">
              Search
            </button>
          </div>

          <!-- Structure Search Tips -->
          <div class="mt-6 pt-6 border-t border-gray-200">
            <h3 class="text-sm font-medium text-gray-700 mb-2">How to use:</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• Draw chemical structures using the left toolbar</li>
              <li>• Click on the tools in the toolbar to select different drawing modes</li>
              <li>• Use the 'Get SMILES' button to obtain the SMILES representation of the current structure</li>
              <li>• Click the "Search" button to find compounds with similar structures</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import KetcherLocalEditor from '../components/KetcherLocalEditor.vue'

const router = useRouter()
const ketcherEditor = ref(null)

const searchType = ref('compound_name')
const searchQuery = ref('')
const currentSmiles = ref('')

const handleTextSearch = () => {
  if (!searchQuery.value.trim()) return

  router.push({
    path: '/results',
    query: {
      type: searchType.value,
      q: searchQuery.value.trim()
    }
  })
}

const handleSmilesUpdate = (smiles) => {
  currentSmiles.value = smiles
}

const handleStructureSearch = () => {
  if (!currentSmiles.value) {
    alert('Please first draw the chemical structure or input SMILES')
    return
  }

  router.push({
    path: '/results',
    query: {
      type: 'smiles',
      q: currentSmiles.value
    }
  })
}

// 添加示例搜索函数
const searchExample = (type, query) => {
  // 更新当前搜索类型和查询词（可选，让用户看到变化）
  searchType.value = type
  searchQuery.value = query

  // 直接跳转到搜索结果页面
  router.push({
    path: '/results',
    query: {
      type: type,
      q: query
    }
  })
}

// 示例SMILES（用于测试）
const exampleSmiles = ref(' ')

// 加载示例结构（可选）
onMounted(() => {
  // 延迟设置示例结构，确保Ketcher已加载
  setTimeout(() => {
    if (ketcherEditor.value) {
      ketcherEditor.value.setSmiles(exampleSmiles.value)
      currentSmiles.value = exampleSmiles.value
    }
  }, 2000)
})
</script>