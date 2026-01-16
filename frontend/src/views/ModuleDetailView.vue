<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '../stores/modules'

const route = useRoute()
const router = useRouter()
const modules = useModulesStore()

const loading = ref(true)
const error = ref('')
const activeTab = ref('steps')
const expandedSteps = ref([])

const module = computed(() => modules.currentModule)
const progress = computed(() => module.value?.user_progress)

onMounted(async () => {
  try {
    await modules.fetchModule(route.params.id)
    if (progress.value?.current_step) {
      expandedSteps.value = [progress.value.current_step]
    } else if (module.value?.steps?.length) {
      expandedSteps.value = [1]
    }
  } catch (err) {
    error.value = 'Не удалось загрузить модуль'
  } finally {
    loading.value = false
  }
})

const toggleStep = (stepNumber) => {
  const index = expandedSteps.value.indexOf(stepNumber)
  if (index === -1) {
    expandedSteps.value.push(stepNumber)
  } else {
    expandedSteps.value.splice(index, 1)
  }
}

const isStepExpanded = (stepNumber) => {
  return expandedSteps.value.includes(stepNumber)
}

const startModule = async () => {
  try {
    await modules.startModule(module.value.id)
  } catch (err) {
    error.value = 'Ошибка при начале модуля'
  }
}

const updateCurrentStep = async (stepNumber) => {
  try {
    await modules.updateProgress(module.value.id, { current_step: stepNumber })
  } catch (err) {
    console.error('Failed to update step:', err)
  }
}

const completeModule = async () => {
  try {
    await modules.completeModule(module.value.id)
  } catch (err) {
    error.value = 'Ошибка при завершении модуля'
  }
}

const getNoteIcon = (noteType) => {
  const icons = {
    'info': 'ℹ️',
    'warning': '⚠️',
    'tip': '💡',
    'important': '❗',
    'example': '📝'
  }
  return icons[noteType] || 'ℹ️'
}

const getNoteClass = (noteType) => {
  return `note-${noteType}`
}

