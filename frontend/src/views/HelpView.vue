<template>
  <div class="bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-center text-gray-900 mb-8 font-roboto">
          Help
        </h1>
      </div>

      <!-- Frequently Asked Questions Card -->
      <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
        <!-- Card Header -->
        <div class="bg-white from-primary/10 to-primary/5 p-6 border-b border-gray-200">
          <div class="flex items-center gap-4">
            <!-- Logo Placeholder -->
            <div class="flex-shrink-0 w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="none"
                version="1.1" width="16" height="16" viewBox="0 0 16 16">
                <path
                  d="M8,16Q10.1875,16.03125,12,17.0625Q13.8125,18.125,14.9375,20Q16,21.90625,16,24Q16,26.09375,14.9375,28Q13.8125,29.875,12,30.9375Q10.1875,31.96875,8,32Q5.8125,31.96875,4,30.9375Q2.1875,29.875,1.0625,28Q0,26.09375,0,24Q0,21.90625,1.0625,20Q2.1875,18.125,4,17.0625Q5.8125,16.03125,8,16ZM5.3125,26.84375Q5.5,27.375,5.9375,27.6875Q6.375,28,6.96875,28L8.78125,28Q9.625,27.96875,10.1875,27.40625Q10.71875,26.875,10.75,26.03125Q10.71875,24.90625,9.75,24.3125L8.75,23.75Q8.6875,23.0625,8,23Q7.3125,23.0625,7.25,23.75L7.25,24.15625Q7.25,24.59375,7.625,24.8125L9,25.625Q9.25,25.75,9.25,26.03125Q9.21875,26.46875,8.78125,26.5L6.96875,26.5Q6.78125,26.5,6.71875,26.34375L6.71875,26.28125Q6.40625,25.65625,5.75,25.84375Q5.125,26.125,5.28125,26.78125L5.3125,26.84375ZM7,21Q7,21.4375,7.28125,21.71875Q7.5625,22,8,22Q8.4375,22,8.71875,21.71875Q9,21.4375,9,21Q9,20.5625,8.71875,20.28125Q8.4375,20,8,20Q7.5625,20,7.28125,20.28125Q7,20.5625,7,21Z"
                  fill="#16A34A" fill-opacity="1" style="mix-blend-mode:passthrough"
                  transform="matrix(1,0,0,-1,0,32)" />
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Frequently Asked Questions</h2>
            </div>
          </div>
        </div>

        <!-- Q&A Accordion Section -->
        <div>
          <!-- Q1 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(1)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q1</span>
                </span>
                <span class="font-medium text-gray-900">Get an overview of PMMdb from the Home page</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 1 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 1" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-4">
                <div>
                  <h3 class="font-medium text-gray-900 mb-2">Overview:</h3>
                  <p class="text-gray-700">
                    Secondary metabolites of poisonous mushrooms are the primary causative agents of poisoning
                    incidents, and their unique chemical structures also render them a valuable source for discovering
                    novel active molecules. The current version of the database documents 678 secondary metabolites
                    derived from 235 poisonous mushroom species, accompanied by 915 toxicological data records. In
                    summary, this database provides a convenient and user-friendly interface for querying, browsing, and
                    visualizing detailed information on these metabolites, and will be of help in elucidating poisoning
                    mechanisms, facilitating toxin prevention and control, and supporting risk assessment.
                  </p>
                </div>

                <div>
                  <h3 class="font-medium text-gray-900 mb-2">The homepage is displayed in the following Fig 1-1:</h3>
                  <ul class="list-disc pl-5 space-y-1 text-gray-700 mb-4">
                    <li>Main functions of the database are provided in menu bar form (boxed in red).</li>
                    <li>Introduction and overview for PMMdb.</li>
                    <li>Quick search for users.</li>
                  </ul>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                    <img :src="getImageUrl('helpimg1.1')" alt="PMMdb Homepage" class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 1-1. homepage</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Q2 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(2)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q2</span>
                </span>
                <span class="font-medium text-gray-900">How to implement Compound search and Mushroom search in Search
                  page?</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 2 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 2" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-4">
                <div>
                  <h3 class="font-medium text-gray-900 mb-2">The search page is displayed in Fig 2-1:</h3>
                  <h4 class="font-medium text-gray-800 mb-2">Compound or Mushroom search:</h4>
                  <ol class="list-decimal pl-5 space-y-2 text-gray-700">
                    <li><strong>Select the search type.</strong> Choose a category from the dropdown menu (five options
                      are provided: Compound Name, CAS Number, Mushroom Species, Genus, and Family).</li>
                    <li><strong>Input a keyword.</strong> Enter your query in the search box corresponding to the
                      selected category.</li>
                    <li><strong>Keyword examples.</strong></li>
                    <li><strong>Structure Search.</strong> Draw or import a chemical structure to search for compounds.
                      Please follow the operation instructions listed below the canvas (e.g., use the toolbar to draw
                      and click "Similarity Search").</li>
                  </ol>
                </div>

                <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                  <img :src="getImageUrl('helpimg2.1')" alt="PMMdb Search Page" class="max-w-full h-auto rounded" />
                  <p class="text-center text-sm text-gray-500 mt-2">Fig 2-1. search page</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Q3 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(3)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q3</span>
                </span>
                <span class="font-medium text-gray-900">How to read the search results?</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 3 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 3" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-6">
                <!-- Compound Search Results -->
                <div>
                  <h3 class="font-medium text-gray-900 mb-3">Compound Search Result Display</h3>
                  <div class="space-y-3">
                    <div>
                      <p class="text-gray-700"><strong>1. Exact Search:</strong> The system directly displays the
                        information card for the specific compound matching your query.</p>
                      <p class="text-gray-700"><strong>Similarity Search:</strong> The system displays compounds with a
                        structural similarity score greater than 0.7 relative to your query. The star rating indicates
                        the degree of similarity:</p>
                      <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-700">
                        <li>3 stars: 0.7 -- 0.8</li>
                        <li>4 stars: 0.8 -- 0.9</li>
                        <li>5 stars: 0.9 -- 1.0</li>
                      </ul>
                    </div>
                    <p class="text-gray-700"><strong>2. Click to link to Detail page</strong></p>
                  </div>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mt-4">
                    <img :src="getImageUrl('helpimg3.1')" alt="Compound Search Results"
                      class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 3-1. Result page of Compound search</p>
                  </div>
                </div>

                <!-- Mushroom Search Results -->
                <div>
                  <h3 class="font-medium text-gray-900 mb-3">Mushroom Search Result Display:</h3>
                  <ol class="list-decimal pl-5 space-y-2 text-gray-700">
                    <li>The result table (including mushroom taxonomy information).</li>
                    <li>Click to link to the Compound Detail page.</li>
                  </ol>
                  <p class="text-gray-700 italic mt-2">Note: The layout for Species and Genus search results is similar
                    to the current interface.</p>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mt-4">
                    <img :src="getImageUrl('helpimg3.2')" alt="Mushroom Search Results"
                      class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 3-2. Result page of Mushroom search</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Q4 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(4)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q4</span>
                </span>
                <span class="font-medium text-gray-900">How to read Detail page?</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 4 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 4" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-4">
                <div>
                  <p class="text-gray-700 mb-4">
                    In the Detail page, you can access comprehensive information about secondary metabolites,
                    categorized into "Compound Basic Information", "Physicochemical Property", "Experimental Toxicity",
                    "ADMET", and
                    "Source Fungi", as well as the references for the data sources in each section.
                  </p>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mb-4">
                    <img :src="getImageUrl('helpimg4.1')" alt="Compound Detail Page"
                      class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 4-1. Compound Detail page</p>
                  </div>

                  <ol class="list-decimal pl-5 space-y-3 text-gray-700">
                    <li>
                      <strong>Compound Basic Information:</strong> Including the 2D chemical structure, Molecular
                      Formula, Molecular Descriptors (SMILES, InChI, InChI Key), Synonyms, and external IDs (PubChem
                      CID, CAS Number).
                    </li>
                    <li>
                      <strong>Information Categories:</strong> Click the corresponding tabs to view specific details:
                      "Physicochemical Property", "Experimental Toxicity", "ADMET", and "Source Fungi".
                    </li>
                    <li>
                      <strong>Experimental Toxicity Details:</strong>
                      <p class="mt-1">This section presents the general toxicity, cytotoxicity, organ toxicity, and
                        specific toxicity mechanisms of the compound. All information is derived from literature
                        reports. Key metrics are explained as follows:</p>
                      <ul class="list-disc pl-5 mt-2 space-y-1">
                        <li><strong>General Toxicity:</strong> Displays metrics such as LD50. For example, in "LD50 =
                          129 mg/kg (Oral, Rat)", the information in parentheses indicates the route of administration
                          and the experimental animal.</li>
                        <li><strong>Cytotoxicity:</strong> Displays metrics such as IC50. For example, in "IC50 = 0.13 ±
                          0.02 µM (MTT, HF)", the information in parentheses indicates the experimental method and the
                          cell line.</li>
                      </ul>
                    </li>
                  </ol>
                </div>
              </div>
            </div>
          </div>

          <!-- Q5 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(5)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q5</span>
                </span>
                <span class="font-medium text-gray-900">How to use Browse page?</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 5 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 5" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-4">
                <div>
                  <p class="text-gray-700 mb-4">
                    The <strong>Browse</strong> page presents comprehensive lists of all data records stored in the
                    database. Users can navigate through the data using the following controls:
                  </p>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mb-4">
                    <img :src="getImageUrl('helpimg5.1')" alt="Browse Page" class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 5-1. Browse page</p>
                  </div>

                  <ol class="list-decimal pl-5 space-y-3 text-gray-700">
                    <li><strong>Switch Browse Mode:</strong> Click the toggle buttons to switch between "Compounds
                      Overview" (to browse secondary metabolites) and "Mushrooms Overview" (to browse mushroom species).
                    </li>
                    <li><strong>Page Navigation:</strong> Use the "Previous" and "Next" buttons located at the bottom
                      right to navigate through the multiple pages of records.</li>
                    <li><strong>View Details:</strong> Click the "Details" link in the "Action" column to navigate to
                      the specific Detail page for that compound or mushroom.</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>

          <!-- Q6 -->
          <div class="border-b border-gray-200">
            <button @click="toggleAccordion(6)"
              class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
              <div class="flex items-center gap-3">
                <span class="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                  <span class="text-primary font-bold">Q6</span>
                </span>
                <span class="font-medium text-gray-900">How to download the details of the compounds, mushrooms and
                  compounds data?</span>
              </div>
              <svg :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-300',
                activeAccordion === 6 ? 'rotate-180' : ''
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-show="activeAccordion === 6" class="px-6 pb-6 pt-2 bg-gray-50/50">
              <div class="space-y-4">
                <div>
                  <p class="text-gray-700 mb-4">
                    PMMdb provides the Download page for users. You can download the complete datasets for Compounds
                    (detailed chemical information), Mushrooms (taxonomic information), and Toxicity Data (encompassing
                    LD50 and mechanisms of action) in CSV format directly from this page.
                  </p>

                  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                    <img :src="getImageUrl('helpimg6.1')" alt="Download Page" class="max-w-full h-auto rounded" />
                    <p class="text-center text-sm text-gray-500 mt-2">Fig 6-1. Download page</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Special Thanks Card -->
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <!-- Card Header -->
        <div class="bg-gradient-to-r from-amber-50 to-amber-100 p-6 border-b border-gray-200">
          <div class="flex items-center gap-4">
            <!-- Logo Placeholder -->
            <div class="flex-shrink-0 w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Special Thanks</h2>
              <p class="text-gray-600">Acknowledgements for tools and contributions</p>
            </div>
          </div>
        </div>

        <!-- Special Thanks Content -->
        <div class="p-6">
          <div class="bg-amber-50 rounded-lg p-5 border border-amber-200">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                <!-- <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg> -->
                <img src="/src/assets/ketcher.png" alt="Ketcher化学结构绘制工具" class="w-full h-full object-contain p-1" />
              </div>
              <div>
                <h3 class="font-bold text-gray-900 mb-2">Chemical Structure Drawing Tool</h3>
                <p class="text-gray-700">
                  This website uses Ketcher for chemical structure drawing. Special thanks to Ketcher for providing this
                  powerful drawing tool that enables users to easily create and search chemical structures.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeAccordion = ref(null)

const toggleAccordion = (index) => {
  activeAccordion.value = activeAccordion.value === index ? null : index
}

const baseURL = import.meta.env.BASE_URL
const getImageUrl = (imageName) => {
  return `${baseURL}/help-images/${imageName}.png`
}

// 可选：自动展开第一个Q&A
// onMounted(() => {
//   activeAccordion.value = 1
// })
</script>

<style scoped>
/* 平滑展开动画 */
div[v-show] {
  transition: all 0.3s ease-out;
}
</style>