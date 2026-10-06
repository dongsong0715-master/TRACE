<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { PhArrowRight } from '@phosphor-icons/vue'
import { accountApi } from '../../api/accounts'
import AuthLayout from '../../components/AuthLayout.vue'
import PasswordField from '../../components/PasswordField.vue'

const router = useRouter()
const username = ref('')
const nickname = ref('')
const password = ref('')
const confirm = ref('')
const busy = ref(false)
const error = ref('')
async function submit() {
  if (busy.value) return
  error.value = ''
  if (password.value !== confirm.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  if (!nickname.value.trim()) {
    error.value = '请输入昵称'
    return
  }
  busy.value = true
  try {
    await accountApi.register(username.value, password.value, nickname.value.trim())
    password.value = ''
    confirm.value = ''
    await router.push({
      path: '/login',
      query: { registered: '1', username: username.value.toLowerCase() },
    })
  } catch (e) {
    error.value = e instanceof Error ? e.message : '注册失败，请重试'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <AuthLayout mode="register">
    <p v-if="error" class="error-message" role="alert">{{ error }}</p>
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
          aria-describedby="username-hint"
        /><small id="username-hint">3–64位字母、数字或下划线，字母不区分大小写。</small>
      </div>
      <div class="field">
        <label for="nickname">昵称</label
        ><input
          id="nickname"
          v-model="nickname"
          autocomplete="nickname"
          required
          maxlength="64"
          placeholder="我们该如何称呼你"
        />
      </div>
      <PasswordField
        id="password"
        v-model="password"
        label="密码"
        autocomplete="new-password"
        hint="8–128位，请使用独立的账号密码。"
      />
      <PasswordField id="confirm" v-model="confirm" label="确认密码" autocomplete="new-password" />
      <button class="primary-button" style="width: 100%" :disabled="busy" type="submit">
        {{ busy ? '正在创建…' : '创建账号' }}<PhArrowRight :size="20" />
      </button>
    </form>
    <p class="muted" style="margin: 24px 0 0; font-size: 14px">
      已有账号？ <RouterLink to="/login" style="color: var(--color-ink)">返回登录</RouterLink>
    </p>
  </AuthLayout>
</template>
