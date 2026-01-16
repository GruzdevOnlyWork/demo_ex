<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useExamStore } from '../stores/exam'

const router = useRouter()
const route = useRoute()
const exam = useExamStore()

const loading = ref(true)
const error = ref('')
const submitting = ref(false)
const testTitle = ref('')
const timer = ref(null)
const timeLeft = ref(0)

const attemptId = computed(() => route.params.attemptId)

const currentQuestion = computed(() => exam.questions[exam.currentQuestionIndex])
const progress = computed(() => {
  if (exam.questions.length === 0) return 0
  return Math.round(((exam.currentQuestionIndex + 1) / exam.questions.length) * 100)
})

const answeredCount = computed(() => {
  return exam.questions.filter(q => {
    const ua = q.user_answer
    return (ua?.selected_answer_ids?.length > 0) || ua?.text_answer
  }).length
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = Math.floor(timeLeft.value % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

const timerClass = computed(() => {
  if (timeLeft.value <= 60) return 'danger'
  if (timeLeft.value <= 300) return 'warning'
  return ''
})

const selectedAnswers = ref([])
const textAnswer = ref('')

onMounted(async () => {
  try {
    const data = await exam.loadQuestions(attemptId.value)
    testTitle.value = data.test_title

    if (data.time_remaining) {
      timeLeft.value = data.time_remaining
      startTimer()
    }

    updateLocalState()
  } catch (err) {
    error.value = err.response?.data?.error || 'Не удалось загрузить вопросы'
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})

function startTimer() {
  timer.value = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      clearInterval(timer.value)
      finishTest()
    }
  }, 1000)
}

function updateLocalState() {
  if (!currentQuestion.value) return
  const ua = currentQuestion.value.user_answer
  selectedAnswers.value = ua?.selected_answer_ids || []
  textAnswer.value = ua?.text_answer || ''
}

function selectAnswer(answerId) {
  if (currentQuestion.value.question_type === 'single') {
    selectedAnswers.value = [answerId]
  } else {
    const index = selectedAnswers.value.indexOf(answerId)
    if (index === -1) {
      selectedAnswers.value.push(answerId)
    } else {
      selectedAnswers.value.splice(index, 1)
    }
  }
  saveAnswer()
}

async function saveAnswer() {
  if (!currentQuestion.value) return
  try {
    await exam.submitAnswer(
      attemptId.value,
      currentQuestion.value.id,
      selectedAnswers.value,
      textAnswer.value
    )
  } catch (err) {
    console.error('Failed to save answer:', err)
  }
}

function goToQuestion(index) {
  exam.goToQuestion(index)
  updateLocalState()
}

function nextQuestion() {
  exam.nextQuestion()
  updateLocalState()
}

function prevQuestion() {
  exam.prevQuestion()
  updateLocalState()
}

async function finishTest() {
  if (submitting.value) return

  const unanswered = exam.questions.length - answeredCount.value
  if (unanswered > 0) {
    if (!confirm(`У вас ${unanswered} неотвеченных вопросов. Завершить тест?`)) {
      return
    }
  }

  submitting.value = true
  try {
    await exam.finishTest(attemptId.value)
    router.push(`/test/${attemptId.value}/result`)
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при завершении теста'
    submitting.value = false
  }
}
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading-state">
      <p>Загрузка вопросов...</p>
    </div>

    <div v-else-if="error" class="card">
      <div class="alert alert-error">{{ error }}</div>
      <router-link to="/" class="btn btn-primary">Вернуться к тестам</router-link>
    </div>

    <div v-else class="test-container">
      <!-- Header -->
      <div class="test-header card">
        <h2>{{ testTitle }}</h2>
        <div class="test-info">
          <span>Вопрос {{ exam.currentQuestionIndex + 1 }} из {{ exam.questions.length }}</span>
          <span>Отвечено: {{ answeredCount }} / {{ exam.questions.length }}</span>
        </div>
        <div class="progress-bar">
          <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>

      <div class="test-layout">
        <!-- Main content -->
        <div class="test-main">
          <!-- Timer -->
          <div v-if="timeLeft > 0" class="timer" :class="timerClass">
            {{ formattedTime }}
          </div>

          <!-- Question -->
          <div v-if="currentQuestion" class="question-card">
            <div class="question-number">
              Вопрос {{ exam.currentQuestionIndex + 1 }}
              <span class="question-points">({{ currentQuestion.points }} балл.)</span>
            </div>
            <div class="question-text">{{ currentQuestion.text }}</div>

            <!-- Варианты ответов -->
            <div v-if="currentQuestion.question_type !== 'text'" class="answers-list">
              <div
                v-for="answer in currentQuestion.answers"
                :key="answer.id"
                class="answer-option"
                :class="{ selected: selectedAnswers.includes(answer.id) }"
                @click="selectAnswer(answer.id)"
              >
                <input
                  :type="currentQuestion.question_type === 'single' ? 'radio' : 'checkbox'"
                  :checked="selectedAnswers.includes(answer.id)"
                  :name="'question-' + currentQuestion.id"
                />
                <span>{{ answer.text }}</span>
              </div>
            </div>

            <!-- Текстовый ответ -->
            <div v-else class="text-answer">
              <textarea
                v-model="textAnswer"
                @blur="saveAnswer"
                class="form-control"
                rows="4"
                placeholder="Введите ваш ответ..."
              ></textarea>
            </div>
          </div>

          <!-- Navigation -->
          <div class="question-nav">
            <button
              @click="prevQuestion"
              class="btn btn-secondary"
              :disabled="exam.currentQuestionIndex === 0"
            >
              Назад
            </button>

            <button
              v-if="exam.currentQuestionIndex < exam.questions.length - 1"
              @click="nextQuestion"
              class="btn btn-primary"
            >
              Далее
            </button>

            <button
              v-else
              @click="finishTest"
              class="btn btn-success"
              :disabled="submitting"
            >
              {{ submitting ? 'Завершение...' : 'Завершить тест' }}
            </button>
          </div>
        </div>

        <!-- Question navigator -->
        <div class="test-sidebar card">
          <h4>Навигация</h4>
          <div class="question-dots">
            <button
              v-for="(q, index) in exam.questions"
              :key="q.id"
              class="question-dot"
              :class="{
                active: index === exam.currentQuestionIndex,
                answered: q.user_answer?.selected_answer_ids?.length > 0 || q.user_answer?.text_answer
              }"
              @click="goToQuestion(index)"
            >
              {{ index + 1 }}
            </button>
          </div>

          <button
            @click="finishTest"
            class="btn btn-success btn-block"
            :disabled="submitting"
            style="margin-top: 20px;"
          >
            Завершить тест
          </button>
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

