<template>
  <div class="auto bg-gray-50 py-12">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Title -->
      <h1 class="text-3xl font-bold text-center text-gray-900 mb-8 font-roboto">
        Submit New Compound Data
      </h1>

      <!-- Submission Form -->
      <form @submit.prevent="handleSubmit" class="bg-white rounded-xl shadow-lg p-8 border border-gray-200">

        <!-- Contributor Information -->
        <div class="mb-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Contributor Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Family Name <span class="text-red-500">*</span>
              </label>
              <input v-model="form.familyName" type="text" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Enter family name" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Your First Name <span class="text-red-500">*</span>
              </label>
              <input v-model="form.yourFirstName" type="text" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Enter your first name" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Your Email <span class="text-red-500">*</span>
              </label>
              <input v-model="form.yourEmail" type="email" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Enter your email address" />
            </div>
          </div>
        </div>

        <div class="border-t border-gray-200 my-8"></div>

        <!-- Compound Information -->
        <div class="mb-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Compound Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Compound Name <span class="text-red-500">*</span>
              </label>
              <input v-model="form.compoundName" type="text" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Enter compound name" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                CAS Number <span class="text-red-500">*</span>
              </label>
              <input v-model="form.casNumber" type="text" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="e.g., 2763-96-4" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Source Mushroom Species <span class="text-red-500">*</span>
              </label>
              <input v-model="form.sourceMushroom" type="text" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="e.g., Amanita pantherina" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Description <span class="text-red-500">*</span>
              </label>
              <textarea v-model="form.description" rows="4" required
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Describe the compound and its properties"></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Toxicity Data
              </label>
              <textarea v-model="form.toxicityData" rows="3"
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="Enter toxicity information (if available)"></textarea>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                References (DOI or URL)
              </label>
              <input v-model="form.reference" type="text"
                class="w-full rounded-lg border-gray-300 border p-3 focus:ring-2 focus:ring-primary focus:border-primary transition"
                placeholder="e.g., https://doi.org/10.xxxx/xxxx" />
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex justify-center gap-6 mt-8">
          <button type="submit" :disabled="submitting" :class="[
            'px-10 py-3 rounded-lg font-medium transition-all duration-300',
            submitting
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary text-white hover:bg-green-700 shadow-md hover:shadow-lg'
          ]">
            {{ submitting ? 'Submitting...' : 'Submit' }}
          </button>
          <button type="button" @click="resetForm"
            class="px-10 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition">
            Reset
          </button>
        </div>

        <!-- Submission Status -->
        <div v-if="submitStatus" class="mt-6 text-center">
          <p :class="[
            'p-3 rounded-lg',
            submitStatus.type === 'success'
              ? 'bg-green-50 text-green-700'
              : 'bg-red-50 text-red-700'
          ]">
            {{ submitStatus.message }}
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import * as api from '../api'

const initialForm = {
  familyName: '',
  yourFirstName: '',
  yourEmail: '',
  compoundName: '',
  casNumber: '',
  description: '',
  toxicityData: '',
  sourceMushroom: '',
  reference: ''
}

const form = reactive({ ...initialForm })
const submitting = ref(false)
const submitStatus = ref(null)

const handleSubmit = async () => {
  // 验证必填字段
  if (!form.familyName || !form.yourFirstName || !form.yourEmail ||
    !form.compoundName || !form.casNumber || !form.description || !form.sourceMushroom) {
    submitStatus.value = {
      type: 'error',
      message: 'Please fill in all required fields (*)'
    }
    return
  }

  submitting.value = true
  submitStatus.value = null

  try {
    await api.submitData(form)

    submitStatus.value = {
      type: 'success',
      message: 'Thank you for your submission! The data will be reviewed and added to the database.'
    }

    resetForm()
  } catch (error) {
    console.error('Submission failed:', error)
    submitStatus.value = {
      type: 'error',
      message: 'Submission failed. Please try again or contact support.'
    }
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  Object.assign(form, initialForm)
  submitStatus.value = null
}
</script>