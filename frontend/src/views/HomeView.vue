<template>
  <div class="min-h-screen flex flex-col">
    <!-- Hero Section -->
    <div class="flex-grow flex items-center py-2">
      <!-- Background Image -->
      <div class="absolute inset-0 z-0">
        <img src="/src/assets/hero-bg.jpg" alt="Mushroom background" class="w-full h-full object-cover opacity-10" />
      </div>

      <!-- Main Content Container -->
      <div class="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl p-6 md:p-8 lg:p-10">
          <!-- Title -->
          <h1 class="text-2xl md:text-4xl font-bold text-gray-900 mb-6 md:mb-8 text-center">
            Welcome to the Poisonous Mushroom Metabolite Database!
          </h1>

          <!-- Content with Image - 使用相同的网格布局 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-10 items-center">
            <!-- Left: Image -->
            <div class="w-full">
              <div class="relative overflow-hidden rounded-xl shadow-lg">
                <img src="/src/assets/hero.png" alt="Mushroom metabolites visualization"
                  class="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500" />
              </div>
            </div>

            <!-- Right: Text Content -->
            <div class="w-full">
              <div class="text-gray-700 text-base md:text-xl leading-relaxed space-y-4 md:space-y-6 text-justify">
                <p>
                  The secondary metabolites of poisonous mushrooms are the primary causative agents of poisoning
                  incidents. Their unique chemical structures also render them a valuable source for discovering novel
                  bioactive molecules.
                </p>
                <p>
                  To systematically consolidate scientific data directly relevant to the hazards of poisonous mushrooms,
                  we have developed the <b>"Characteristic Secondary Metabolites Database of Poisonous Mushrooms"</b>.
                </p>
                <p>
                  Currently, the database contains 678 secondary metabolites derived from 235 poisonous mushroom
                  species, along with 915 toxicological data records. It provides key information including chemical
                  structures, physicochemical properties, ADME parameters, toxicological data, and source organisms.
                  This database aims to offer professional and comprehensive data support for research on poisoning
                  mechanisms, toxin prevention and control, as well as risk assessment related to poisonous mushrooms.
                </p>
              </div>

              <!-- Button - 居中 -->
              <div class="mt-8 md:mt-10 text-center">
                <router-link to="/browse"
                  class="inline-flex items-center justify-center px-8 py-3 md:px-10 md:py-4 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-base md:text-lg"
                  :style="{ backgroundColor: '#16A34A' }">
                  Explore Database
                  <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer - 使用相同的最大宽度和对齐方式 -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-0">
<<<<<<< HEAD
          
=======

>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
          <!-- Sister Projects -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-1">
              Sister Projects
            </h3>
            <div class="border-b border-gray-300 mb-0"></div>
            <div class="grid grid-cols-1 md:grid-cols-2">
<<<<<<< HEAD
              <a v-for="project in sisterProjects" 
                :key="project.name"
                :href="project.url"
                target="_blank"
                rel="noopener noreferrer"
                class="group hover:bg-gray-50 p-2 rounded-lg transition-colors duration-200"
              >
=======
              <a v-for="project in sisterProjects" :key="project.name" :href="project.url" target="_blank"
                rel="noopener noreferrer" class="group hover:bg-gray-50 p-2 rounded-lg transition-colors duration-200">
>>>>>>> dc1dfda12b8a4d7f588a005e8d539f45cb23ed02
                <div class="text-xs text-gray-700 hover:text-gray-900 transition-colors duration-200">
                  <span class="font-medium group-hover:text-green-600 transition-colors duration-200">
                    {{ project.name }}
                  </span>
                </div>
              </a>
            </div>
          </div>

          <!-- About Us -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-1">
              About Us
            </h3>
            <div class="border-b border-gray-300 mb-1"></div>
            <div class="space-y-4">
              <!-- Yang Zhang -->
              <div>
                <p class="text-sm font-medium text-gray-900 mb-1">Yang Zhang</p>
                <p class="text-xs text-gray-700">
                  Contact
                  <a href="mailto:zhy1001@alu.uestc.edu.cn"
                    class="text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200">
                    zhy1001@alu.uestc.edu.cn
                  </a>
                  <span class="text-gray-400 mx-1">,</span>
                  <a href="mailto:yangzhang@cdutcm.edu.cn"
                    class="text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200">
                    yangzhang@cdutcm.edu.cn
                  </a>
                </p>
              </div>

              <!-- Guangbo Xie -->
              <div>
                <p class="text-sm font-medium text-gray-900 mb-1">Guangbo Xie</p>
                <p class="text-xs text-gray-700">
                  Contact
                  <a href="mailto:gbxie@uestc.edu.cn"
                    class="text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200">
                    gbxie@uestc.edu.cn
                  </a>
                </p>
              </div>
            </div>

            <!-- Copyright -->
            <div class="pt-4 mt-4 border-t border-gray-200">
              <p class="text-xs text-gray-500">
                © Department of Bioinformatics
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const sisterProjects = ref([
  { name: 'CellCall (NAR. 2021)', url: 'https://pubmed.ncbi.nlm.nih.gov/34331449/' },
  { name: 'cncRNAdb (NAR. 2021)', url: 'https://pubmed.ncbi.nlm.nih.gov/33010163/' },
  { name: 'Cellinker (Bioinformatics. 2021)', url: 'https://pubmed.ncbi.nlm.nih.gov/33471060/' },
  { name: 'TCM2COVID (iMETA. 2022)', url: 'https://pubmed.ncbi.nlm.nih.gov/36245702/' },
  { name: 'MetaboliteCOVID (Comput Biol Med. 2023)', url: 'https://pubmed.ncbi.nlm.nih.gov/37925911/' },
  { name: 'MCSdb (Scientific Data. 2024)', url: 'https://pubmed.ncbi.nlm.nih.gov/38459036/' },
  { name: 'P450Rdb (J Adv Res. 2024)', url: 'https://pubmed.ncbi.nlm.nih.gov/37871773/' }
])
</script>

<style scoped>
/* 确保最小高度足够，使footer能够粘在底部 */
.min-h-screen {
  min-height: 100vh;
}

/* 移除之前的自定义样式，使用Tailwind CSS类 */
</style>