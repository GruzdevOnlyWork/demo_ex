<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExamStore } from '../stores/exam'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const exam = useExamStore()
const auth = useAuthStore()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    await exam.fetchTests()
  } catch (err) {
    error.value = 'Не удалось загрузить тесты'
  } finally {
    loading.value = false
  }
})

const startTest = async (testId) => {
  try {
    const result = await exam.startTest(testId)
    router.push(`/test/${result.attempt_id}/take`)
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при запуске теста'
  }
}
</script>

<template>
  <div class="container">
    <div class="welcome-section">
      <h1>Добро пожаловать, {{ auth.user?.first_name || auth.user?.username }}!</h1>
      <p>Выберите тест для прохождения</p>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div v-if="loading" class="loading">Загрузка тестов...</div>

    <div v-else-if="exam.tests.length === 0" class="empty-state">
      <p>Пока нет доступных тестов</p>
    </div>

    <div v-else class="tests-grid">
      <div v-for="test in exam.tests" :key="test.id" class="test-card card">
        <h3>{{ test.title }}</h3>
        <p v-if="test.description" class="test-description">{{ test.description }}</p>

        <div class="test-meta">
          <span>{{ test.questions_count }} вопросов</span>
          <span v-if="test.time_limit"> | {{ test.time_limit }} мин</span>
          <span> | Проходной: {{ test.passing_score }}%</span>
        </div>

        <div v-if="test.categories?.length" class="test-categories">
          <span v-for="cat in test.categories" :key="cat.id" class="category-tag">
            {{ cat.name }}
          </span>
        </div>

        <button @click="startTest(test.id)" class="btn btn-primary">
          Начать тест
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-section {
  text-align: center;
  margin-bottom: 32px;
}

.welcome-section h1 {
  color: #4f46e5;
}

.welcome-section p {
  color: #6b7280;
  font-size: 18px;
}

.loading, .empty-state {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

.tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.test-card {
  display: flex;
  flex-direction: column;
}

.test-card h3 {
  color: #1f2937;
  margin-bottom: 8px;
}

.test-description {
  color: #6b7280;
  margin-bottom: 12px;
  flex-grow: 1;
}

.test-meta {
  color: #9ca3af;
  font-size: 14px;
  margin-bottom: 12px;
}

.test-categories {
  margin-bottom: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-tag {
  background: #eef2ff;
  color: #4f46e5;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
}

.test-card .btn {
  margin-top: auto;
}
</style>
