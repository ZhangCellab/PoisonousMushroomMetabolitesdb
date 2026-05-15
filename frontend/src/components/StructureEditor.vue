<template>
  <div class="structure-editor">
    <div :id="containerId" class="ketcher-container border border-gray-300 rounded-lg"></div>
    <div class="mt-4 flex space-x-4">
      <button @click="handleGetSmiles" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200">
        Get SMILES
      </button>
      <button @click="handleClear" class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200">
        Clear
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, defineEmits } from 'vue'
import { initializeKetcher, getSmilesFromKetcher } from '../api/ketcher'

const props = defineProps({
  containerId: {
    type: String,
    default: 'ketcher-editor'
  }
})

const emit = defineEmits(['smiles-updated', 'structure-cleared'])

let ketcherInstance = null

const initializeEditor = async () => {
  try {
    ketcherInstance = await initializeKetcher(props.containerId)
    console.log('Ketcher initialized successfully')
  } catch (error) {
    console.error('Failed to initialize Ketcher:', error)
  }
}

const handleGetSmiles = async () => {
  if (ketcherInstance) {
    const smiles = await getSmilesFromKetcher(ketcherInstance)
    if (smiles) {
      emit('smiles-updated', smiles)
    }
  }
}

const handleClear = () => {
  if (ketcherInstance) {
    ketcherInstance.clear()
    emit('structure-cleared')
  }
}

onMounted(() => {
  initializeEditor()
})

onBeforeUnmount(() => {
  ketcherInstance = null
})
</script>