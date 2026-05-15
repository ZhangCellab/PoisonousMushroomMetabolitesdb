<template>
  <div class="expandable-field">
    <div class="flex items-start space-x-2">
      <span class="font-bold text-gray-700 min-w-24">{{ label }}:</span>
      <div class="flex-grow">
        <!-- 修改点1：扩展化学字段判断 -->
        <span :class="[
          'text-gray-800 break-words',
          isExpanded ? '' : 'line-clamp-2',
          // 判断是否是化学或特殊格式字段
          isSpecialFormatField ? 'special-format-field' : ''
        ]">
          {{ displayValue }}
        </span>
        <button v-if="shouldShowButton" @click="toggleExpand"
          class="text-primary hover:text-green-700 text-sm font-medium mt-1">
          {{ isExpanded ? 'Less' : 'More' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    default: ''
  },
  limit: {
    type: Number,
    default: 100
  }
})

const isExpanded = ref(false)

// 修改点2：扩展特殊格式字段的判断
const isSpecialFormatField = computed(() => {
  const specialFormatLabels = [
    'smiles',
    'inchi',
    'inchikey',
    'other name',
    'othername',
    'other names',
    'othernames'
  ]
  return specialFormatLabels.includes(props.label.toLowerCase().trim())
})

const shouldShowButton = computed(() => {
  return props.value && props.value.toString().length > props.limit
})

const displayValue = computed(() => {
  if (!props.value) return 'N/A'

  const valueStr = props.value.toString()

  if (isExpanded.value || valueStr.length <= props.limit) {
    return valueStr
  }

  return valueStr.substring(0, props.limit) + '...'
})

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}
</script>

<style scoped>
/* 修改点3：应用特殊格式字段样式 */
.expandable-field .special-format-field {
  /* font-family: 'Courier New', Consolas, monospace;  */
  word-break: break-all;
  /* 允许在任何字符处换行 */
  white-space: pre-wrap;
  /* 保留空白符并允许换行 */
  overflow-wrap: anywhere;
  /* 现代浏览器的智能换行 */
  line-break: anywhere;
  /* 允许在任何地方断行 */
  /*  background-color: #f8f9fa; 
  padding: 4px 6px; 
  border-radius: 4px; 
  border: 1px solid #e5e7eb; 细边框 */
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
}

/* 修改点4：展开状态的特殊处理 */
.expandable-field .special-format-field:not(.line-clamp-2) {
  min-height: 60px;
  /* 展开时有最小高度 */
}

/* 兼容性处理 */
.expandable-field .special-format-field {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  /* 允许连字符断字 */
}

/* 修改点5：为特定字段添加额外样式提示 */
.expandable-field .special-format-field {
  position: relative;
}

/* 可选：为不同字段添加颜色提示 */
.expandable-field :deep(.smiles-field) {
  border-left: 3px solid #10b981;
  /* 绿色边框表示SMILES */
}

.expandable-field :deep(.inchi-field) {
  border-left: 3px solid #3b82f6;
  /* 蓝色边框表示InChI */
}

.expandable-field :deep(.inchikey-field) {
  border-left: 3px solid #8b5cf6;
  /* 紫色边框表示InChIKey */
}

.expandable-field :deep(.othername-field) {
  border-left: 3px solid #f59e0b;
  /* 橙色边框表示Other Name */
}
</style>