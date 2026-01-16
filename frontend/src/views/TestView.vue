<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useExamStore } from '../stores/exam'
import { ref } from 'vue'

const router = useRouter()
const route = useRoute()
const exam = useExamStore()

const loading = ref(false)
const error = ref('')

const startTest = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await exam.startTest(route.params.testId)
    router.push(`/test/${result.attempt_id}/take`)
  } catch (err) {
    error.value = err.response?.data?.error || 'Не удалось начать тест'
    loading.value = false
  }
}

startTest()
</script>

<template>
  <div class="container">
    <div class="card" style="max-width: 500px; margin: 100px auto; text-align: center;">
      <div v-if="loading">
        <h2>Подготовка теста...</h2>
        <p>Пожалуйста, подождите</p>
      </div>
      <div v-else-if="error">
        <h2>Ошибка</h2>
        <p class="alert alert-error">{{ error }}</p>
        <router-link to="/" class="btn btn-primary">Вернуться к тестам</router-link>
      </div>
    </div>
  </div>
</template>
