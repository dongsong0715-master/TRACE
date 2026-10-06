<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PhArrowRight } from '@phosphor-icons/vue'
import AuthLayout from '../../components/AuthLayout.vue'
import PasswordField from '../../components/PasswordField.vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const username = ref(typeof route.query.username === 'string' ? route.query.username : '')
const password = ref('')
const busy = ref(false)
const error = ref('')
async function submit() {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    password.value = ''
    await router.push('/workspace')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '登录失败，请重试'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <AuthLayout mode="login">
    <p v-if="route.query.registered" class="success-message" role="status">账号已创建，请登录。</p>
    <p v-if="error || auth.connectionError" class="error-message" role="alert">
      {{ error || auth.connectionError }}
    </p>
    <form @submit.prevent="submit">
      <div class="field">
        <label for="username">用户名</label
        ><input
          id="username"
          v-model="username"
          autocomplete="username"
          required
          minlength="3"
          maxlength="64"
          pattern="[a-zA-Z0-9_]+"
          spellcheck="false"
          autocapitalize="none"
          placeholder="你的用户名"
        />
      </div>
      <PasswordField
        id="password"
        v-model="password"
        label="密码"
        autocomplete="current-password"
      />
      <button class="primary-button" style="width: 100%" :disabled="busy" type="submit">
        {{ busy ? '正在登录…' : '登录' }}<PhArrowRight :size="20" />
      </button>
    </form>
    <p class="login-signup muted">
      还没有账号？
      <RouterLink to="/register" style="color: var(--color-ink)">创建学生账号</RouterLink>
    </p>
  </AuthLayout>
</template>

<style scoped>
.login-signup {
  margin: 24px 0 0;
  font-size: 14px;
}
</style>
