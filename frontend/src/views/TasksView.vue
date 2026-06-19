<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTasksStore } from '../stores/tasks'

const router = useRouter()
const tasksStore = useTasksStore()

const loading = ref(true)
const selectedCode = ref('')

onMounted(async () => {
  try {
    await tasksStore.fetchVariants()
  } finally {
    loading.value = false
  }
})

const filteredVariants = computed(() => {
  if (!selectedCode.value) return tasksStore.variants
  return tasksStore.variants.filter(v => v.code === selectedCode.value)
})

const uniqueCodes = computed(() => {
  return [...new Set(tasksStore.variants.map(v => v.code))]
})

const openVariant = (variantId) => {
  router.push(`/tasks/${variantId}`)
}
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1>Задания демо-экзамена</h1>
      <p class="page-subtitle">Варианты заданий с пошаговыми инструкциями решения</p>
    </div>

    <div v-if="uniqueCodes.length > 1" class="filters card">
      <div class="filter-group">
        <label for="code-filter">Код экзамена:</label>
        <select id="code-filter" v-model="selectedCode" class="filter-select">
          <option value="">Все варианты</option>
          <option v-for="code in uniqueCodes" :key="code" :value="code">
            {{ code }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="tasksStore.error" class="alert alert-error">
      {{ tasksStore.error }}
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <span>Загрузка заданий...</span>
    </div>

    <div v-else-if="filteredVariants.length === 0" class="empty-state card">
      <div class="empty-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="12" y1="18" x2="12" y2="12"/>
          <line x1="9" y1="15" x2="15" y2="15"/>
        </svg>
      </div>
      <h3>Задания не найдены</h3>
      <p>Пока нет доступных вариантов экзамена</p>
    </div>

    <div v-else class="variants-grid">
      <div
        v-for="variant in filteredVariants"
        :key="variant.id"
        class="variant-card card"
        @click="openVariant(variant.id)"
      >
        <div class="variant-header">
          <span class="variant-badge">{{ variant.code }}</span>
          <span class="variant-number">Вариант {{ variant.variant_number }}</span>
        </div>

        <h3 class="variant-name">{{ variant.name }}</h3>

        <p v-if="variant.description" class="variant-description">
          {{ variant.description.substring(0, 150) }}{{ variant.description.length > 150 ? '...' : '' }}
        </p>

        <div class="variant-meta">
          <div class="meta-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span>{{ variant.sessions_count }} {{ variant.sessions_count === 1 ? 'сессия' : 'сессий' }}</span>
          </div>
          <div class="meta-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            <span>{{ variant.tasks_count }} {{ variant.tasks_count === 1 ? 'задание' : 'заданий' }}</span>
          </div>
          <div v-if="variant.total_time" class="meta-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span>{{ variant.total_time }}</span>
          </div>
        </div>

        <div class="variant-actions">
          <a
            v-if="variant.description_file_url"
            :href="variant.description_file_url"
            target="_blank"
            class="btn btn-outline btn-sm"
            @click.stop
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            Описание
          </a>
          <a
            v-if="variant.task_file_url"
            :href="variant.task_file_url"
            target="_blank"
            class="btn btn-outline btn-sm"
            @click.stop
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            Задание PDF
          </a>
        </div>

        <button class="btn btn-primary variant-open-btn">
          Открыть решение
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #6b7280;
  margin: 0;
}

.filters {
  margin-bottom: 24px;
  padding: 16px 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-group label {
  font-weight: 500;
  color: #374151;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  min-width: 200px;
  background: white;
}

.filter-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

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

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  color: #9ca3af;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-state p {
  color: #6b7280;
  margin: 0;
}

.variants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.variant-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.variant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.variant-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
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

.variant-number {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.variant-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.variant-description {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
  flex-grow: 1;
}

.variant-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
}

.meta-item svg {
  color: #9ca3af;
}

.variant-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #4f46e5;
  color: #4f46e5;
  background: #f5f3ff;
}

.variant-open-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .variants-grid {
    grid-template-columns: 1fr;
  }

  .variant-meta {
    flex-direction: column;
    gap: 8px;
  }

  .variant-actions {
    flex-direction: column;
  }

  .btn-outline {
    justify-content: center;
  }
}
</style>
