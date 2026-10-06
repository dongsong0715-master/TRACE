<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { PhSignOut, PhSquaresFour, PhUserCircle } from '@phosphor-icons/vue'
import { useAuthStore } from '../stores/auth'

withDefaults(defineProps<{ guest?: boolean }>(), { guest: false })
const auth = useAuthStore()
const router = useRouter()
const busy = ref(false)
const error = ref('')
async function logout() {
  busy.value = true
  error.value = ''
  try {
    await auth.logout()
    await router.push('/login')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '退出失败，请重试'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <header class="app-header" :class="{ 'app-header--authenticated': !guest }">
    <RouterLink class="wordmark" :to="guest ? '/login' : '/workspace'" aria-label="TRACE 首页"
      >TRACE</RouterLink
    >
    <nav v-if="!guest" class="main-nav" aria-label="主导航">
      <RouterLink to="/workspace"><PhSquaresFour :size="20" />工作台</RouterLink>
      <RouterLink v-if="auth.user?.role === 'student'" to="/profile"
        ><PhUserCircle :size="20" />个人资料</RouterLink
      >
    </nav>
    <span v-if="guest" class="header-caption">大学生就业赋能平台</span>
    <div v-if="!guest" class="account-nav">
      <PhUserCircle :size="30" weight="duotone" class="account-icon" />
      <span class="account-name">{{ auth.user?.profile?.nickname ?? auth.user?.username }}</span>
      <button class="signout" :disabled="busy" @click="logout">
        <span>{{ busy ? '退出中' : '退出' }}</span
        ><PhSignOut :size="17" />
      </button>
    </div>
  </header>
  <p v-if="error" class="header-error" role="alert">{{ error }}</p>
</template>

<style scoped>
.app-header {
  height: 70px;
  background: #fff;
  color: var(--color-ink);
  border-bottom: 1px solid var(--color-rule);
  display: flex;
  align-items: center;
  padding: 0 32px;
  gap: 48px;
}
.app-header--authenticated {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.96);
  border-bottom-color: rgba(190, 204, 224, 0.55);
  box-shadow: 0 4px 24px rgba(25, 48, 82, 0.06);
}
@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .app-header--authenticated {
    background: rgba(255, 255, 255, 0.72);
    -webkit-backdrop-filter: blur(18px) saturate(145%);
    backdrop-filter: blur(18px) saturate(145%);
  }
}
.wordmark {
  font-size: 25px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.12em;
  text-decoration: none;
}
.main-nav {
  display: flex;
  align-items: stretch;
  height: 100%;
  gap: 38px;
  margin: 0;
}
.main-nav a {
  position: relative;
  display: flex;
  align-items: center;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  color: var(--color-muted);
  gap: 9px;
}
.main-nav .router-link-active {
  color: var(--color-signal);
}
.main-nav .router-link-active::after {
  content: '';
  height: 3px;
  background: var(--color-signal);
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}
.account-nav {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-left: auto;
}
.signout {
  background: none;
  border: none;
  color: var(--color-muted);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}
.account-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
}
.header-caption {
  color: var(--color-muted);
  font-size: 12px;
  letter-spacing: 0.12em;
}
.account-icon {
  color: #8995a8;
}
.header-error {
  padding: 10px 48px;
  background: #fff1f1;
  color: var(--color-error);
  margin: 0;
  font-size: 13px;
}
@media (max-width: 700px) {
  .app-header {
    padding: 0 22px;
    gap: 20px;
  }
  .main-nav {
    gap: 18px;
    margin: 0;
  }
  .main-nav a {
    font-size: 13px;
  }
  .account-nav {
    gap: 8px;
  }
  .account-name,
  .header-caption,
  .account-icon {
    display: none;
  }
  .wordmark {
    font-size: 20px;
  }
}
</style>
