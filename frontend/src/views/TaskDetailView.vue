<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTasksStore } from '../stores/tasks'
import { useModulesStore } from '../stores/modules'

const route = useRoute()
const router = useRouter()
const tasksStore = useTasksStore()
const modulesStore = useModulesStore()

const loading = ref(true)
const expandedSessions = ref([])

const variant = computed(() => tasksStore.currentVariant)

onMounted(async () => {
  try {
    await tasksStore.fetchVariant(route.params.id)
    if (variant.value?.sessions?.length) {
      expandedSessions.value = [variant.value.sessions[0].id]
    }
  } finally {
    loading.value = false
  }
})

const toggleSession = (sessionId) => {
  const index = expandedSessions.value.indexOf(sessionId)
  if (index === -1) {
    expandedSessions.value.push(sessionId)
  } else {
    expandedSessions.value.splice(index, 1)
  }
}

const isSessionExpanded = (sessionId) => {
  return expandedSessions.value.includes(sessionId)
}

const openTask = (taskId) => {
  router.push(`/modules/${taskId}`)
}

const getStatusClass = (status) => {
  if (!status) return ''
  return {
    'not_started': '',
    'in_progress': 'status-progress',
    'completed': 'status-completed'
  }[status] || ''
}

const getStatusText = (status) => {
  if (!status) return 'Не начато'
  return {
    'not_started': 'Не начато',
    'in_progress': 'В процессе',
    'completed': 'Завершено'
  }[status] || status
}
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <span>Загрузка варианта...</span>
    </div>

    <div v-else-if="tasksStore.error" class="error-state card">
      <div class="alert alert-error">{{ tasksStore.error }}</div>
      <router-link to="/tasks" class="btn btn-primary">
        Вернуться к заданиям
      </router-link>
    </div>

    <div v-else-if="variant" class="variant-page">
      <div class="variant-header card">
        <div class="header-top">
          <router-link to="/tasks" class="back-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            К заданиям
          </router-link>
          <span class="variant-badge">{{ variant.code }}</span>
        </div>

        <h1 class="variant-title">
          Вариант {{ variant.variant_number }}: {{ variant.name }}
        </h1>

        <p v-if="variant.description" class="variant-description">
          {{ variant.description }}
        </p>

        <div class="variant-meta">
          <div v-if="variant.total_time" class="meta-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span>{{ variant.total_time }}</span>
          </div>
          <div class="meta-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span>{{ variant.sessions?.length || 0 }} сессий</span>
          </div>
        </div>

        <div class="variant-files">
          <a
            v-if="variant.description_file_url"
            :href="variant.description_file_url"
            target="_blank"
            class="file-link"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            Описание предметной области (PDF)
          </a>
          <a
            v-if="variant.task_file_url"
            :href="variant.task_file_url"
            target="_blank"
            class="file-link"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            Задание (PDF)
          </a>
        </div>
      </div>

      <div class="sessions-list">
        <div
          v-for="session in variant.sessions"
          :key="session.id"
          class="session-block"
        >
          <div
            class="session-header"
            :class="{ expanded: isSessionExpanded(session.id) }"
            @click="toggleSession(session.id)"
          >
            <div class="session-info">
              <span v-if="session.session_number" class="session-number">
                Сессия {{ session.session_number }}
              </span>
              <h2 class="session-name">{{ session.name }}</h2>
              <span class="session-tasks-count">{{ session.tasks?.length || 0 }} заданий</span>
            </div>
            <div class="session-toggle">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                :class="{ rotated: isSessionExpanded(session.id) }"
              >
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <p v-if="session.description && isSessionExpanded(session.id)" class="session-description">
            {{ session.description }}
          </p>

          <div v-if="isSessionExpanded(session.id)" class="tasks-list">
            <div
              v-for="task in session.tasks"
              :key="task.id"
              class="task-card"
              @click="openTask(task.id)"
            >
              <div class="task-header">
                <span v-if="task.task_number" class="task-number">{{ task.task_number }}</span>
                <h3 class="task-name">{{ task.name }}</h3>
                <span
                  v-if="task.user_progress"
                  class="task-status"
                  :class="getStatusClass(task.user_progress.status)"
                >
                  {{ getStatusText(task.user_progress.status) }}
                </span>
              </div>

              <p v-if="task.description" class="task-description">
                {{ task.description }}
              </p>

              <div class="task-meta">
                <span v-if="task.duration" class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  {{ task.duration }}
                </span>
                <span class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="8" y1="6" x2="21" y2="6"/>
                    <line x1="8" y1="12" x2="21" y2="12"/>
                    <line x1="8" y1="18" x2="21" y2="18"/>
                    <line x1="3" y1="6" x2="3.01" y2="6"/>
                    <line x1="3" y1="12" x2="3.01" y2="12"/>
                    <line x1="3" y1="18" x2="3.01" y2="18"/>
                  </svg>
                  {{ task.steps_count }} шагов
                </span>
                <span v-if="task.files_count" class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  {{ task.files_count }} файлов
                </span>
                <span class="meta-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                  </svg>
                  {{ task.max_score }} баллов
                </span>
              </div>

              <div v-if="task.user_progress?.status === 'in_progress'" class="task-progress">
                <div class="progress-text">
                  Шаг {{ task.user_progress.current_step }} из {{ task.steps_count }}
                </div>
                <div class="progress-bar">
                  <div
                    class="progress-bar-fill"
                    :style="{ width: (task.user_progress.current_step / task.steps_count * 100) + '%' }"
                  ></div>
                </div>
              </div>

              <div class="task-action">
                <span class="action-text">Открыть</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12 5 19 12 12 19"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.variant-header {
  margin-bottom: 24px;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.back-link:hover {
  color: #4f46e5;
}

