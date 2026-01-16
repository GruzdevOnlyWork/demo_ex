<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useExamStore } from '../stores/exam'

const route = useRoute()
const exam = useExamStore()

const result = ref(null)
const loading = ref(true)
const error = ref('')
const showDetails = ref(false)

onMounted(async () => {
  try {
    result.value = await exam.getAttemptResult(route.params.attemptId)
  } catch (err) {
    error.value = err.response?.data?.error || 'Не удалось загрузить результаты'
  } finally {
    loading.value = false
  }
})

const isPassed = computed(() => result.value?.is_passed)
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading-state">
      <p>Загрузка результатов...</p>
    </div>

    <div v-else-if="error" class="card">
      <div class="alert alert-error">{{ error }}</div>
      <router-link to="/" class="btn btn-primary">Вернуться к тестам</router-link>
    </div>

    <div v-else-if="result" class="result-container">
      <div class="card result-card">
        <h1>Результаты теста</h1>
        <h2>{{ result.test?.title }}</h2>

        <div class="result-score" :class="{ passed: isPassed, failed: !isPassed }">
          {{ result.percentage }}%
        </div>

        <p class="result-status" :class="{ passed: isPassed, failed: !isPassed }">
          {{ isPassed ? 'Тест пройден!' : 'Тест не пройден' }}
        </p>

        <div class="result-details">
          <div class="result-item">
            <div class="result-item-value">{{ result.score }}</div>
            <div class="result-item-label">Набрано баллов</div>
          </div>
          <div class="result-item">
            <div class="result-item-value">{{ result.max_score }}</div>
            <div class="result-item-label">Максимум</div>
          </div>
          <div class="result-item">
            <div class="result-item-value">{{ result.test?.passing_score }}%</div>
            <div class="result-item-label">Проходной балл</div>
          </div>
        </div>

        <div class="result-actions">
          <router-link to="/" class="btn btn-primary">К списку тестов</router-link>
          <button @click="showDetails = !showDetails" class="btn btn-secondary">
            {{ showDetails ? 'Скрыть ответы' : 'Показать ответы' }}
          </button>
        </div>
      </div>

      <!-- Детализация ответов -->
      <div v-if="showDetails" class="answers-review">
        <h3>Детализация ответов</h3>

        <div
          v-for="(ua, index) in result.user_answers"
          :key="ua.id"
          class="review-card card"
          :class="{ correct: ua.is_correct, incorrect: !ua.is_correct }"
        >
          <div class="review-header">
            <span class="review-number">Вопрос {{ index + 1 }}</span>
            <span class="review-status">
              {{ ua.is_correct ? '+' + ua.points_earned : '0' }} балл.
            </span>
          </div>

          <div class="review-question">{{ ua.question.text }}</div>

          <div v-if="ua.question.question_type !== 'text'" class="review-answers">
            <div
              v-for="answer in ua.question.answers"
              :key="answer.id"
              class="review-answer"
              :class="{
                'is-correct': answer.is_correct,
                'user-selected': ua.selected_answers.some(a => a.id === answer.id),
                'wrong-selected': ua.selected_answers.some(a => a.id === answer.id) && !answer.is_correct
              }"
            >
              <span class="answer-marker">
                <template v-if="answer.is_correct">&#10003;</template>
                <template v-else-if="ua.selected_answers.some(a => a.id === answer.id)">&#10007;</template>
              </span>
              {{ answer.text }}
            </div>
          </div>

          <div v-else class="review-text-answer">
            <p><strong>Ваш ответ:</strong> {{ ua.text_answer || '(не отвечено)' }}</p>
            <p><strong>Правильный ответ:</strong> {{ ua.question.answers[0]?.text }}</p>
          </div>

          <div v-if="ua.question.explanation" class="review-explanation">
            <strong>Пояснение:</strong> {{ ua.question.explanation }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading-state {
  text-align: center;
  padding: 48px;
}

.result-container {
  max-width: 800px;
  margin: 0 auto;
}

.result-card {
  text-align: center;
}

.result-card h1 {
  color: #4f46e5;
  margin-bottom: 8px;
}

.result-card h2 {
  color: #6b7280;
  font-weight: normal;
  margin-bottom: 24px;
}

.result-score {
  font-size: 72px;
  font-weight: 700;
  margin: 24px 0;
}

.result-score.passed {
  color: #10b981;
}

.result-score.failed {
  color: #ef4444;
}

.result-status {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
}

.result-status.passed {
  color: #10b981;
}

.result-status.failed {
  color: #ef4444;
}

.result-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 32px 0;
}

.result-item {
  padding: 20px;
  background: #f9fafb;
  border-radius: 12px;
}

.result-item-value {
  font-size: 28px;
  font-weight: 700;
  color: #4f46e5;
}

.result-item-label {
  color: #6b7280;
  margin-top: 4px;
}

.result-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.answers-review {
  margin-top: 32px;
}

.answers-review h3 {
  margin-bottom: 20px;
}

.review-card {
  margin-bottom: 16px;
  border-left: 4px solid;
}

.review-card.correct {
  border-color: #10b981;
}

.review-card.incorrect {
  border-color: #ef4444;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.review-number {
  font-weight: 600;
  color: #4f46e5;
}

.review-status {
  font-weight: 600;
}

.review-card.correct .review-status {
  color: #10b981;
}

.review-card.incorrect .review-status {
  color: #ef4444;
}

.review-question {
  font-size: 16px;
  margin-bottom: 16px;
  line-height: 1.5;
}

.review-answer {
  padding: 10px 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  background: #f9fafb;
  display: flex;
  align-items: center;
  gap: 8px;
}

.review-answer.is-correct {
  background: #ecfdf5;
  color: #065f46;
}

.review-answer.wrong-selected {
  background: #fef2f2;
  color: #991b1b;
}

.answer-marker {
  font-weight: bold;
  width: 20px;
}

.review-text-answer {
  background: #f9fafb;
  padding: 12px;
  border-radius: 8px;
}

.review-text-answer p {
  margin-bottom: 8px;
}

.review-explanation {
  margin-top: 12px;
  padding: 12px;
  background: #fef3c7;
  border-radius: 8px;
  color: #92400e;
}
</style>