.test-header {
  margin-bottom: 20px;
}

.test-header h2 {
  margin-bottom: 8px;
}

.test-info {
  display: flex;
  justify-content: space-between;
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 12px;
}

.test-layout {
  display: grid;
  grid-template-columns: 1fr 250px;
  gap: 24px;
}

@media (max-width: 900px) {
  .test-layout {
    grid-template-columns: 1fr;
  }

  .test-sidebar {
    order: -1;
  }
}

.question-points {
  color: #6b7280;
  font-size: 14px;
}

.question-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.question-number {
  color: #4f46e5;
  font-weight: 600;
  margin-bottom: 12px;
}

.question-text {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.answers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-option {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.answer-option:hover {
  border-color: #4f46e5;
  background: #f5f3ff;
}

.answer-option.selected {
  border-color: #4f46e5;
  background: #eef2ff;
}

.answer-option input {
  margin-right: 12px;
  width: 18px;
  height: 18px;
}

.text-answer textarea {
  resize: vertical;
  min-height: 100px;
}

.question-nav {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
  gap: 12px;
}

.test-sidebar h4 {
  margin-bottom: 16px;
}

.question-dots {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.question-dot {
  width: 40px;
  height: 40px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.question-dot:hover {
  border-color: #4f46e5;
}

.question-dot.active {
  border-color: #4f46e5;
  background: #4f46e5;
  color: white;
}

.question-dot.answered {
  background: #dcfce7;
  border-color: #10b981;
}

.question-dot.answered.active {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.btn-block {
  width: 100%;
}
</style>
