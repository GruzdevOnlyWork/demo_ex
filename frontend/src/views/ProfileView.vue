<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const form = ref({
  first_name: auth.user?.first_name || '',
  last_name: auth.user?.last_name || '',
  email: auth.user?.email || '',
  group: auth.user?.group || ''
})

const loading = ref(false)
const success = ref('')
const error = ref('')

const user = computed(() => auth.user)
if (user.value) {
  form.value = {
    first_name: user.value.first_name || '',
    last_name: user.value.last_name || '',
    email: user.value.email || '',
    group: user.value.group || ''
  }
}

const updateProfile = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const { authApi } = await import('../api')
    await authApi.updateProfile(form.value)
    await auth.fetchProfile()
    success.value = 'Профиль успешно обновлен'
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при обновлении профиля'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="profile-container">
      <div class="card">
        <h1>Профиль</h1>

        <div v-if="success" class="alert alert-success">{{ success }}</div>
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label>Логин</label>
            <input
              type="text"
              :value="auth.user?.username"
              class="form-control"
              disabled
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="first_name">Имя</label>
              <input
                type="text"
                id="first_name"
                v-model="form.first_name"
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="last_name">Фамилия</label>
              <input
                type="text"
                id="last_name"
                v-model="form.last_name"
                class="form-control"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label for="group">Группа</label>
            <input
              type="text"
              id="group"
              v-model="form.group"
              class="form-control"
              placeholder="Например: ИС-21"
            />
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 0 auto;
}

h1 {
  color: #4f46e5;
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.btn {
  margin-top: 8px;
}
</style>
