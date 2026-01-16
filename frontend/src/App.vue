<script setup>
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const isAuthenticated = computed(() => auth.isAuthenticated)
const user = computed(() => auth.user)

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <nav class="navbar" v-if="isAuthenticated">
      <div class="container">
        <router-link to="/" class="navbar-brand">Демо-Экзамен</router-link>
        <div class="navbar-nav">
          <router-link to="/modules">Модули</router-link>
          <router-link to="/">Тесты</router-link>
          <router-link to="/history">История</router-link>
          <router-link to="/profile">Профиль</router-link>
          <a href="#" @click.prevent="logout">Выход</a>
        </div>
      </div>
    </nav>

    <main>
      <router-view />
    </main>
  </div>
</template>