.variant-badge {
  display: inline-block;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.variant-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.variant-description {
  color: #6b7280;
  line-height: 1.6;
  margin: 0 0 20px 0;
  white-space: pre-line;
}

.variant-meta {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  font-size: 14px;
}

.meta-item svg {
  color: #9ca3af;
}

.variant-files {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.file-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f3f4f6;
  border-radius: 8px;
  color: #374151;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.file-link:hover {
  background: #e5e7eb;
  color: #4f46e5;
}

.file-link svg {
  color: #6b7280;
}

.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.session-block {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.session-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  cursor: pointer;
  transition: background 0.2s;
}

.session-header:hover {
  background: #f9fafb;
}

.session-header.expanded {
  border-bottom: 1px solid #e5e7eb;
}

.session-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.session-number {
  display: inline-block;
  background: #dbeafe;
  color: #1d4ed8;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
}

.session-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0;
}

.session-tasks-count {
  color: #6b7280;
  font-size: 14px;
}

.session-toggle svg {
  color: #9ca3af;
  transition: transform 0.2s;
}

.session-toggle svg.rotated {
  transform: rotate(180deg);
}

.session-description {
  padding: 0 24px 16px;
  color: #6b7280;
  font-size: 14px;
  margin: 0;
  line-height: 1.6;
}

.tasks-list {
  padding: 16px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.task-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.task-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.task-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
}

.task-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0;
  flex-grow: 1;
}

.task-status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background: #f3f4f6;
  color: #6b7280;
}

.task-status.status-progress {
  background: #fef3c7;
  color: #92400e;
}

.task-status.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.task-description {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 12px;
}

.task-meta .meta-item {
  font-size: 13px;
}

.task-progress {
  margin-bottom: 12px;
}

.progress-text {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 6px;
}

.progress-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 3px;
  transition: width 0.3s;
}

.task-action {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4f46e5;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .variant-meta {
    flex-direction: column;
    gap: 12px;
  }

  .variant-files {
    flex-direction: column;
  }

  .session-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .task-header {
    flex-wrap: wrap;
  }

  .task-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
