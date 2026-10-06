<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import AppHeader from '../../components/AppHeader.vue'
const auth = useAuthStore()
const router = useRouter()
const busy = ref(false)
async function retry() {
  busy.value = true
  await auth.restore(true)
  busy.value = false
  if (!auth.connectionError) await router.replace(auth.user ? '/workspace' : '/login')
}
</script>
<template>
  <AppHeader guest />
  <main class="page-wrap">
    <p class="eyebrow">CONNECTION INTERRUPTED</p>
    <h1>暂时无法连接</h1>
    <p class="muted" role="alert">{{ auth.connectionError || '服务暂不可用，请稍后再试。' }}</p>
    <button class="primary-button" :disabled="busy" @click="retry">
      {{ busy ? '正在重试…' : '重新连接' }}
    </button>
  </main>
</template>
