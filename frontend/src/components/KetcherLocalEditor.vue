<template>
  <div class="ketcher-local-editor">
    <!-- Ketcher iframe -->
    <iframe ref="ketcherIframe" :src="ketcherUrl" :style="{ width, height }"
      class="ketcher-iframe border border-gray-300 rounded-lg" frameborder="0" @load="onIframeLoad"></iframe>

    <!-- 控制按钮 -->
    <div class="mt-4 flex flex-wrap gap-3 items-center">
      <button @click="getSmiles" :disabled="!ketcherReady" :class="[
        'px-4 py-2 rounded font-medium transition',
        ketcherReady
          ? 'bg-primary text-white hover:bg-green-700'
          : 'bg-gray-200 text-gray-500 cursor-not-allowed'
      ]">
        Get SMILES
      </button>

      <button @click="clearStructure" :disabled="!ketcherReady" :class="[
        'px-4 py-2 rounded font-medium transition',
        ketcherReady
          ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          : 'bg-gray-100 text-gray-400 cursor-not-allowed'
      ]">
        Clear
      </button>

      <div class="flex-1">
        <textarea v-model="smilesInput" placeholder="Or directly input the SMILES string .." rows="2"
          class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-2 focus:ring-primary focus:border-primary"
          @input="handleSmilesInput"></textarea>
      </div>

      <div v-if="loading" class="flex items-center text-sm text-gray-500">
        <svg class="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        Loading...
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
      Unable to load chemical editor. Please ensure that the Ketcher file is correctly placed in the<code
        class="bg-red-100 px-1">/public/ketcher/</code>directory.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineEmits } from 'vue'

const props = defineProps({
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '400px'
  },
  initialSmiles: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['smiles-updated', 'structure-cleared', 'editor-ready'])

// Refs
const ketcherIframe = ref(null)
const ketcherReady = ref(false)
const loading = ref(true)
const error = ref(false)
const smilesInput = ref(props.initialSmiles || '')

const baseURL = import.meta.env.BASE_URL  //动态访问资源路径
// Ketcher URL - 使用本地文件
const ketcherUrl = computed(() => {
  return 'ketcher/index.html'
})

// Ketcher API方法
const ketcherMethods = {
  // 获取SMILES
  async getSmilesFromKetcher() {
    if (!ketcherReady.value || !ketcherIframe.value) {
      console.warn('Ketcher not ready or iframe not available')
      return null
    }

    try {
      const ketcherWindow = ketcherIframe.value.contentWindow

      // 方法1: 直接调用Ketcher API
      if (ketcherWindow.ketcher && typeof ketcherWindow.ketcher.getSmiles === 'function') {
        return ketcherWindow.ketcher.getSmiles()
      }

      // 方法2: 通过postMessage通信
      ketcherWindow.postMessage({
        type: 'getSmiles',
        timestamp: Date.now()
      }, '*')

      return await new Promise((resolve) => {
        const messageHandler = (event) => {
          if (event.data && event.data.type === 'smilesResponse') {
            window.removeEventListener('message', messageHandler)
            resolve(event.data.smiles)
          }
        }
        window.addEventListener('message', messageHandler)

        // 超时处理
        setTimeout(() => {
          window.removeEventListener('message', messageHandler)
          resolve('')
        }, 1000)
      })
    } catch (err) {
      console.error('Failed to get SMILES from Ketcher:', err)
      return null
    }
  },

  // 设置SMILES
  async setSmilesToKetcher(smiles) {
    if (!ketcherReady.value || !ketcherIframe.value || !smiles) {
      return
    }

    try {
      const ketcherWindow = ketcherIframe.value.contentWindow

      // 方法1: 直接调用Ketcher API
      if (ketcherWindow.ketcher && typeof ketcherWindow.ketcher.setMolecule === 'function') {
        ketcherWindow.ketcher.setMolecule(smiles)
        return true
      }

      // 方法2: 通过postMessage通信
      ketcherWindow.postMessage({
        type: 'setMolecule',
        smiles: smiles,
        timestamp: Date.now()
      }, '*')

      return true
    } catch (err) {
      console.error('Failed to set SMILES to Ketcher:', err)
      return false
    }
  },

  // 清空画布
  async clearKetcher() {
    if (!ketcherReady.value || !ketcherIframe.value) {
      return
    }

    try {
      const ketcherWindow = ketcherIframe.value.contentWindow

      // 方法1: 直接调用Ketcher API
      if (ketcherWindow.ketcher && typeof ketcherWindow.ketcher.setMolecule === 'function') {
        ketcherWindow.ketcher.setMolecule('')
        return true
      }

      // 方法2: 通过postMessage通信
      ketcherWindow.postMessage({
        type: 'clear',
        timestamp: Date.now()
      }, '*')

      return true
    } catch (err) {
      console.error('Failed to clear Ketcher:', err)
      return false
    }
  }
}

