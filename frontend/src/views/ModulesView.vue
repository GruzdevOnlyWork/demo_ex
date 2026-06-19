<script setup>
import { ref, onMounted } from 'vue'
import { useModulesStore } from '../stores/modules'

const modules = useModulesStore()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    await modules.fetchSectionsWithModules()
  } catch (err) {
    error.value = 'Не удалось загрузить модули'
  } finally {
    loading.value = false
  }
})

const getStatusClass = (status) => {
  if (!status) return ''
  return {
    'not_started': '',
    'in_progress': 'status-progress',
    'completed': 'status-completed'
  }[status] || ''
}

const getStatusText = (status) => {
  if (!status) return 'Не начат'
  return {
    'not_started': 'Не начат',
    'in_progress': 'В процессе',
    'completed': 'Завершен'
  }[status] || status
}
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1>Учебные модули</h1>
      <p>Изучите материалы для подготовки к демо-экзамену</p>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div v-if="loading" class="loading">Загрузка модулей...</div>

    <div v-else-if="modules.sections.length === 0" class="empty-state card">
      <p>Пока нет доступных модулей</p>
    </div>

    <div v-else class="sections-list">
      <div v-for="section in modules.sections" :key="section.id" class="section-block">
        <div class="section-header">
          <h2>{{ section.name }}</h2>
          <span class="section-count">{{ section.modules?.length || 0 }} модулей</span>
        </div>
        <p v-if="section.description" class="section-description">{{ section.description }}</p>

        <div class="modules-grid">
          <router-link
            v-for="module in section.modules"
            :key="module.id"
            :to="`/modules/${module.id}`"
            class="module-card card"
          >
            <div class="module-header">
              <h3>{{ module.name }}</h3>
              <span
                v-if="module.user_progress"
                class="module-status"
                :class="getStatusClass(module.user_progress.status)"
              >
                {{ getStatusText(module.user_progress.status) }}
              </span>
            </div>

            <p v-if="module.description" class="module-description">
              {{ module.description }}
            </p>

            <div class="module-meta">
              <span v-if="module.duration" class="meta-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                {{ module.duration }}
              </span>
              <span class="meta-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                {{ module.steps_count }} шагов
              </span>
              <span v-if="module.files_count" class="meta-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z"/>
                  <path d="M13 2v7h7"/>
                </svg>
                {{ module.files_count }} файлов
              </span>
            </div>

            <div v-if="module.user_progress?.status === 'in_progress'" class="module-progress">
              <div class="progress-text">
                Шаг {{ module.user_progress.current_step }} из {{ module.steps_count }}
              </div>
              <div class="progress-bar">
                <div
                  class="progress-bar-fill"
                  :style="{ width: (module.user_progress.current_step / module.steps_count * 100) + '%' }"
                ></div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  color: #4f46e5;
  margin-bottom: 8px;
}

.page-header p {
  color: #6b7280;
  font-size: 18px;
}

.loading, .empty-state {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section-block {
  background: #f9fafb;
  border-radius: 16px;
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.section-header h2 {
  color: #1f2937;
  margin: 0;
}

.section-count {
  color: #6b7280;
  font-size: 14px;
}

.section-description {
  color: #6b7280;
  margin-bottom: 20px;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.module-card {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.module-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 18px;
}

.module-status {
  flex-shrink: 0;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background: #f3f4f6;
  color: #6b7280;
}

.module-status.status-progress {
  background: #fef3c7;
  color: #d97706;
}

.module-status.status-completed {
  background: #dcfce7;
  color: #16a34a;
}

.module-description {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 16px;
  flex-grow: 1;
}

.module-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: #9ca3af;
  font-size: 13px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-item svg {
  opacity: 0.7;
}

.module-progress {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.progress-text {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.progress-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: #4f46e5;
  border-radius: 3px;
  transition: width 0.3s;
}
</style>
