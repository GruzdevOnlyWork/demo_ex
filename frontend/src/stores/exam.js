import { defineStore } from 'pinia'
import { ref } from 'vue'
import { examsApi } from '../api'

export const useExamStore = defineStore('exam', () => {
  const tests = ref([])
  const currentAttempt = ref(null)
  const questions = ref([])
  const currentQuestionIndex = ref(0)
  const timeRemaining = ref(null)
  const attempts = ref([])

  async function fetchTests() {
    const response = await examsApi.getTests()
    tests.value = response.data
  }

  async function startTest(testId) {
    const response = await examsApi.startTest(testId)
    currentAttempt.value = response.data
    return response.data
  }

  async function loadQuestions(attemptId) {
    const response = await examsApi.getAttemptQuestions(attemptId)
    questions.value = response.data.questions
    timeRemaining.value = response.data.time_remaining
    currentQuestionIndex.value = 0
    return response.data
  }

  async function submitAnswer(attemptId, questionId, answerIds, textAnswer = '') {
    await examsApi.submitAnswer(attemptId, {
      question_id: questionId,
      answer_ids: answerIds,
      text_answer: textAnswer
    })

    const question = questions.value.find(q => q.id === questionId)
    if (question) {
      question.user_answer = {
        selected_answer_ids: answerIds,
        text_answer: textAnswer
      }
    }
  }

  async function finishTest(attemptId) {
    const response = await examsApi.finishTest(attemptId)
    currentAttempt.value = null
    questions.value = []
    return response.data
  }

  async function fetchAttempts() {
    const response = await examsApi.getMyAttempts()
    attempts.value = response.data
  }

  async function getAttemptResult(attemptId) {
    const response = await examsApi.getAttemptResult(attemptId)
    return response.data
  }

  function nextQuestion() {
    if (currentQuestionIndex.value < questions.value.length - 1) {
      currentQuestionIndex.value++
    }
  }

  function prevQuestion() {
    if (currentQuestionIndex.value > 0) {
      currentQuestionIndex.value--
    }
  }

  function goToQuestion(index) {
    if (index >= 0 && index < questions.value.length) {
      currentQuestionIndex.value = index
    }
  }

  return {
    tests,
    currentAttempt,
    questions,
    currentQuestionIndex,
    timeRemaining,
    attempts,
    fetchTests,
    startTest,
    loadQuestions,
    submitAnswer,
    finishTest,
    fetchAttempts,
    getAttemptResult,
    nextQuestion,
    prevQuestion,
    goToQuestion
  }
})
