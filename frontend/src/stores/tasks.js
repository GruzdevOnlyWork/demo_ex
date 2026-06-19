import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tasksApi } from '../api'

export const useTasksStore = defineStore('tasks', () => {
  const variants = ref([])
  const currentVariant = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchVariants() {
    loading.value = true
    error.value = null
    try {
      const response = await tasksApi.getVariants()
      variants.value = response.data
    } catch (err) {
      error.value = 'Не удалось загрузить варианты экзаменов'
      console.error('Error fetching variants:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchVariant(variantId) {
    loading.value = true
    error.value = null
    try {
      const response = await tasksApi.getVariant(variantId)
      currentVariant.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Не удалось загрузить вариант экзамена'
      console.error('Error fetching variant:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  function clearCurrentVariant() {
    currentVariant.value = null
  }

  return {
      variants,
    currentVariant,
    loading,
    error,
      fetchVariants,
    fetchVariant,
    clearCurrentVariant
  }
})
