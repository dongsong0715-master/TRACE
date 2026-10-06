<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { PhArrowRight } from '@phosphor-icons/vue'
import AppHeader from '../../components/AppHeader.vue'
import { useAuthStore } from '../../stores/auth'
import { ApiError } from '../../api/client'
import type { Profile } from '../../api/types'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({
  nickname: '',
  education: '' as Profile['education'] | '',
  category: '' as Profile['target_category'] | '',
  cities: '',
  version: 1,
})
const busy = ref(false)
const error = ref('')
const saved = ref(false)
const conflict = ref(false)
function populate() {
  const p = auth.user?.profile
  if (p)
    Object.assign(form, {
      nickname: p.nickname,
      education: p.education ?? '',
      category: p.target_category ?? '',
      cities: p.preferred_cities.join('、'),
      version: p.version,
    })
}
populate()
async function reload() {
  busy.value = true
  try {
    await auth.restore(true)
    if (auth.connectionError) {
      error.value = auth.connectionError
      return
    }
    if (!auth.user) {
      await router.push('/login')
      return
    }
    populate()
    conflict.value = false
    error.value = ''
    saved.value = false
  } finally {
    busy.value = false
  }
}
async function submit() {
  if (busy.value) return
  error.value = ''
  saved.value = false
  conflict.value = false
  const cities = form.cities
    .split(/[,，、]/)
    .map((c) => c.trim())
    .filter(Boolean)
  if (cities.length > 5 || new Set(cities).size !== cities.length) {
    error.value = '最多填写5个城市，请勿重复。'
    return
  }
  if (!form.nickname.trim()) {
    error.value = '请输入昵称。'
    return
  }
  busy.value = true
  try {
    await auth.saveProfile({
      version: form.version,
      nickname: form.nickname.trim(),
      education: form.education || null,
      target_category: form.category || null,
      preferred_cities: cities,
    })
    populate()
    saved.value = true
  } catch (e) {
    error.value = e instanceof Error ? e.message : '保存失败'
    if (e instanceof ApiError && e.status === 401) await router.push('/login')
    if (e instanceof ApiError && e.code === 'PROFILE_VERSION_CONFLICT') conflict.value = true
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <AppHeader />
  <main class="page-wrap profile-layout appear">
    <section>
      <p class="eyebrow">YOUR STARTING POINT</p>
      <h1>个人资料</h1>
      <p class="muted">写下现在的方向，之后也可以随时调整。</p>
      <dl class="account-facts">
        <dt>用户名</dt>
        <dd>{{ auth.user?.username }}</dd>
        <dt>账号类型</dt>
        <dd>学生</dd>
      </dl>
      <RouterLink to="/workspace" class="text-button"
        >返回工作台 <PhArrowRight :size="18"
      /></RouterLink>
    </section>
    <section class="profile-form">
      <h2>关于你</h2>
      <p v-if="error" class="error-message" role="alert">{{ error }}</p>
      <p v-if="saved" class="success-message" role="status">个人资料已保存。</p>
      <button v-if="conflict" class="text-button" :disabled="busy" @click="reload">
        重新载入最新资料（替换当前输入）<PhArrowRight :size="18" />
      </button>
      <form @submit.prevent="submit">
        <div class="field">
          <label for="nickname">昵称</label
          ><input
            id="nickname"
            v-model="form.nickname"
            required
            maxlength="64"
            autocomplete="nickname"
          />
        </div>
        <div class="field">
          <label for="education">学历</label
          ><select id="education" v-model="form.education">
            <option value="">暂未确定</option>
            <option value="college">专科</option>
            <option value="bachelor">本科</option>
            <option value="master">硕士</option>
          </select>
        </div>
        <div class="field">
          <label for="category">目标岗位方向</label
          ><select id="category" v-model="form.category">
            <option value="">暂未确定</option>
            <option value="python">Python 开发</option>
            <option value="frontend">前端开发</option>
            <option value="data">数据分析</option>
          </select>
        </div>
        <div class="field">
          <label for="cities">意向城市</label
          ><input
            id="cities"
            v-model="form.cities"
            maxlength="320"
            aria-describedby="cities-hint"
            placeholder="例如：北京、天津"
          /><small id="cities-hint">最多5个城市，用逗号或顿号分隔；也可以先留空。</small>
        </div>
        <button class="primary-button" type="submit" :disabled="busy">
          {{ busy ? '正在保存…' : '保存资料' }}<PhArrowRight :size="20" />
        </button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 7vw;
  padding-top: 70px;
}
h1 {
  margin: 22px 0;
}
.profile-form {
  border-left: 1px solid var(--color-rule);
  padding-left: 64px;
  max-width: 640px;
}
.profile-form h2 {
  margin-bottom: 32px;
}
.account-facts {
  margin: 42px 0;
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 14px;
  font-size: 14px;
}
.account-facts dt {
  color: var(--color-muted);
}
.account-facts dd {
  margin: 0;
  overflow-wrap: anywhere;
}
@media (max-width: 750px) {
  .profile-layout {
    grid-template-columns: 1fr;
    padding-top: 32px;
    gap: 30px;
  }
  .profile-form {
    border-left: 0;
    border-top: 1px solid var(--color-rule);
    padding: 28px 0;
  }
}
</style>
