<template>
  <div class="bg-gray-50 py-8">
    <div v-if="detail && detail.info" class="max-w-7xl mx-auto px-4">
      <!-- Header Section -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex flex-col lg:flex-row gap-8">
          <!-- Structure Image -->
          <div class="w-full lg:w-1/3">
            <div class="bg-white border border-gray-200 rounded-lg p-6 flex items-center justify-center">
              <img :src="getImageUrl(detail.info.fileSource)" :alt="detail.info.commonName"
                class="max-w-full h-64 object-contain" />
            </div>
          </div>

          <!-- Compound Info -->
          <div class="w-full lg:w-2/3">
            <h1 class="text-3xl font-bold text-gray-900 mb-4">
              {{ detail.info.commonName }}
            </h1>

            <!-- Basic Info Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div>
                <span class="font-medium text-gray-600">Formula:</span>
                <span class="ml-2 text-gray-800">{{ detail.info.molecularFormula || 'N/A' }}</span>
              </div>
              <div>
                <span class="font-medium text-gray-600">PubChem CID:</span>
                <span class="ml-2 text-gray-800">{{ detail.info.pubchemCid || 'N/A' }}</span>
              </div>
              <div>
                <span class="font-medium text-gray-600">CAS Number:</span>
                <span class="ml-2 text-gray-800">{{ detail.info.cas || 'N/A' }}</span>
              </div>
              <div>
                <span class="font-medium text-gray-600">Taxonomy:</span>
                <span class="ml-2 text-gray-800">{{ detail.info.chemicalTaxonomy || 'N/A' }}</span>
              </div>
            </div>

            <!-- Expandable Fields -->
            <div class="space-y-4 mb-6">
              <ExpandableField label="SMILES" :value="detail.info.smiles" :limit="70" />
              <ExpandableField label="InChI" :value="detail.info.inchi" :limit="80" />
              <ExpandableField label="InChI Key" :value="detail.info.inchikey" :limit="50" />
              <ExpandableField label="Synonyms" :value="detail.info.otherName" :limit="85" />
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Navigation -->
      <div class="bg-white rounded-xl shadow-lg p-4 border border-gray-200">
        <div class="flex flex-wrap gap-2">
          <button v-for="tab in tabs" :key="tab" @click="currentTab = tab" :class="[
            'px-6 py-2 rounded-lg font-medium transition-all duration-300',
            currentTab === tab
              ? 'bg-primary text-white shadow-md'
              : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-300'
          ]">
            {{ tab }}
          </button>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
