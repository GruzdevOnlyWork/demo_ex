import { defineStore } from 'pinia'
import { ref } from 'vue'
import { modulesApi } from '../api'

export const useModulesStore = defineStore('modules', () => {
  const sections = ref([])
  const currentModule = ref(null)
  const myProgress = ref([])
  const loading = ref(false)

  async function fetchSectionsWithModules() {
    loading.value = true
    try {
      const response = await modulesApi.getSectionsWithModules()
      sections.value = response.data
    } finally {
      loading.value = false
    }
  }

  async function fetchModule(moduleId) {
    loading.value = true
    try {
      const response = await modulesApi.getModule(moduleId)
      currentModule.value = response.data
      return response.data
    } finally {
      loading.value = false
    }
  }

  async function startModule(moduleId) {
    const response = await modulesApi.startModule(moduleId)
    if (currentModule.value && currentModule.value.id === moduleId) {
      currentModule.value.user_progress = response.data
    }
    return response.data
  }

  async function updateProgress(moduleId, data) {
    const response = await modulesApi.updateProgress(moduleId, data)
    if (currentModule.value && currentModule.value.id === moduleId) {
      currentModule.value.user_progress = response.data
    }
    return response.data
  }

  async function completeModule(moduleId) {
    const response = await modulesApi.completeModule(moduleId)
    if (currentModule.value && currentModule.value.id === moduleId) {
      currentModule.value.user_progress = response.data
    }
    return response.data
  }

  async function fetchMyProgress() {
    const response = await modulesApi.getMyProgress()
    myProgress.value = response.data
    return response.data
  }

  return {
    sections,
    currentModule,
    myProgress,
    loading,
    fetchSectionsWithModules,
    fetchModule,
    startModule,
    updateProgress,
    completeModule,
    fetchMyProgress
  }
})
