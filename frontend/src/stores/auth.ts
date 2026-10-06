import { defineStore } from 'pinia'
import { ref } from 'vue'
import { accountApi } from '../api/accounts'
import { ApiError } from '../api/client'
import type { Account, ProfileUpdate } from '../api/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<Account | null>(null)
  const initialized = ref(false)
  const connectionError = ref('')
  let pending: Promise<void> | null = null

  async function restore(force = false): Promise<void> {
    if (pending) return pending
    if (initialized.value && !force) return
    pending = (async () => {
      connectionError.value = ''
      try {
        user.value = await accountApi.me()
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) user.value = null
        else connectionError.value = error instanceof Error ? error.message : '无法连接服务'
      } finally {
        initialized.value = true
        pending = null
      }
    })()
    return pending
  }

  async function login(username: string, password: string) {
    user.value = await accountApi.login(username, password)
    connectionError.value = ''
    initialized.value = true
  }

  async function logout() {
    try {
      await accountApi.logout()
    } catch (error) {
      if (!(error instanceof ApiError && error.status === 401)) throw error
    }
    user.value = null
    initialized.value = true
  }

  async function saveProfile(payload: ProfileUpdate) {
    try {
      const profile = await accountApi.saveProfile(payload)
      if (user.value) user.value.profile = profile
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) user.value = null
      throw error
    }
  }

  return { user, initialized, connectionError, restore, login, logout, saveProfile }
})
