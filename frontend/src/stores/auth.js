import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)

  async function login(username, password) {
    const response = await authApi.login(username, password)
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    await fetchProfile()
  }

  async function register(data) {
    await authApi.register(data)
  }

  async function fetchProfile() {
    if (!accessToken.value) return
    try {
      const response = await authApi.getProfile()
      user.value = response.data
    } catch (error) {
      if (error.response?.status === 401) {
        logout()
      }
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  if (accessToken.value) {
    fetchProfile()
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    login,
    register,
    fetchProfile,
    logout
  }
})
