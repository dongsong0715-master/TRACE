<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import {
  PhIdentificationCard,
  PhBriefcase,
  PhChatCircleText,
  PhGraduationCap,
} from '@phosphor-icons/vue'
defineProps<{ mode: 'login' | 'register' }>()
</script>

<template>
  <div class="auth-shell" :class="`auth-shell--${mode}`">
    <AppHeader guest />
    <main class="auth-layout appear">
      <section class="auth-context">
        <img
          class="auth-context-image"
          src="/images/employment-background.png"
          alt=""
          aria-hidden="true"
        />
        <p class="eyebrow">
          <span class="career-badge"><PhGraduationCap :size="17" />从校园到职场</span
          ><span class="career-label">YOUR NEXT CHAPTER</span>
        </p>
        <h1>从校园，<br />走向你的职场。</h1>
        <p class="context-copy muted">
          看见自己的优势，找到适合的机会。<br />为第一次求职，也为更长远的职业旅程。
        </p>
        <ol class="chapter-list">
          <li>
            <PhIdentificationCard :size="26" class="chapter-icon" />
            <div><strong>认识自己</strong><span>从能力与期待出发</span></div>
          </li>
          <li>
            <PhBriefcase :size="26" class="chapter-icon" />
            <div><strong>发现机会</strong><span>阅读岗位与匹配依据</span></div>
          </li>
          <li>
            <PhChatCircleText :size="26" class="chapter-icon" />
            <div><strong>练习表达</strong><span>为真实面试做好准备</span></div>
          </li>
        </ol>
        <p class="career-note">每一次准备，都是迈向未来的一步。</p>
      </section>
      <section class="auth-form-area" :aria-label="mode === 'login' ? '账号登录' : '学生注册'">
        <p class="eyebrow">{{ mode === 'login' ? 'WELCOME BACK' : 'START YOUR JOURNEY' }}</p>
        <h2>{{ mode === 'login' ? '登录你的账号' : '创建学生账号' }}</h2>
        <slot />
      </section>
    </main>
    <footer class="auth-footer page-footer">
      <span>TRACE · 大学生就业赋能平台</span><span>认识 / 探索 / 实践</span>
    </footer>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}
