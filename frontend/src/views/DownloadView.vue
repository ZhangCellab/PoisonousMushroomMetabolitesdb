<template>
  <div class="bg-gray-50 py-12">
    <div class="max-w-6xl mx-auto px-4">
      <!-- 页面标题 -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">Download</h1>
        <!-- <p class="text-gray-600">Access and download the complete mushroom secondary metabolites database</p> -->
      </div>

      <!-- 主信息表格 -->
      <div class="bg-white rounded-2xl border border-gray-200 shadow-xl overflow-hidden mb-8">
        <!-- 表格头部 -->
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col"
                class="px-6 py-4 text-left text-sm font-medium text-gray-700 uppercase tracking-wider border-r border-gray-200 w-1/4">
                File Name
              </th>
              <th scope="col"
                class="px-6 py-4 text-left text-sm font-medium text-gray-700 uppercase tracking-wider border-r border-gray-200 w-1/2">
                Description
              </th>
              <th scope="col"
                class="px-6 py-4 text-left text-sm font-medium text-gray-700 uppercase tracking-wider w-1/4">
                Download
              </th>
            </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-200">
            <!-- 第一行：Compound Data -->
            <tr class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-5 whitespace-nowrap border-r border-gray-200">
                <div class="text-sm font-medium text-gray-900">Compounds.csv</div>
                <!-- <div class="text-xs text-gray-500 mt-1">Size: ~2.4 MB</div> -->
              </td>
              <td class="px-6 py-5 border-r border-gray-200">
                <div class="text-sm text-gray-900">
                  Complete dataset of all documented compounds with detail information
                </div>
                <!-- <div class="text-xs text-gray-500 mt-2">
                  Includes: Compound name, CAS number, SMILES, InChI, molecular formula, source fungi
                </div> -->
              </td>
              <td class="px-6 py-5">
                <button @click="downloadFile('Compounds.csv')"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white transition-colors duration-200"
                  style="background-color: #16A34A;" onmouseover="this.style.backgroundColor='#15803D'"
                  onmouseout="this.style.backgroundColor='#16A34A'">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download
                </button>
              </td>
            </tr>

            <!-- 第二行：Mushroom Data -->
            <tr class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-5 whitespace-nowrap border-r border-gray-200">
                <div class="text-sm font-medium text-gray-900">Mushrooms.csv</div>
                <!-- <div class="text-xs text-gray-500 mt-1">Size: ~1.8 MB</div> -->
              </td>
              <td class="px-6 py-5 border-r border-gray-200">
                <div class="text-sm text-gray-900">
                  Taxonomic information and source fungi for all documented compounds
                </div>
              </td>
              <td class="px-6 py-5">
                <button @click="downloadFile('Mushrooms.csv')"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white transition-colors duration-200"
                  style="background-color: #16A34A;" onmouseover="this.style.backgroundColor='#15803D'"
                  onmouseout="this.style.backgroundColor='#16A34A'">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download
                </button>
              </td>
            </tr>

            <!-- 第三行：Toxicity Data -->
            <tr class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-5 whitespace-nowrap border-r border-gray-200">
                <div class="text-sm font-medium text-gray-900">ToxicityData.csv</div>
                <!-- <div class="text-xs text-gray-500 mt-1">Size: ~3.1 MB</div> -->
              </td>
              <td class="px-6 py-5 border-r border-gray-200">
                <div class="text-sm text-gray-900">
                  Comprehensive toxicity data encompassing LD₅₀, organ toxicity, and mechanisms of action
                </div>
              </td>
              <td class="px-6 py-5">
                <button @click="downloadFile('ToxicityData.csv')"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white transition-colors duration-200"
                  style="background-color: #16A34A;" onmouseover="this.style.backgroundColor='#15803D'"
                  onmouseout="this.style.backgroundColor='#16A34A'">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 提示信息框 -->
      <div class="rounded-2xl shadow-xl p-5 border border-gray-200" style="background-color: #EFF6FF;">
        <h3 class="text-lg font-medium mb-4" style="color: #1E40AF;">Dataset Information</h3>

        <ul class="space-y-3">
          <li class="flex items-start">
            <svg class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" style="color: #1E40AF;" fill="currentColor"
              viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd" />
            </svg>
            <span class="text-sm" style="color: #1C51B9;">All datasets are provided in CSV format for easy
              analysis</span>
          </li>

          <li class="flex items-start">
            <svg class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" style="color: #1E40AF;" fill="currentColor"
              viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                clip-rule="evenodd" />
            </svg>
            <span class="text-sm" style="color: #1C51B9;">Last updated: October, 2025</span>
          </li>

          <li class="flex items-start">
            <svg class="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" style="color: #1E40AF;" fill="currentColor"
              viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                clip-rule="evenodd" />
            </svg>
            <span class="text-sm" style="color: #1C51B9;">Total records: 678 compounds, 235 mushroom species, 915
              toxicity experiments</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
const baseURL = import.meta.env.BASE_URL
const downloadFile = (fileName) => {
  // 创建下载链接
  const link = document.createElement('a')

  // 设置文件路径（相对于public目录）
  link.href = `${baseURL}downloads/${fileName}`

  // 设置下载文件名
  link.download = fileName

  // 添加到DOM并触发点击
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  // 可选：添加下载反馈
  console.log(`Downloading ${fileName}...`)
}
</script>

<style scoped>
/* 精确的按钮颜色和悬停效果 */
button {
  background-color: #16A34A !important;
}

button:hover {
  background-color: #15803D !important;
}

/* 确保表格样式准确 */
th,
td {
  vertical-align: top;
}

/* 提示信息框的精确颜色 */
.info-box {
  background-color: #EFF6FF !important;
}

.info-box h3 {
  color: #1E40AF !important;
}

.info-box span {
  color: #1C51B9 !important;
}

.info-box svg {
  color: #1E40AF !important;
}
</style>