<<<<<<< HEAD
        
      <!-- Toxicity Tab - Combined Table -->
      <div v-if="currentTab === 'Toxicity'">
        <!-- <h3 class="text-xl font-bold text-gray-900 mb-6">Toxicity Data</h3> -->
        
      <!-- Toxicity Tab - Separate Tables for Each Type -->
      <div v-if="currentTab === 'Toxicity'">
        <h3 class="text-xl font-bold text-gray-900 mb-6">Toxicity Data</h3>
        
        <div v-if="hasToxicityData">
          <!-- 按毒性类型分组的数据 -->
          <template v-for="(toxicityGroup, groupName) in groupedToxicityData" :key="groupName">
            <!-- 只有该组有数据时才显示 -->
            <div v-if="toxicityGroup.length > 0" class="mb-8">
              <!-- 表格标题 -->
              <h4 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                {{ getToxicityGroupTitle(groupName) }}
              </h4>
              
              <!-- 毒性数据表格 -->
              <div class="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route/Test</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organism</th>
                      <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reference</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr 
                      v-for="tox in toxicityGroup" 
                      :key="'tox-' + tox.toxicityId"
                      class="hover:bg-gray-50"
                    >
                      <td class="px-4 py-3 text-sm text-gray-900">{{ tox.toxicityType }}</td>
                      <td class="px-4 py-3 text-sm font-medium text-gray-700">{{ tox.toxicityValue }}</td>
                      <td class="px-4 py-3 text-sm text-gray-600">{{ tox.route || 'N/A' }}</td>
                      <td class="px-4 py-3 text-sm text-gray-600">{{ tox.organism || 'N/A' }}</td>
                      <td class="px-4 py-3 text-sm">
                        <a 
                          v-if="isDoiReference(tox.reference)"
                          :href="getDoiUrl(tox.reference)"
                          target="_blank"
                          rel="noopener noreferrer"
                          class="text-primary hover:underline inline-flex items-center gap-1"
                          title="Click to view paper"
                        >
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                          </svg>
                          {{ tox.reference }}
                        </a>
                        <span v-else class="text-gray-600">{{ tox.reference || 'N/A' }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </template>
          
          <!-- Molecular Activities 表格（始终在最后） -->
          <div v-if="molecularActivitiesCount > 0" class="mt-8">
            <h4 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Molecular Activities</h4>
            
            <div class="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Target</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Function</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Parameter</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organism</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr 
                    v-for="activity in detail.toxicitySection.molecularActivities" 
                    :key="'activity-' + activity.activityId"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-4 py-3 text-sm text-gray-900">{{ activity.target || 'N/A' }}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">{{ activity.function || 'N/A' }}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">{{ activity.parameter || 'N/A' }}</td>
                    <td class="px-4 py-3 text-sm font-medium text-gray-700">{{ activity.value || 'N/A' }}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">{{ activity.organism || 'N/A' }}</td>
                    <td class="px-4 py-3 text-sm">
                      <a 
                        v-if="isDoiReference(activity.source)"
                        :href="getDoiUrl(activity.source)"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary hover:underline inline-flex items-center gap-1"
                        title="Click to view paper"
                      >
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                        </svg>
                        {{ activity.source }}
                      </a>
                      <span v-else class="text-gray-600">{{ activity.source || 'N/A' }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-500">
          No toxicity data available
        </div>
      </div>
      </div>
        
=======

        <!-- Toxicity Tab - Combined Table -->
        <div v-if="currentTab === 'Experimental Toxicity'">
          <!-- Toxicity Tab - Separate Tables for Each Type -->
          <div v-if="currentTab === 'Experimental Toxicity'">
            <h3 class="text-xl font-bold text-gray-900 mb-6">Experimental Toxicity Data</h3>

            <div v-if="hasToxicityData">
              <!-- 按毒性类型分组的数据 -->
              <template v-for="(toxicityGroup, groupName) in groupedToxicityData" :key="groupName">
                <div v-if="toxicityGroup.length > 0" class="mb-8">
                  <h4 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                    {{ getToxicityGroupTitle(groupName) }}
                  </h4>

                  <!-- 检查该组是否有数据 -->
                  <div class="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
                    <table class="min-w-full divide-y divide-gray-200">
                      <thead class="bg-gray-50">
                        <tr>
                          <th v-if="shouldShowColumn(toxicityGroup, 'toxicityType')"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                          <th v-if="shouldShowColumn(toxicityGroup, 'toxicityValue')"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-80">
                            Value/Description</th>
                          <th v-if="shouldShowColumn(toxicityGroup, 'route')"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route/Test</th>
                          <th v-if="shouldShowColumn(toxicityGroup, 'organism')"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organism</th>
                          <th v-if="shouldShowColumn(toxicityGroup, 'reference')"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reference</th>
                          <!-- 仅当该组存在 mechanism 数据时显示此列 -->
                          <th v-if="groupHasMechanismColumn(toxicityGroup)"
                            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                            Mechanism of Toxicity
                          </th>
                        </tr>
                      </thead>
                      <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="tox in toxicityGroup" :key="'tox-' + tox.toxicityId" class="hover:bg-gray-50">
                          <td v-if="shouldShowColumn(toxicityGroup, 'toxicityType')"
                            class="px-4 py-3 text-sm text-gray-900">{{ tox.toxicityType }}</td>
                          <td v-if="shouldShowColumn(toxicityGroup, 'toxicityValue')"
                            class="px-4 py-3 text-sm font-medium text-gray-700">{{ tox.toxicityValue }}</td>
                          <td v-if="shouldShowColumn(toxicityGroup, 'route')" class="px-4 py-3 text-sm text-gray-600">{{
                            tox.route || 'N/A' }}</td>
                          <td v-if="shouldShowColumn(toxicityGroup, 'organism')"
                            class="px-4 py-3 text-sm text-gray-600">{{ tox.organism || 'N/A' }}</td>
                          <td v-if="shouldShowColumn(toxicityGroup, 'reference')" class="px-4 py-3 text-sm">
                            <a v-if="isDoiReference(tox.reference)" :href="getDoiUrl(tox.reference)" target="_blank"
                              rel="noopener noreferrer"
                              class="text-primary hover:underline inline-flex items-center gap-1"
                              title="Click to view paper">
                              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd"
                                  d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                                  clip-rule="evenodd" />
                              </svg>
                              {{ tox.reference }}
                            </a>
                            <span v-else class="text-gray-600">{{ tox.reference || 'N/A' }}</span>
                          </td>
                          <!-- 仅当存在 mechanism 数据时显示此单元格 -->
                          <td v-if="groupHasMechanismColumn(toxicityGroup)" class="px-4 py-3 text-sm max-w-xs">
                            <div v-if="getMechanismByToxicityId(tox.toxicityId)" class="space-y-1">
                              <p class="text-gray-800">{{ getMechanismByToxicityId(tox.toxicityId).Description }}</p>
                              <!-- 用脚注标记替代内联参考文献 -->
                              <div v-if="hasMechanismRefs(getMechanismByToxicityId(tox.toxicityId))"
                                class="text-xs text-gray-500 mt-1">
                                <span v-if="getMechanismByToxicityId(tox.toxicityId).Reference">[1]</span>
                                <span v-if="getMechanismByToxicityId(tox.toxicityId).ExternalLink"
                                  class="ml-1">[2]</span>
                              </div>
                            </div>
                            <span v-else class="text-gray-500">No mechanism data available</span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <!-- Mechanism 参考文献脚注（仅当该组存在 mechanism 时显示） -->
                  <div v-if="groupHasMechanismColumn(toxicityGroup)"
                    class="mt-3 text-xs text-gray-600 border-t border-gray-200 pt-2">
                    <p class="font-medium mb-1">Mechanism References:</p>
                    <div class="space-y-1 pl-4">
                      <p v-for="(tox, index) in toxicityGroup" :key="'ref-' + index">
                        <span v-if="getMechanismByToxicityId(tox.toxicityId)">
                          <template v-if="getMechanismByToxicityId(tox.toxicityId).Reference">
                            <br />[1]
                            <a v-if="isDoiReference(getMechanismByToxicityId(tox.toxicityId).Reference)"
                              :href="getDoiUrl(getMechanismByToxicityId(tox.toxicityId).Reference)" target="_blank"
                              rel="noopener noreferrer" class="text-primary hover:underline">
                              {{ getMechanismByToxicityId(tox.toxicityId).Reference }}
                            </a>
                            <span v-else>{{ getMechanismByToxicityId(tox.toxicityId).Reference }}</span>
                          </template>
                          <template v-if="getMechanismByToxicityId(tox.toxicityId).ExternalLink">
                            <br />[2] External Resource:
                            <a :href="getMechanismByToxicityId(tox.toxicityId).ExternalLink" target="_blank"
                              rel="noopener noreferrer" class="text-primary hover:underline">
                              Link
                            </a>
                          </template>
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Molecular Activities 表格（始终在最后） -->
              <div v-if="molecularActivitiesCount > 0" class="mt-8">
                <h4 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Quantitative Toxicological Targets
                </h4>

                <div class="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'target')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Target</th>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'function')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Function</th>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'parameter')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Parameter</th>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'value')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'organism')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organism</th>
                        <th v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'source')"
                          class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="activity in detail.toxicitySection.molecularActivities"
                        :key="'activity-' + activity.activityId" class="hover:bg-gray-50">
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'target')"
                          class="px-4 py-3 text-sm text-gray-900">{{ activity.target || 'N/A' }}</td>
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'function')"
                          class="px-4 py-3 text-sm text-gray-600">{{ activity.function || 'N/A' }}</td>
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'parameter')"
                          class="px-4 py-3 text-sm text-gray-600">{{ activity.parameter || 'N/A' }}</td>
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'value')"
                          class="px-4 py-3 text-sm font-medium text-gray-700">{{ activity.value || 'N/A' }}</td>
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'organism')"
                          class="px-4 py-3 text-sm text-gray-600">{{ activity.organism || 'N/A' }}</td>
                        <td v-if="shouldShowColumn(detail.toxicitySection.molecularActivities, 'source')"
                          class="px-4 py-3 text-sm">
                          <a v-if="isDoiReference(activity.source)" :href="getDoiUrl(activity.source)" target="_blank"
                            rel="noopener noreferrer"
                            class="text-primary hover:underline inline-flex items-center gap-1"
                            title="Click to view paper">
                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd"
                                d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                                clip-rule="evenodd" />
                            </svg>
                            {{ activity.source }}
                          </a>
                          <span v-else class="text-gray-600">{{ activity.source || 'N/A' }}</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8 text-gray-500">
              No experimental toxicity data available
            </div>
          </div>
        </div>

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
        <!-- Source Fungi Tab -->
        <div v-else-if="currentTab === 'Source Fungi'">
          <h3 class="text-xl font-bold text-gray-900 mb-6">Source Fungi</h3>
          <div v-if="detail.fungi && detail.fungi.length">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="fungus in detail.fungi" :key="fungus.fungusId" @click="goToFungusDetail(fungus.fungusId)"
                class="bg-cardbg border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer hover:border-primary hover:bg-gray-50">
                <h4 class="font-bold text-lg text-primary mb-2" v-html="fungus.fungusName">
                </h4>
                <div class="text-sm text-gray-600">
                  <p><span class="font-medium">Family:</span> {{ fungus.family }}</p>
                  <p><span class="font-medium">Genus:</span> {{ fungus.genus }}</p>
                  <p><span class="font-medium">NCBI ID:</span> {{ fungus.ncbiTaxonomyId }}</p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            No source fungi data available
          </div>
        </div>

        <!-- ADMET Tab -->
        <div v-else-if="currentTab === 'ADMET'">
          <h3 class="text-xl font-bold text-gray-900 mb-6">ADMET Properties</h3>

          <!-- ADMET分类按钮 -->
          <div class="mb-8">
            <div class="flex flex-wrap gap-2 mb-4">
              <button v-for="category in admetCategories" :key="category.key"
                @click="selectedAdmetCategory = category.key" :class="[
                  'px-4 py-2 rounded-lg font-medium transition-all duration-300 text-sm',
                  selectedAdmetCategory === category.key
                    ? 'bg-primary text-white shadow-md'
                    : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-300'
                ]">
                {{ category.label }}
              </button>
            </div>
          </div>

          <!-- 显示选中的ADMET分类数据 -->
          <div v-if="detail.admet && detail.admet[selectedAdmetCategory]">
            <div class="overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/5">
                      Property
                    </th>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/5">
                      Value
                    </th>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/5">
                      Comment
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(value, propertyKey) in detail.admet[selectedAdmetCategory]" :key="propertyKey"
                    class="hover:bg-gray-50 transition-colors duration-150">
                    <td class="px-6 py-4 text-sm font-medium text-gray-900">
                      {{ formatPropertyKey(propertyKey) }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-700 font-medium">
                      {{ formatAdmetValue(propertyKey, value) }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-600 whitespace-pre-line">
                      {{ getAdmetComment(propertyKey) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- ADMET数据来源说明 -->
            <div class="text-xs text-gray-500 text-center mt-4">
              Calculated by
              <a href="https://admetlab3.scbdd.com" target="_blank" class="text-[#22C55E] hover:underline font-medium">
                ADME Tlab 3.0
              </a>
              , DOI: 10.1093/nar/gkae236
            </div>
          </div>

          <!-- 没有数据的情况 -->
          <div v-else-if="detail.admet" class="text-center py-8 text-gray-500">
            No {{ getCategoryLabel(selectedAdmetCategory) }} data available
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            No ADMET data available
          </div>
        </div>

        <!-- Physicochemical Properties Tab -->
        <div v-else-if="currentTab === 'Physicochemical Property'">
          <h3 class="text-xl font-bold text-gray-900 mb-6">Physicochemical Properties</h3>
          <div v-if="detail.admet && detail.admet.physicochemicalProperty">
            <!-- 表格容器 -->
            <div class="overflow-x-auto border border-gray-200 rounded-lg">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/5">
                      Property
                    </th>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/5">
                      Value
                    </th>
                    <th scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/5">
                      Comment
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(value, key) in detail.admet.physicochemicalProperty" :key="key"
                    class="hover:bg-gray-50 transition-colors duration-150">
                    <td class="px-6 py-4 text-sm font-medium text-gray-900">
                      {{ formatPropertyKey(key) }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-700 font-medium">
                      {{ formatPhysicochemicalValue(key, value) }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-600 whitespace-pre-line">
                      {{ getPhysicochemicalComment(key) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- 添加说明文字 -->
            <div class="text-xs text-gray-500 text-center mt-2">
              Calculated by
              <a href="https://admetlab3.scbdd.com" target="_blank" class="text-[#22C55E] hover:underline font-medium">
                ADME Tlab 3.0
              </a>
              , DOI: 10.1093/nar/gkae236
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            No physicochemical properties data available
          </div>
        </div>

      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">Loading compound details...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as api from '../api'
import ExpandableField from '../components/ExpandableField.vue'
import mechData from '../assets/mech.json'

const route = useRoute()
const router = useRouter()
const detail = ref(null)
const currentTab = ref('Physicochemical Property')
const tabs = ['Physicochemical Property', 'Experimental Toxicity', 'ADMET', 'Source Fungi']
const selectedAdmetCategory = ref('absorption')

// 构建毒性ID到机制的映射 (toxicity_id 为字符串)
const mechanismMap = computed(() => {
  const map = {}
  if (mechData?.data) {
    mechData.data.forEach(item => {
      // 确保 toxicity_id 存在且唯一（取首次出现）
      if (item.toxicity_id && !map[item.toxicity_id]) {
        map[item.toxicity_id] = item
      }
    })
  }
  return map
})

// 根据毒性ID获取机制数据 (处理ID类型转换)
const getMechanismByToxicityId = (toxicityId) => {
  if (!toxicityId) return null
  // 尝试字符串和数字两种形式匹配
  const idStr = toxicityId.toString()
  return mechanismMap.value[idStr] || null
}

// ADMET分类定义（按要求的顺序）
const admetCategories = ref([
  { key: 'absorption', label: 'Absorption' },
  { key: 'distribution', label: 'Distribution' },
  { key: 'metabolism', label: 'Metabolism' },
  { key: 'excretion', label: 'Excretion' },
  { key: 'toxicology', label: 'Toxicology' }
])

// Physicochemical Properties Comment数据
const physicochemicalComments = ref({
  'MW': 'Contain hydrogen atoms. Optimal: 100~600',
  'Vol': 'Van der Waals volume',
  'Dense': 'Density = MW / Volume',
  'nHA': 'Number of hydrogen bond acceptors. Optimal: 0~12',
  'nHD': 'Number of hydrogen bond donors. Optimal: 0~7',
  'TPSA': 'Topological Polar Surface Area. Optimal: 0~140',
  'nRot': 'Number of rotatable bonds. Optimal: 0~11',
  'nRing': 'Number of rings. Optimal: 0~6',
  'MaxRing': 'Number of atoms in the biggest ring. Optimal: 0~18',
  'nHet': 'Number of heteroatoms. Optimal: 1~15',
  'fChar': 'Formal charge. Optimal: -4 ~ 4',
  'nRig': 'Number of rigid bonds. Optimal: 0~30',
  'Flex': 'Flexibility = nRot / nRig',
  'nStereo': 'Stereo Centers. Optimal: ≤ 2',
  'logS': 'The logarithm of aqueous solubility value.',
  'logD': 'The logarithm of the n-octanol/water distribution coefficient.',
  'logP': 'The logarithm of the n-octanol/water distribution coefficients at pH=7.4.',
  'mp': 'The predicted melting point of a compound is expressed in degrees Celsius (°C). Melting points below 25°C are classified as liquids, while melting points above 25°C are classified as solids.',
  'bp': 'The predicted melting point of a compound is expressed in degrees Celsius (°C). A normal boiling point below 25°C is categorized as a gas.',
  'pka_acidic': 'Acid-base dissociation constant (pKa) value represents the strength of a drug molecule\'s acidity or basicity.',
  'pka_basic': 'Acid-base dissociation constant (pKa) value represents the strength of a drug molecule\'s acidity or basicity.'
})

// ADMET Comment数据
const admetComments = ref({
  // Absorption
  'caco2': 'Optimal: higher than -5.15 Log unit',
  'MDCK': '\n■ low permeability: < 2 × 10⁻⁶ cm/s \n■ medium permeability: 2-20 × 10⁻⁶ cm/s \n■ high passive permeability: > 20 × 10⁻⁶ cm/s',
  'hia': '\n■ Human Intestinal Absorption \n■ Category 1: HIA+ (HIA < 30%); \n■ Category 0: HIA- (HIA >= 30%); \n■ The output value is the probability of being HIA+',
  'PAMPA': '\n■ The experimental data for Peff was logarithmically transformed (logPeff). \n■ Molecules with log Peff values below 2.0 were classified as low-permeability (Category 0), while those with log Peff values exceeding 2.5 were classified as high-permeability (Category 1).',
  'f20': '\n■ 20% Bioavailability \n■ Category 1: F 20%+ (bioavailability < 20%); \n■ Category 0: F 20%- (bioavailability ≥ 20%); \n■ The output value is the probability of being F 20%+',
  'f30': '\n■ 30% Bioavailability \n■ Category 1: F 30%+ (bioavailability < 30%); \n■ Category 0: F 30%- (bioavailability ≥ 30%); \n■ The output value is the probability of being F 30%+',
  'f50': '\n■ 50% Bioavailability \n■ Category 1: F 50%+ (bioavailability < 50%); \n■ Category 0: F 50%- (bioavailability ≥ 50%); \n■ The output value is the probability of being F 50%+',

  // Distribution
  'logVDss': '\n■ Volume Distribution \n■ Optimal: 0.04-20 L/kg',
  'Fu': '\n■ The fraction unbound in plasma \n■ Low: <5%; Middle: 5~20%; High: > 20%',
  'PPB': '\n■ Plasma Protein Binding Optimal: < 90%. \n■ Drugs with high protein-bound may have a low therapeutic index.',
  'BBB': '\n■ Blood-Brain Barrier Penetration \n■ Category 1: BBB+; Category 0: BBB-; \n■ The output value is the probability of being BBB+',

  // Metabolism
  'CYP1A2-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP1A2-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP2C19-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP2C19-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP2C9-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP2C9-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP2D6-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP2D6-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP3A4-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP3A4-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP2B6-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'CYP2B6-sub': '\n■ Category 1: Substrate; Category 0: Non-substrate; \n■ The output value is the probability of being substrate.',
  'CYP2C8-inh': '\n■ Category 1: Inhibitor; Category 0: Non-inhibitor; \n■ The output value is the probability of being inhibitor.',
  'MRP1': '\n■ Category 0: Non-inhibitor; Category 1: inhibitor. \n■ The output value is the probability of being inhibitor, within the range of 0 to 1.',
  'OATP1B1': '\n■ Category 0: Non-inhibitor; Category 1: inhibitor. \n■ The output value is the probability of being inhibitor, within the range of 0 to 1.',
  'OATP1B3': '\n■ Category 0: Non-inhibitor; Category 1: inhibitor. \n■ The output value is the probability of being inhibitor, within the range of 0 to 1.',
  'pgp_inh': '\n■ Category 1: Inhibitor; \n■ Category 0: Non-inhibitor; \n■ The output value is the probability of being Pgp-inhibitor',
  'pgp_sub': '\n■ Category 1: substrate; \n■ Category 0: Non-substrate; \n■ The output value is the probability of being Pgp-substrate',
  'BCRP': '\n■ Category 0: Non-inhibitor; Category 1: inhibitor. \n■ The output value is the probability of being inhibitor, within the range of 0 to 1.',
  'BSEP': '\n■ Category 0: Non-inhibitor; Category 1: inhibitor. \n■ The output value is the probability of being inhibitor, within the range of 0 to 1.',
  'LM-human': '\n■ human liver microsomal (HLM) stability \n■ Category 0: stable+ (HLM > 30 min); Category 1: unstable- (HLM ≤ 30 min). The output value is the probability of human liver microsomal instability, where a value closer to 1 indicates a higher likelihood of instability. The range is between 0 and 1.',

  // Excretion
  't0.5': '\n■ The unit of predicted T1/2 is hours. \n■ ultra-short half-life drugs: 1/2 < 1 hour; short half-life drugs: T1/2 between 1-4 hours; intermediate short half-life drugs: T1/2 between 4-8 hours; long half-life drugs: T1/2 > 8 hours.',
  'cl-plasma': '\n■ The unit of predicted CLplasma penetration is ml/min/kg. >15 ml/min/kg: high clearance; 5-15 ml/min/kg: moderate clearance; < 5 ml/min/kg: low clearance.',

  // Toxicology
  'A549': '\n■ Category 0: non-cytotoxicity (-); \n■ Category 1: cytotoxicity (+). \n■ The output value is the probability of being ototoxicity (+), within the range of 0 to 1.',
  'Ames': '\n■ Category 1: Ames positive(+); \n■ Category 0: Ames negative(-); \n■ The output value is the probability of being toxic.',
  'Carcinogenicity': '\n■ Category 1: carcinogens; \n■ Category 0: non-carcinogens; \n■ The output value is the probability of being toxic.',
  'DILI': '\n■ Drug Induced Liver Injury. \n■ Category 1: drugs with a high risk of DILI; \n■ Category 0: drugs with no risk of DILI. \n■ The output value is the probability of being toxic.',
  'EC': '\n■ Category 1: corrosives; Category 0: noncorrosives; \n■ The output value is the probability of being corrosives.',
  'EI': '\n■ Category 1: irritants; Category 0: nonirritants; \n■ The output value is the probability of being irritants.',
  'FDAMDD': '\n■ FDA Maximum (Recommended) Daily Dose. \n■ Category 1: FDAMDD (+); \n■ Category 0: FDAMDD (-); The output value is the probability of being positive.',
  'Genotoxicity': '\n■ Category 0: non-Genotoxicity (-); \n■ Category 1: Genotoxicity (+). \n■ The output value is the probability of being ototoxicity (+), within the range of 0 to 1.',
  'H-HT': '\n■ Category 1: H-HT positive(+); \n■ Category 0: H-HT negative(-); \n■ The output value is the probability of being toxic.',
  'HEK293': '\n■ Category 0: non-cytotoxicity (-); \n■ Category 1: cytotoxicity (+). \n■ The output value is the probability of being ototoxicity (+), within the range of 0 to 1.',
  'Hematotoxicity': '\n■ Category 0: non-hematotoxicity (-); \n■ Category 1: hematotoxicity (+). \n■ The output value is the probability of being hematotoxicity (+), within the range of 0 to 1.',
  'hERG-10um': '\n■ Molecules with IC50 ≤10 µM are classified as hERG+ (Category 1), \n■ and molecules with IC50 > 10µM are classified as hERG- (Category 0). \n■ The output value is the probability of being hERG+, within the range of 0 to 1.',
  'hERG': '\n■ Molecules with IC50 ≤10µM or ≥50% inhibition at 10 µM were classified as hERG+ (Category 1), \n■ while molecules with IC50 >10µM or < 50% inhibition at 10µM were classified as hERG- (Category 0). \n■ The output value is the probability of being hERG+, within the range of 0 to 1.',
  'Nephrotoxicity-DI': '\n■ Category 0: non-nephrotoxic (-); \n■ Category 1: nephrotoxic (+). \n■ The output value is the probability of being nephrotoxic (+), within the range of 0 to 1.',
  'Neurotoxicity-DI': '\n■ Category 0: non-neurotoxic (-); \n■ Category 1: neurotoxic (+). \n■ The output value is the probability of being neurotoxic (+), within the range of 0 to 1.',
  'Ototoxicity': '\n■ Category 0: non-ototoxicity (-); \n■ Category 1: ototoxicity (+). \n■ The output value is the probability of being ototoxicity (+), within the range of 0 to 1.',
  'Respiratory': '\n■ Category 1: respiratory toxicants; \n■ Category 0: non-respiratory toxicants. \n■ The output value is the probability of being toxic, within the range of 0 to 1.',
  'ROA': '\n■ Category 0: low-toxicity, > 500 mg/kg; \n■ Category 1: high-toxicity; < 500 mg/kg. \n■ The output value is the probability of being toxic, within the range of 0 to 1.',
  'RPMI-8226': '\n■ Category 0: non-cytotoxicity (-); \n■ Category 1: cytotoxicity (+). \n■ The output value is the probability of being ototoxicity (+), within the range of 0 to 1.',
  'SkinSen': '\n■ Category 1: Sensitizer; \n■ Category 0: Non-sensitizer. \n■ The output value is the probability of being toxic, within the range of 0 to 1.'
})

// 计算按毒性类型分组的数据
const groupedToxicityData = computed(() => {
  if (!detail.value || !detail.value.toxicitySection || !detail.value.toxicitySection.generalToxicity) {
    return {}
  }
<<<<<<< HEAD
  
  // 定义毒性类型分组顺序
  const typeOrder = [
    'General Toxicity',
    'Gastrointestinal Toxicity', 
    'Neurotoxicity',
    'Cytotoxicity',
    'Hepatotoxicity',
    'Other Toxicity'
  ]
  
=======

  // 定义毒性类型分组顺序
  const typeOrder = [
    'General Toxicity',
    'Gastrointestinal Toxicity',
    'Neurotoxicity',
    'Cytotoxicity',
    'Hepatotoxicity',
    'Nephrotoxicity',
    'Other Toxicity'
  ]

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
  // 初始化分组
  const groups = {}
  typeOrder.forEach(type => {
    groups[type] = []
  })
<<<<<<< HEAD
  
  // 按毒性类型分组数据
  detail.value.toxicitySection.generalToxicity.forEach(tox => {
    const toxicityType = tox.toxicityType || 'Other Toxicity'
    
=======

  // 按毒性类型分组数据
  detail.value.toxicitySection.generalToxicity.forEach(tox => {
    const toxicityType = tox.toxicityType || 'Other Toxicity'

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
    // 检查毒性类型是否在预定义的类型中，否则归类为"Other Toxicity"
    if (typeOrder.includes(toxicityType)) {
      groups[toxicityType].push(tox)
    } else {
      groups['Other Toxicity'].push(tox)
    }
  })
<<<<<<< HEAD
  
=======

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
  return groups
})

// 获取毒性分组的标题
const getToxicityGroupTitle = (groupName) => {
  const titleMap = {
    'General Toxicity': 'General Toxicity',
    'Gastrointestinal Toxicity': 'Gastrointestinal Toxicity',
    'Neurotoxicity': 'Neurotoxicity',
    'Cytotoxicity': 'Cytotoxicity',
    'Hepatotoxicity': 'Hepatotoxicity',
<<<<<<< HEAD
=======
    'Nephrotoxicity': 'Nephrotoxicity',
>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
    'Other Toxicity': 'Other Toxicity'
  }
  return titleMap[groupName] || groupName
}

// 计算Molecular Activities数量
const molecularActivitiesCount = computed(() => {
  return detail.value?.toxicitySection?.molecularActivities?.length || 0
})

// 修改hasToxicityData计算属性
const hasToxicityData = computed(() => {
  if (!detail.value || !detail.value.toxicitySection) return false
<<<<<<< HEAD
  
  // 检查是否有任何毒性数据（包括分组后的数据）
  const hasGeneralToxicity = detail.value.toxicitySection.generalToxicity?.length > 0
  const hasMolecularActivities = molecularActivitiesCount.value > 0
  
  return hasGeneralToxicity || hasMolecularActivities
})

=======

  // 检查是否有任何毒性数据（包括分组后的数据）
  const hasGeneralToxicity = detail.value.toxicitySection.generalToxicity?.length > 0
  const hasMolecularActivities = molecularActivitiesCount.value > 0

  return hasGeneralToxicity || hasMolecularActivities
})

// 新增：判断是否应该显示某列
const shouldShowColumn = (dataArray, columnName) => {
  if (!dataArray || !Array.isArray(dataArray) || dataArray.length === 0) {
    return false
  }

  // 检查该列是否在所有行中都有数据
  // 如果某行有数据（不为空或N/A），则显示该列
  return dataArray.some(item => {
    const value = item[columnName]
    return value !== null &&
      value !== undefined &&
      value !== '' &&
      value !== 'N/A' &&
      !(typeof value === 'string' && value.trim() === '')
  })
}

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
const loadCompoundDetail = async () => {
  try {
    const response = await api.getCompoundDetail(route.params.id)
    if (response.data) {
      detail.value = response.data
      // 如果有ADMET数据，检查默认分类是否存在，如果不存在则选择第一个存在的分类
      if (detail.value.admet) {
        const firstAvailableCategory = admetCategories.value.find(
          cat => detail.value.admet[cat.key]
        )
        if (firstAvailableCategory && !detail.value.admet[selectedAdmetCategory.value]) {
          selectedAdmetCategory.value = firstAvailableCategory.key
        }
      }
    }
  } catch (error) {
    console.error('Failed to load compound details:', error)
  }
}

<<<<<<< HEAD
=======
const baseURL = import.meta.env.BASE_URL
>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
const getImageUrl = (source) => {
  return source ? `${baseURL}images/${source}.png` : '${baseURL}images/placeholder.png'
}

// 新增：跳转到真菌详情页面的函数
const goToFungusDetail = (fungusId) => {
  router.push(`/fungus/${fungusId}`)
}

// 获取分类的显示标签
const getCategoryLabel = (categoryKey) => {
  const category = admetCategories.value.find(cat => cat.key === categoryKey)
<<<<<<< HEAD
  return category ? category.label : formatPropertyKey(categoryKey) // 修复这里
=======
  return category ? category.label : formatPropertyKey(categoryKey)
>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
}

// 格式化属性键名
const formatPropertyKey = (key) => {
  // 处理各种格式的键名
  const formatMap = {
    'MW': 'Molecular Weight',
    'Vol': 'Molecular Volume',
    'Dense': 'Density',
    'nHA': 'Hydrogen Bond Acceptors',
    'nHD': 'Hydrogen Bond Donors',
    'TPSA': 'Topological Polar Surface Area',
    'nRot': 'Rotatable Bonds',
    'nRing': 'Number of Rings',
    'MaxRing': 'Maximum Ring Size',
    'nHet': 'Heteroatoms',
    'fChar': 'Formal Charge',
    'nRig': 'Rigid Bonds',
    'Flex': 'Flexibility Index',
    'nStereo': 'Stereocenters',
    'logS': 'Log Solubility',
    'logD': 'Log Distribution Coefficient',
    'logP': 'Log Partition Coefficient',
    'mp': 'Melting Point (°C)',
    'bp': 'Boiling Point (°C)',
    'pka_acidic': 'pKa (Acidic)',
    'pka_basic': 'pKa (Basic)',
    't0.5': 'Half-life (h)',
    'cl-plasma': 'Plasma Clearance (mL/min/kg)',
    'logVDss': 'Log Volume of Distribution',
    'Fu': 'Fraction Unbound (%)',
    'PPB': 'Plasma Protein Binding (%)',
    'BBB': 'Blood-Brain Barrier Penetration',
    'hia': 'Human Intestinal Absorption',
    'PAMPA': 'Parallel Artificial Membrane Permeability',
    'caco2': 'Caco-2 Permeability (log Papp)',
    'MDCK': 'MDCK Permeability (log Papp)',
    'f20': 'F20 (20% FBS)',
    'f30': 'F30 (30% FBS)',
    'f50': 'F50 (50% FBS)',
    'pgp_inh': 'P-gp Inhibitor',
    'pgp_sub': 'P-gp Substrate',
    'A549': 'A549 Cell Toxicity',
    'Ames': 'Ames Test',
    'Carcinogenicity': 'Carcinogenicity',
    'DILI': 'Drug-Induced Liver Injury',
    'EC': 'Eye Corrosion',
    'EI': 'Eye Irritation',
    'FDAMDD': 'FDA Maximum Daily Dose',
    'Genotoxicity': 'Genotoxicity',
    'H-HT': 'Human Hepatotoxicity',
    'HEK293': 'HEK293 Cell Toxicity',
    'Hematotoxicity': 'Hematotoxicity',
    'hERG': 'hERG Inhibition',
    'hERG-10um': 'hERG Inhibition (10µM)',
    'Nephrotoxicity-DI': 'Nephrotoxicity',
    'Neurotoxicity-DI': 'Neurotoxicity',
    'Ototoxicity': 'Ototoxicity',
    'Respiratory': 'Respiratory Toxicity',
    'ROA': 'Route of Administration',
    'RPMI-8226': 'RPMI-8226 Cell Toxicity',
    'SkinSen': 'Skin Sensitization',
    'LM-human': 'Liver Microsomal Stability (human)',
    'CYP1A2-inh': 'CYP1A2 Inhibitor',
    'CYP1A2-sub': 'CYP1A2 Substrate',
    'CYP2C19-inh': 'CYP2C19 Inhibitor',
    'CYP2C19-sub': 'CYP2C19 Substrate',
    'CYP2C9-inh': 'CYP2C9 Inhibitor',
    'CYP2C9-sub': 'CYP2C9 Substrate',
    'CYP2D6-inh': 'CYP2D6 Inhibitor',
    'CYP2D6-sub': 'CYP2D6 Substrate',
    'CYP3A4-inh': 'CYP3A4 Inhibitor',
    'CYP3A4-sub': 'CYP3A4 Substrate',
    'CYP2B6-inh': 'CYP2B6 Inhibitor',
    'CYP2B6-sub': 'CYP2B6 Substrate',
    'CYP2C8-inh': 'CYP2C8 Inhibitor',
    'MRP1': 'MRP1 Substrate',
    'OATP1B1': 'OATP1B1 Substrate',
    'OATP1B3': 'OATP1B3 Substrate',
    'BCRP': 'BCRP Substrate',
    'BSEP': 'BSEP Inhibitor'
  }

  return formatMap[key] || key
}

// 获取物理化学属性的Comment
const getPhysicochemicalComment = (key) => {
  return physicochemicalComments.value[key] || 'No comment available'
}

// 获取ADMET属性的Comment
const getAdmetComment = (key) => {
  return admetComments.value[key] || 'No comment available'
}

// 格式化物理化学属性值
const formatPhysicochemicalValue = (key, value) => {
  if (value === null || value === undefined || value === '') return 'N/A'

  // 根据属性类型添加单位
  const unitMap = {
    'MW': ' g/mol',
    'Vol': ' Å³',
    'Dense': ' g/cm³',
    'mp': '°C',
    'bp': '°C',
    'logS': '',
    'logD': '',
    'logP': '',
    'pka_acidic': '',
    'pka_basic': ''
  }

  const unit = unitMap[key] || ''
  return `${value}${unit}`
}

// 格式化ADMET属性值
const formatAdmetValue = (key, value) => {
  if (value === null || value === undefined || value === '') return 'N/A'

  // 对于概率值，显示为百分比
  const probabilityKeys = [
    'hia', 'f20', 'f30', 'f50', 'BBB', 'PAMPA', 'pgp_inh', 'pgp_sub',
    'CYP1A2-inh', 'CYP1A2-sub', 'CYP2C19-inh', 'CYP2C19-sub',
    'CYP2C9-inh', 'CYP2C9-sub', 'CYP2D6-inh', 'CYP2D6-sub',
    'CYP3A4-inh', 'CYP3A4-sub', 'CYP2B6-inh', 'CYP2B6-sub',
    'CYP2C8-inh', 'MRP1', 'OATP1B1', 'OATP1B3', 'BCRP', 'BSEP',
    'LM-human', 'A549', 'Ames', 'Carcinogenicity', 'DILI', 'EC',
    'EI', 'FDAMDD', 'Genotoxicity', 'H-HT', 'HEK293', 'Hematotoxicity',
    'hERG-10um', 'hERG', 'Nephrotoxicity-DI', 'Neurotoxicity-DI',
    'Ototoxicity', 'Respiratory', 'ROA', 'RPMI-8226', 'SkinSen'
  ]

  if (probabilityKeys.includes(key)) {
    const numericValue = parseFloat(value)
    if (!isNaN(numericValue)) {
      return `${(numericValue * 100).toFixed(1)}%`
    }
  }

  // 对于特定属性添加单位
  const unitMap = {
    't0.5': ' h',
    'cl-plasma': ' mL/min/kg',
    'logVDss': ' L/kg',
    'Fu': '%',
    'PPB': '%',
    'caco2': ' log unit',
    'MDCK': ' log unit'
  }

  const unit = unitMap[key] || ''
  return `${value}${unit}`
}

// 检查是否为DOI引用
const isDoiReference = (reference) => {
  if (!reference) return false
  // 检查字符串是否包含DOI或doi（不区分大小写）
  return reference.toLowerCase().includes('doi:') ||
    reference.toLowerCase().includes('doi ')
}

// 获取DOI链接
const getDoiUrl = (doiText) => {
  if (!doiText) return ''

  // 提取DOI号码（去掉"DOI:"前缀和空格）
  let doiNumber = doiText.trim()

  // 去掉开头的"DOI:"或"doi:"（不区分大小写）
  if (doiNumber.toLowerCase().startsWith('doi:')) {
    doiNumber = doiNumber.substring(4).trim()
  } else if (doiNumber.toLowerCase().startsWith('doi ')) {
    doiNumber = doiNumber.substring(4).trim()
  }

  // 去掉末尾的句号
  if (doiNumber.endsWith('.')) {
    doiNumber = doiNumber.slice(0, -1)
  }

  // 构建DOI URL
  return `https://doi.org/${doiNumber}`
}

// 修改判断函数：当整列的 mechanism 数据都为空时才隐藏该列
const groupHasMechanismColumn = (toxicityGroup) => {
  // 检查该组中是否至少有一条毒性数据有mechanism信息
  return toxicityGroup.some(tox => {
    const mechanism = getMechanismByToxicityId(tox.toxicityId);
    // 如果有mechanism数据且Description不为空，则显示该列
    return mechanism && mechanism.Description && mechanism.Description.trim() !== '';
  });
};

// 原有的 groupHasMechanism 函数可以保留，但修改判断条件
const groupHasMechanism = (toxicityGroup) => {
  return toxicityGroup.some(tox => {
    const mechanism = getMechanismByToxicityId(tox.toxicityId);
    // 修改判断条件：只有当Description不为空时才认为有mechanism数据
    return mechanism && mechanism.Description && mechanism.Description.trim() !== '';
  });
};

// 判断 mechanism 是否包含参考文献
const hasMechanismRefs = (mechanism) => {
  return mechanism && (mechanism.Reference || mechanism.ExternalLink)
}

onMounted(() => {
  loadCompoundDetail()
})

watch(() => route.params.id, () => {
  loadCompoundDetail()
  selectedAdmetCategory.value = 'absorption'
})
</script>