<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const login = async () => {
  error.value = ''
  loading.value = true

  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Неверные учетные данные'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="auth-wrapper">
      <div class="card auth-card">
        <h1>Вход в систему</h1>
        <p class="subtitle">Демо-экзамен "Программные решения для бизнеса"</p>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="login">
          <div class="form-group">
            <label for="username">Логин</label>
            <input
              type="text"
              id="username"
              v-model="username"
              class="form-control"
              required
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>
        </form>

        <p class="auth-link">
          Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
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
  max-width: 400px;
}

.auth-card h1 {
  text-align: center;
  color: #4f46e5;
}

.subtitle {
  text-align: center;
  color: #6b7280;
  margin-bottom: 24px;
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
