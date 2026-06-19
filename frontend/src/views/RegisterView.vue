<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  group: '',
  password: '',
  password_confirm: ''
})
const error = ref('')
const loading = ref(false)

const register = async () => {
  error.value = ''
  loading.value = true

  try {
    await auth.register(form.value)
    await auth.login(form.value.username, form.value.password)
    router.push('/')
  } catch (err) {
    const errors = err.response?.data
    if (errors) {
      const messages = Object.entries(errors)
        .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
        .join('\n')
      error.value = messages
    } else {
      error.value = 'Ошибка регистрации'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="auth-wrapper">
      <div class="card auth-card">
        <h1>Регистрация</h1>

        <div v-if="error" class="alert alert-error" style="white-space: pre-line">{{ error }}</div>

        <form @submit.prevent="register">
          <div class="form-group">
            <label for="username">Логин *</label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              class="form-control"
              required
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
            <label for="group">Группа</label>
            <input
              type="text"
              id="group"
              v-model="form.group"
              class="form-control"
              placeholder="Например: ИС-21"
            />
          </div>

          <div class="form-group">
            <label for="password">Пароль *</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              class="form-control"
              required
              minlength="8"
            />
          </div>

          <div class="form-group">
            <label for="password_confirm">Подтверждение пароля *</label>
            <input
              type="password"
              id="password_confirm"
              v-model="form.password_confirm"
              class="form-control"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
        </form>

        <p class="auth-link">
          Уже есть аккаунт? <router-link to="/login">Войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 450px;
}

.auth-card h1 {
  text-align: center;
  color: #4f46e5;
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.btn-block {
  width: 100%;
  margin-top: 8px;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  color: #6b7280;
}

.auth-link a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}
</style>
