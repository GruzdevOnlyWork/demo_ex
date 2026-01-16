<script setup>
import { ref, onMounted } from 'vue'
import { useExamStore } from '../stores/exam'

const exam = useExamStore()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    await exam.fetchAttempts()
  } catch (err) {
    error.value = 'Не удалось загрузить историю'
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (status) => {
  const statuses = {
    'in_progress': 'В процессе',
    'completed': 'Завершен',
    'timeout': 'Время вышло'
  }
  return statuses[status] || status
}
</script>

<template>
  <div class="container">
    <h1>История тестирования</h1>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="exam.attempts.length === 0" class="empty-state card">
      <p>У вас пока нет пройденных тестов</p>
      <router-link to="/" class="btn btn-primary">Пройти тест</router-link>
    </div>

    <div v-else class="history-list">
      <div v-for="attempt in exam.attempts" :key="attempt.id" class="history-card card">
        <div class="history-header">
          <h3>{{ attempt.test?.title }}</h3>
          <span class="history-status" :class="attempt.status">
            {{ getStatusText(attempt.status) }}
          </span>
        </div>

        <div class="history-details">
          <div class="history-item">
            <span class="label">Дата:</span>
            <span>{{ formatDate(attempt.started_at) }}</span>
          </div>
          <div class="history-item">
            <span class="label">Результат:</span>
            <span :class="{ passed: attempt.is_passed, failed: !attempt.is_passed && attempt.status === 'completed' }">
              {{ attempt.score }} / {{ attempt.max_score }} ({{ attempt.percentage }}%)
            </span>
          </div>
          <div class="history-item" v-if="attempt.status === 'completed'">
            <span class="label">Статус:</span>
            <span :class="{ passed: attempt.is_passed, failed: !attempt.is_passed }">
              {{ attempt.is_passed ? 'Пройден' : 'Не пройден' }}
            </span>
          </div>
        </div>

        <div class="history-actions">
          <router-link
            v-if="attempt.status === 'in_progress'"
            :to="`/test/${attempt.id}/take`"
            class="btn btn-primary"
          >
            Продолжить
          </router-link>
          <router-link
            v-else
            :to="`/test/${attempt.id}/result`"
            class="btn btn-secondary"
          >
            Подробнее
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 24px;
}

.loading, .empty-state {
  text-align: center;
  padding: 48px;
}

.empty-state p {
  margin-bottom: 16px;
  color: #6b7280;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-card {
  display: grid;
  gap: 16px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.history-header h3 {
  margin: 0;
}

.history-status {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
}

.history-status.completed {
  background: #dcfce7;
  color: #166534;
}

.history-status.in_progress {
  background: #fef3c7;
  color: #92400e;
}

.history-status.timeout {
  background: #fef2f2;
  color: #991b1b;
}

.history-details {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.history-item {
  display: flex;
  gap: 8px;
}

.history-item .label {
  color: #6b7280;
}

.passed {
  color: #10b981;
  font-weight: 600;
}

.failed {
  color: #ef4444;
  font-weight: 600;
}

.history-actions {
  display: flex;
  gap: 12px;
}
</style>