.auth-shell--login {
  height: 100dvh;
  overflow: auto;
  scrollbar-width: none;
}
.auth-shell--login::-webkit-scrollbar {
  display: none;
}
.auth-shell :deep(.app-header) {
  flex-shrink: 0;
}
.auth-layout {
  width: 100%;
  flex: 1 0 auto;
  max-width: 1440px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  padding: 56px 48px 54px;
  gap: 0;
}
.auth-context {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  background: var(--color-soft);
  border: 1px solid var(--color-rule);
  padding: 42px;
  border-radius: 8px 0 0 8px;
}
.auth-context-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: right bottom;
  z-index: -1;
}
.auth-context .eyebrow {
  color: var(--color-muted);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
}
.career-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 3px 9px;
  border: 1px solid #c7daf3;
  border-radius: 999px;
  background: #ffffffcc;
  color: #235592;
  letter-spacing: 0;
}
.career-label {
  font-size: 10px;
  letter-spacing: 0.12em;
}
.auth-context h1 {
  margin: 24px 0;
}
.context-copy {
  font-size: 14px;
  line-height: 1.8;
  max-width: 400px;
}
.chapter-list {
  list-style: none;
  padding: 0;
  margin: 42px 0 0;
  max-width: 300px;
}
.chapter-list li {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 18px 0;
  border-top: 1px solid #d1dceb;
}
.chapter-icon {
  color: var(--color-signal);
  flex-shrink: 0;
}
.chapter-list strong {
  font-size: 16px;
  font-weight: 600;
}
.chapter-list div span {
  display: block;
  color: var(--color-muted);
  font-size: 13px;
  margin-top: 3px;
}
.career-note {
  position: absolute;
  left: 42px;
  bottom: 15px;
  margin: 0;
  font-size: 11px;
  color: #53657b;
  background: #ffffffcc;
  border-radius: 4px;
  padding: 4px 8px;
}
.auth-form-area {
  border: 1px solid var(--color-rule);
  border-left: 0;
  border-radius: 0 8px 8px 0;
  padding: 42px 48px;
}
.auth-form-area h2 {
  margin: 15px 0 32px;
  font-size: 28px;
}
.auth-footer {
  width: calc(100% - 96px);
  flex-shrink: 0;
  max-width: 1344px;
  margin: 0 auto;
  padding: 20px 0 28px;
}
.auth-shell--login .auth-layout {
  padding-block: clamp(16px, 4dvh, 40px);
}
.auth-shell--login .auth-context,
.auth-shell--login .auth-form-area {
  padding-block: clamp(24px, 4dvh, 42px);
}
.auth-shell--login .auth-footer {
  padding-block: 14px 18px;
}
@media (max-width: 900px) {
  .auth-layout {
    gap: 0;
    padding: 42px 32px;
  }
  .auth-form-area {
    padding: 32px;
  }
  .auth-context {
    padding: 32px;
  }
  .career-label,
  .career-note {
    display: none;
  }
  .auth-context h1 {
    font-size: 36px;
  }
  .auth-footer {
    width: calc(100% - 64px);
    margin: 0 32px;
  }
}
@media (max-width: 650px) {
  .auth-layout {
    grid-template-columns: 1fr;
    padding: 32px 22px;
    gap: 0;
    min-height: auto;
  }
  .auth-context h1 {
    font-size: 30px;
    margin: 20px 0;
  }
  .context-copy {
    font-size: 14px;
  }
  .chapter-list {
    display: none;
  }
  .auth-form-area {
    border-left: 1px solid var(--color-rule);
    border-top: 0;
    padding: 28px 24px;
    border-radius: 0 0 8px 8px;
  }
  .auth-context {
    padding: 24px;
    border-radius: 8px 8px 0 0;
  }
  .auth-context-image {
    object-position: center 72%;
  }
  .auth-footer {
    width: calc(100% - 44px);
    margin: 20px 22px 0;
  }
  .auth-shell--login .auth-context {
    padding: 20px 24px;
  }
  .auth-shell--login .auth-context h1 {
    font-size: 24px;
    margin: 0;
  }
  .auth-shell--login .auth-context .eyebrow,
  .auth-shell--login .context-copy {
    display: none;
  }
  .auth-shell--login .auth-footer {
    margin-top: 0;
  }
}
@media (min-width: 651px) and (max-height: 820px) {
  .auth-shell--login .chapter-list {
    margin-top: 24px;
  }
  .auth-shell--login .chapter-list li {
    padding-block: 12px;
  }
}
@media (max-height: 720px) {
  .auth-shell--login :deep(.app-header) {
    height: 60px;
  }
  .auth-shell--login .auth-layout {
    padding-block: 16px;
  }
  .auth-shell--login .auth-context,
  .auth-shell--login .auth-form-area {
    padding-block: 20px;
  }
  .auth-shell--login .chapter-list {
    display: none;
  }
  .auth-shell--login .auth-form-area h2 {
    font-size: 24px;
    margin: 10px 0 20px;
  }
  .auth-shell--login :deep(.field) {
    margin-bottom: 16px;
    gap: 6px;
  }
  .auth-shell--login :deep(.field input) {
    padding-block: 10px;
  }
  .auth-shell--login .auth-footer {
    padding-block: 8px 12px;
  }
}
@media (max-width: 650px) and (max-height: 720px) {
  .auth-shell--login .auth-context {
    display: none;
  }
  .auth-shell--login .auth-form-area {
    border-top: 1px solid var(--color-rule);
    border-radius: 8px;
  }
}
@media (max-height: 520px) {
  .auth-shell--login .auth-layout {
    padding-block: 8px;
  }
  .auth-shell--login .auth-form-area {
    padding-block: 16px;
  }
  .auth-shell--login :deep(.login-signup) {
    margin-top: 16px;
  }
  .auth-shell--login .auth-footer {
    display: none;
  }
}
</style>