// 事件处理
const onIframeLoad = async () => {
  loading.value = true
  error.value = false

  try {
    // 等待Ketcher初始化
    await new Promise((resolve) => {
      const checkKetcher = () => {
        if (ketcherIframe.value && ketcherIframe.value.contentWindow) {
          const ketcherWindow = ketcherIframe.value.contentWindow

          // 检查Ketcher是否可用
          if (ketcherWindow.ketcher || ketcherWindow.document.readyState === 'complete') {
            ketcherReady.value = true
            resolve()
          } else {
            setTimeout(checkKetcher, 100)
          }
        }
      }

      // 设置超时
      setTimeout(() => {
        if (!ketcherReady.value) {
          console.warn('Ketcher loading timeout')
          resolve()
        }
      }, 100000)

      checkKetcher()
    })

    // 监听来自Ketcher的消息
    window.addEventListener('message', handleKetcherMessage)

    // 如果有初始SMILES，设置到Ketcher
    if (props.initialSmiles) {
      await ketcherMethods.setSmilesToKetcher(props.initialSmiles)
      smilesInput.value = props.initialSmiles
    }

    emit('editor-ready')
  } catch (err) {
    console.error('Failed to load Ketcher:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const handleKetcherMessage = (event) => {
  // 处理来自Ketcher的消息
  if (event.data && event.data.type === 'smilesChanged') {
    const smiles = event.data.smiles
    smilesInput.value = smiles
    emit('smiles-updated', smiles)
  }
}

const getSmiles = async () => {
  const smiles = await ketcherMethods.getSmilesFromKetcher()
  if (smiles) {
    smilesInput.value = smiles
    emit('smiles-updated', smiles)
  }
}

const clearStructure = async () => {
  const success = await ketcherMethods.clearKetcher()
  if (success) {
    smilesInput.value = ''
    emit('structure-cleared')
  }
}

const handleSmilesInput = () => {
  // 去抖处理
  clearTimeout(handleSmilesInput.debounce)
  handleSmilesInput.debounce = setTimeout(async () => {
    if (smilesInput.value) {
      const success = await ketcherMethods.setSmilesToKetcher(smilesInput.value)
      if (success) {
        emit('smiles-updated', smilesInput.value)
      }
    }
  }, 5000)
}

// 生命周期
onMounted(() => {
  // 设置iframe加载超时
  setTimeout(() => {
    if (loading.value && !ketcherReady.value) {
      loading.value = false
      error.value = true
      console.error('Ketcher loading timeout')
    }
  }, 200000)
})

// 暴露方法给父组件
defineExpose({
  getSmiles,
  clearStructure,
  setSmiles: (smiles) => {
    smilesInput.value = smiles
    return ketcherMethods.setSmilesToKetcher(smiles)
  },
  getSmilesInput: () => smilesInput.value
})
</script>

<style scoped>
.ketcher-iframe {
  background-color: white;
}

.ketcher-local-editor {
  width: 100%;
}

/* 加载动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>