const getFileIcon = (fileType) => {
  const icons = {
    'document': '📄',
    'image': '🖼️',
    'archive': '📦',
    'video': '🎬',
    'other': '📎'
  }
  return icons[fileType] || '📎'
}
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading">Загрузка модуля...</div>

    <div v-else-if="error" class="card">
      <div class="alert alert-error">{{ error }}</div>
      <router-link to="/modules" class="btn btn-primary">Вернуться к модулям</router-link>
    </div>

    <div v-else-if="module" class="module-page">
      <!-- Header -->
      <div class="module-header card">
        <div class="header-top">
          <router-link to="/modules" class="back-link">&larr; К модулям</router-link>
          <span v-if="progress" class="status-badge" :class="progress.status">
            {{ progress.status_display }}
          </span>
        </div>

        <h1>{{ module.name }}</h1>
        <p class="module-section">{{ module.section_name }}</p>

        <div v-if="module.description" class="module-description">
          {{ module.description }}
        </div>

        <div class="module-meta">
          <div v-if="module.duration" class="meta-item">
            <span class="meta-label">Время:</span>
            <span>{{ module.duration }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Шагов:</span>
            <span>{{ module.steps?.length || 0 }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Макс. балл:</span>
            <span>{{ module.max_score }}</span>
          </div>
        </div>

        <!-- Progress & Actions -->
        <div class="module-actions">
          <template v-if="!progress || progress.status === 'not_started'">
            <button @click="startModule" class="btn btn-primary">
              Начать изучение
            </button>
          </template>
          <template v-else-if="progress.status === 'in_progress'">
            <div class="progress-info">
              <span>Текущий шаг: {{ progress.current_step }} из {{ module.steps?.length }}</span>
              <div class="progress-bar">
                <div
                  class="progress-bar-fill"
                  :style="{ width: (progress.current_step / (module.steps?.length || 1) * 100) + '%' }"
                ></div>
              </div>
            </div>
            <button
              v-if="progress.current_step >= (module.steps?.length || 0)"
              @click="completeModule"
              class="btn btn-success"
            >
              Завершить модуль
            </button>
          </template>
          <template v-else>
            <div class="completed-badge">
              ✓ Модуль завершен
            </div>
          </template>
        </div>
      </div>

      <!-- Instruction -->
      <div v-if="module.instruction" class="instruction-block card">
        <h3>Общая инструкция</h3>
        <div class="instruction-content">{{ module.instruction }}</div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'steps' }"
          @click="activeTab = 'steps'"
        >
          Шаги ({{ module.steps?.length || 0 }})
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'criteria' }"
          @click="activeTab = 'criteria'"
        >
          Критерии ({{ module.criteria?.length || 0 }})
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'files' }"
          @click="activeTab = 'files'"
        >
          Файлы ({{ module.files?.length || 0 }})
        </button>
      </div>

      <!-- Steps Tab -->
      <div v-if="activeTab === 'steps'" class="tab-content">
        <div v-if="!module.steps?.length" class="empty-tab">
          Шаги не добавлены
        </div>
        <div v-else class="steps-list">
          <div
            v-for="step in module.steps"
            :key="step.id"
            class="step-card card"
            :class="{
              expanded: isStepExpanded(step.number),
              current: progress?.current_step === step.number,
              completed: progress?.current_step > step.number
            }"
          >
            <div class="step-header" @click="toggleStep(step.number)">
              <div class="step-number">
                <span v-if="progress?.current_step > step.number" class="check">✓</span>
                <span v-else>{{ step.number }}</span>
              </div>
              <div class="step-title">{{ step.title }}</div>
              <div class="step-toggle">
                {{ isStepExpanded(step.number) ? '▼' : '▶' }}
              </div>
            </div>

            <div v-if="isStepExpanded(step.number)" class="step-content">
              <div class="step-description">{{ step.description }}</div>

              <!-- Images -->
              <div v-if="step.images?.length" class="step-images">
                <div
                  v-for="image in step.images"
                  :key="image.id"
                  class="step-image"
                >
                  <img :src="image.image_url" :alt="image.caption || 'Изображение шага'" />
                  <p v-if="image.caption" class="image-caption">{{ image.caption }}</p>
                </div>
              </div>

              <div v-if="step.expected_result" class="expected-result">
                <strong>Ожидаемый результат:</strong>
                <p>{{ step.expected_result }}</p>
              </div>

              <!-- Notes -->
              <div v-if="step.notes?.length" class="step-notes">
                <div
                  v-for="note in step.notes"
                  :key="note.id"
                  class="note"
                  :class="getNoteClass(note.note_type)"
                >
                  <div class="note-header">
                    <span class="note-icon">{{ getNoteIcon(note.note_type) }}</span>
                    <span v-if="note.title" class="note-title">{{ note.title }}</span>
                    <span v-else class="note-type">{{ note.note_type_display }}</span>
                  </div>
                  <div class="note-content">{{ note.content }}</div>
                </div>
              </div>

              <!-- Step Actions -->
              <div v-if="progress?.status === 'in_progress'" class="step-actions">
                <button
                  v-if="progress.current_step < step.number"
                  @click="updateCurrentStep(step.number)"
                  class="btn btn-secondary btn-sm"
                >
                  Перейти к этому шагу
                </button>
                <button
                  v-else-if="progress.current_step === step.number && step.number < (module.steps?.length || 0)"
                  @click="updateCurrentStep(step.number + 1)"
                  class="btn btn-primary btn-sm"
                >
                  Следующий шаг →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Criteria Tab -->
      <div v-if="activeTab === 'criteria'" class="tab-content">
        <div v-if="!module.criteria?.length" class="empty-tab">
          Критерии не добавлены
        </div>
        <div v-else class="criteria-list">
          <div class="criteria-header card">
            <span>Общий балл:</span>
            <strong>{{ module.total_criteria_score }} баллов</strong>
          </div>
          <div
            v-for="criteria in module.criteria"
            :key="criteria.id"
            class="criteria-card card"
          >
            <div class="criteria-main">
              <div class="criteria-name">{{ criteria.name }}</div>
              <div class="criteria-score">{{ criteria.max_score }} балл.</div>
            </div>
            <p v-if="criteria.description" class="criteria-description">
              {{ criteria.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- Files Tab -->
      <div v-if="activeTab === 'files'" class="tab-content">
        <div v-if="!module.files?.length" class="empty-tab">
          Файлы не прикреплены
        </div>
        <div v-else class="files-list">
          <a
            v-for="file in module.files"
            :key="file.id"
            :href="file.file_url"
            target="_blank"
            class="file-card card"
          >
            <div class="file-icon">{{ getFileIcon(file.file_type) }}</div>
            <div class="file-info">
              <div class="file-name">{{ file.name }}</div>
              <p v-if="file.description" class="file-description">{{ file.description }}</p>
              <div class="file-meta">
                <span>{{ file.file_type_display }}</span>
                <span>{{ file.file_size }}</span>
              </div>
            </div>
            <div class="file-download">
              ⬇️
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

.module-page {
  max-width: 900px;
  margin: 0 auto;
}

.module-header {
  margin-bottom: 24px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.back-link {
  color: #6b7280;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: #4f46e5;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge.not_started {
  background: #f3f4f6;
  color: #6b7280;
}

.status-badge.in_progress {
  background: #fef3c7;
  color: #d97706;
}

.status-badge.completed {
  background: #dcfce7;
  color: #16a34a;
}

.module-header h1 {
  color: #1f2937;
  margin-bottom: 4px;
}

.module-section {
  color: var(--primary);
  font-weight: 500;
  margin-bottom: 16px;
}

.module-description {
  color: #6b7280;
  margin-bottom: 20px;
  line-height: 1.6;
}

.module-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 16px 0;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  gap: 8px;
}

.meta-label {
  color: #6b7280;
}

.module-actions {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.progress-info {
  flex-grow: 1;
}

.progress-info span {
  display: block;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.completed-badge {
  color: #16a34a;
  font-weight: 600;
  font-size: 18px;
}

/* Instruction */
.instruction-block {
  margin-bottom: 24px;
  background: #fefce8;
  border: 1px solid #fef08a;
}

.instruction-block h3 {
  color: #854d0e;
  margin-bottom: 12px;
}

.instruction-content {
  color: #713f12;
  line-height: 1.7;
  white-space: pre-line;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0;
}

.tab {
  padding: 12px 20px;
  border: none;
  background: none;
  font-size: 15px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab:hover {
  color: var(--primary);
}

.tab.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

.tab-content {
  min-height: 200px;
}

.empty-tab {
  text-align: center;
  padding: 48px;
  color: #9ca3af;
}

/* Steps */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-card {
  overflow: hidden;
  transition: all 0.2s;
}

.step-card.current {
  border-left: 4px solid var(--primary);
}

.step-card.completed {
  border-left: 4px solid #10b981;
  opacity: 0.85;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  padding: 4px 0;
}

.step-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #6b7280;
  flex-shrink: 0;
}

.step-card.current .step-number {
  background: var(--primary);
  color: white;
}

.step-card.completed .step-number {
  background: #10b981;
  color: white;
}

.step-number .check {
  font-size: 18px;
}

.step-title {
  flex-grow: 1;
  font-weight: 500;
  color: #1f2937;
}

.step-toggle {
  color: #9ca3af;
  font-size: 12px;
}

.step-content {
  padding-top: 16px;
  margin-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.step-description {
  color: #4b5563;
  line-height: 1.7;
  white-space: pre-line;
  margin-bottom: 16px;
}

/* Step Images */
.step-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.step-image {
  background: #f9fafb;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.step-image img {
  width: 100%;
  height: auto;
  display: block;
  cursor: pointer;
  transition: transform 0.2s;
}

.step-image img:hover {
  transform: scale(1.02);
}

.image-caption {
  padding: 12px;
  font-size: 14px;
  color: #6b7280;
  text-align: center;
  border-top: 1px solid #e5e7eb;
  margin: 0;
}

.expected-result {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.expected-result strong {
  color: #166534;
}

.expected-result p {
  margin-top: 8px;
  color: #15803d;
}

/* Notes */
.step-notes {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.note {
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid;
}

.note-info {
  background: #eff6ff;
  border-color: #3b82f6;
}

.note-warning {
  background: #fefce8;
  border-color: #eab308;
}

.note-tip {
  background: #f0fdf4;
  border-color: #22c55e;
}

.note-important {
  background: #fef2f2;
  border-color: #ef4444;
}

.note-example {
  background: #faf5ff;
  border-color: #a855f7;
}

.note-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.note-icon {
  font-size: 18px;
}

.note-title {
  font-weight: 600;
  color: #1f2937;
}

.note-type {
  font-weight: 500;
  color: #6b7280;
}

.note-content {
  color: #4b5563;
  line-height: 1.6;
  white-space: pre-line;
}

.step-actions {
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

/* Criteria */
.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.criteria-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #4f46e5;
  color: white;
}

.criteria-header strong {
  font-size: 20px;
}

.criteria-card {
  padding: 16px 20px;
}

.criteria-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.criteria-name {
  font-weight: 500;
  color: #1f2937;
}

.criteria-score {
  font-weight: 600;
  color: #4f46e5;
  background: #eef2ff;
  padding: 4px 12px;
  border-radius: 16px;
}

.criteria-description {
  margin-top: 8px;
  color: #6b7280;
  font-size: 14px;
}

/* Files */
.files-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.file-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.file-icon {
  font-size: 32px;
  width: 50px;
  text-align: center;
}

.file-info {
  flex-grow: 1;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
}

.file-description {
  color: #6b7280;
  font-size: 14px;
  margin-top: 4px;
}

.file-meta {
  display: flex;
  gap: 12px;
  color: #9ca3af;
  font-size: 13px;
  margin-top: 4px;
}

.file-download {
  font-size: 20px;
  opacity: 0.5;
}

.file-card:hover .file-download {
  opacity: 1;
}
</style>
