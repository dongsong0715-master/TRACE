<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import {
  PhBriefcase,
  PhIdentificationCard,
  PhChatCircleText,
  PhUserCircle,
  PhCaretDown,
  PhCode,
  PhGraduationCap,
  PhMapPin,
  PhPencilSimple,
  PhBookmarkSimple,
  PhPaperPlaneTilt,
  PhLink,
  PhQuotes,
  PhX,
} from '@phosphor-icons/vue'
import { previewJobs } from '../../dev/fixtures'

const selectedId = ref(previewJobs[0]!.id)
const selected = computed(() => previewJobs.find((j) => j.id === selectedId.value)!)
const saved = ref(new Set<string>())
const recorded = ref(new Set<string>())
const dialog = ref<HTMLDialogElement | null>(null)
const detail = ref<HTMLElement | null>(null)
const reasons = ref<HTMLElement | null>(null)
const message = ref('')
async function selectJob(id: string) {
  selectedId.value = id
  await nextTick()
  if (window.matchMedia('(max-width: 1000px)').matches)
    detail.value?.scrollIntoView({ block: 'start', behavior: 'auto' })
}
function toggleSave(id: string) {
  const next = new Set(saved.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  saved.value = next
}
function show(text: string) {
  message.value = text
  dialog.value?.showModal()
}
function record() {
  recorded.value = new Set([...recorded.value, selectedId.value])
  show('本次模拟投递已在预览中记录。这里只验证界面交互，刷新页面后清空。')
}
function showReasons() {
  reasons.value?.scrollIntoView({ block: 'nearest', behavior: 'auto' })
  reasons.value?.focus({ preventScroll: true })
}
</script>

<template>
  <header class="concept-header">
    <RouterLink to="/login" class="concept-brand" aria-label="TRACE 返回登录">TRACE</RouterLink>
    <nav aria-label="风格预览导航">
      <button @click="show('职业诊断将在正式业务模块开发后开放。')">
        <PhIdentificationCard :size="22" />职业诊断
      </button>
      <button class="active" aria-current="page" @click="show('当前正在浏览岗位探索的视觉预览。')">
        <PhBriefcase :size="22" />岗位探索
      </button>
      <button @click="show('面试练习将在正式业务模块开发后开放。')">
        <PhChatCircleText :size="22" />面试练习
      </button>
    </nav>
    <button
      class="concept-account"
      @click="show('苏同学是合成画像。请返回正式登录页面使用自己的账号。')"
    >
      <PhUserCircle :size="32" weight="duotone" /><span>苏同学</span><PhCaretDown :size="15" />
    </button>
  </header>
  <main class="explore-layout">
    <aside class="profile-sidebar" aria-labelledby="portrait-title">
      <h2 id="portrait-title">我的画像</h2>
      <dl>
        <div>
          <PhCode :size="24" />
          <div>
            <dd>Python开发</dd>
            <dt>发展方向</dt>
          </div>
        </div>
        <div>
          <PhGraduationCap :size="24" />
          <div>
            <dd>本科</dd>
            <dt>学历层次</dt>
          </div>
        </div>
        <div>
          <PhMapPin :size="24" />
          <div>
            <dd>北京</dd>
            <dt>期望城市</dt>
          </div>
        </div>
      </dl>
      <div class="sidebar-actions">
        <button
          class="edit-profile"
          @click="show('这里展示的是合成画像。请返回登录，进入个人资料页面编辑自己的信息。')"
        >
          <PhPencilSimple :size="21" />编辑资料
        </button>
      </div>
    </aside>
    <section class="job-list-panel" aria-labelledby="explore-title">
      <h1 id="explore-title">岗位探索</h1>
      <p class="list-intro">基于你的能力画像与岗位要求，推荐以下匹配的实习岗位。</p>
      <div class="list-columns" aria-hidden="true">
        <span>#</span><span>岗位 / 企业</span><span>工作地点</span><span>核心技能要求</span
        ><span></span>
      </div>
      <ol class="job-list">
        <li
          v-for="(job, index) in previewJobs"
          :key="job.id"
          :class="{ selected: job.id === selectedId }"
        >
          <button
            class="job-select"
            :aria-label="`查看${job.title}`"
            :aria-pressed="job.id === selectedId"
            @click="selectJob(job.id)"
          >
            <span class="job-rank">{{ index + 1 }}</span
            ><span class="job-name"
              ><strong>{{ job.title }}</strong
              ><span>{{ job.company }}</span></span
            ><span class="job-city"><PhMapPin :size="20" />北京</span
            ><span class="job-skills">{{ job.skills.replaceAll(' · ', ' / ') }}</span>
          </button>
          <button
            class="row-save"
            :aria-label="`${saved.has(job.id) ? '取消收藏' : '收藏'}${job.title}`"
            :aria-pressed="saved.has(job.id)"
            @click="toggleSave(job.id)"
          >
            <PhBookmarkSimple :size="24" :weight="saved.has(job.id) ? 'fill' : 'regular'" />
          </button>
        </li>
      </ol>
    </section>
    <section ref="detail" class="job-detail" aria-labelledby="job-title">
      <img
        class="desk-photo"
        src="/images/career-desk.png"
        alt="明亮办公桌上的笔记本电脑，屏幕展示代码"
      />
      <div class="detail-title-line">
        <h2 id="job-title">{{ selected.title }}</h2>
        <button
          class="detail-save"
          :aria-label="saved.has(selectedId) ? '取消收藏当前岗位' : '收藏当前岗位'"
          :aria-pressed="saved.has(selectedId)"
          @click="toggleSave(selectedId)"
        >
          <PhBookmarkSimple :size="25" :weight="saved.has(selectedId) ? 'fill' : 'regular'" />
        </button>
      </div>
      <p class="company-line">
        {{ selected.company }}<span><PhMapPin :size="21" />北京</span>
      </p>
      <div class="detail-actions">
        <button class="primary-button" @click="showReasons">查看匹配依据</button
        ><button class="secondary-button" @click="record">
          <PhPaperPlaneTilt :size="24" />{{
            recorded.has(selectedId) ? '已记录模拟投递' : '记录模拟投递'
          }}
        </button>
      </div>
      <section class="requirements">
        <div class="section-title">
          <h3>岗位要求（节选）</h3>
          <span><PhLink :size="17" />来自岗位描述</span>
        </div>
        <blockquote>
          <PhQuotes :size="18" weight="fill" />{{ selected.requirement
          }}<PhQuotes :size="18" weight="fill" />
        </blockquote>
      </section>
      <section ref="reasons" class="reason-section" tabindex="-1" aria-labelledby="reason-title">
        <h3 id="reason-title">为什么适合你</h3>
        <ol>
          <li v-for="(reason, index) in selected.reasons" :key="reason.title">
            <span class="reason-number">{{ index + 1 }}</span>
            <div>
              <strong>{{ reason.title }}</strong>
              <p>{{ reason.body }}</p>
            </div>
          </li>
        </ol>
      </section>
    </section>
  </main>
  <footer class="concept-footer">
    <RouterLink to="/login">返回正式登录</RouterLink
    ><span>视觉预览 · 合成岗位与画像 · 交互仅在当前页面有效</span>
  </footer>
  <dialog ref="dialog" class="preview-dialog">
    <button class="dialog-close text-button" aria-label="关闭" @click="dialog?.close()">
      <PhX :size="22" />
    </button>
    <h2>预览说明</h2>
    <p>{{ message }}</p>
    <button class="primary-button" @click="dialog?.close()">知道了</button>
  </dialog>
</template>

<style scoped>
.concept-header {
  height: 69px;
  background: #fff;
  border-bottom: 1px solid var(--color-rule);
  display: flex;
  align-items: center;
  padding: 0 30px;
}
.concept-brand {
  width: 157px;
  flex-shrink: 0;
  color: #0b0b0d;
  font-size: 25px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-decoration: none;
}
.concept-header nav {
  display: flex;
  height: 100%;
  gap: 46px;
  padding-left: 26px;
}
.concept-header nav button {
  border: 0;
  background: none;
  color: var(--color-muted);
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 0;
  position: relative;
  font-size: 17px;
  font-weight: 600;
}
.concept-header nav .active {
  color: var(--color-signal);
}
.concept-header nav .active::after {
  content: '';
  height: 3px;
  background: var(--color-signal);
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}
.concept-account {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  background: none;
  border: 0;
  color: var(--color-muted);
  font-size: 15px;
  font-weight: 600;
}
.concept-account > svg:first-child {
  color: #94a0b0;
}
.explore-layout {
  display: grid;
  grid-template-columns: 187px minmax(0, 1.124fr) minmax(0, 1fr);
  min-height: calc(100vh - 69px);
}
.profile-sidebar {
  background: #f6f8fa;
  border-right: 1px solid var(--color-rule);
  padding: 34px 25px;
}
.profile-sidebar h2 {
  font-size: 15px;
  color: var(--color-muted);
  margin: 0 6px 25px;
  line-height: 1.7;
}
.profile-sidebar dl {
  margin: 0;
}
.profile-sidebar dl > div {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
  padding-left: 6px;
}
.profile-sidebar dl svg {
  color: var(--color-muted);
  flex-shrink: 0;
  margin-top: 8px;
}
.profile-sidebar dd {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
}
.profile-sidebar dt {
  font-size: 13px;
  color: #66758c;
  margin-top: 2px;
}
.edit-profile {
  border: 1px solid var(--color-rule);
  border-radius: 4px;
  background: none;
  color: var(--color-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 7px 4px;
  margin-top: 0;
  font-size: 15px;
}
.sidebar-actions {
  margin-top: 15px;
  padding-top: 20px;
  border-top: 1px solid var(--color-rule);
}
.job-list-panel {
  padding: 36px 16px 40px;
  min-width: 0;
}
.job-list-panel h1 {
  font-size: 36px;
  line-height: 1.3;
  margin: 0 14px 4px;
  font-weight: 700;
  color: #080b10;
}
.list-intro {
  color: var(--color-muted);
  font-size: 17px;
  margin: 0 14px 44px;
  line-height: 1.7;
}
.list-columns {
  display: grid;
  grid-template-columns: 42px minmax(0, 1.74fr) minmax(80px, 0.92fr) minmax(0, 1.34fr) 32px;
  padding: 0 20px 16px;
  font-size: 14px;
  color: #6f7d92;
}
.job-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.job-list li {
  display: flex;
  align-items: center;
  position: relative;
  min-height: 104px;
  border-top: 1px solid var(--color-rule);
  padding-right: 18px;
}
.job-list li:last-child {
  border-bottom: 1px solid var(--color-rule);
}
.job-list li.selected {
  background: var(--color-tint);
}
.job-list li.selected::before {
  content: '';
  position: absolute;
  width: 5px;
  background: var(--color-signal);
  top: 4px;
  bottom: 4px;
  left: 0;
}
.job-select {
  display: grid;
  grid-template-columns: 42px minmax(0, 1.74fr) minmax(80px, 0.92fr) minmax(0, 1.34fr);
  flex: 1;
  align-items: center;
  padding: 22px 0 22px 20px;
  text-align: left;
  background: none;
  border: 0;
  min-width: 0;
  color: var(--color-ink);
}
.job-rank {
  font-size: 16px;
}
.job-name {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.job-name strong {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.6;
}
.job-name > span,
.job-city,
.job-skills {
  font-size: 15px;
  color: var(--color-muted);
}
.job-city {
  display: flex;
  align-items: center;
  gap: 6px;
}
.job-skills {
  line-height: 1.6;
  padding-right: 8px;
}
.row-save,
.detail-save {
  border: 0;
  background: none;
  color: #41516b;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.selected .row-save,
[aria-pressed='true'].row-save,
[aria-pressed='true'].detail-save {
  color: var(--color-signal);
}
.job-detail {
  border-left: 1px solid var(--color-rule);
  padding: 24px 25px 40px 23px;
  min-width: 0;
  scroll-margin-top: 18px;
}
.desk-photo {
  width: calc(100% + 25px);
  height: 222px;
  object-fit: cover;
  object-position: center;
  display: block;
  margin-bottom: 22px;
}
.detail-title-line {
  display: flex;
  align-items: center;
  gap: 12px;
}
.detail-title-line h2 {
  margin: 0;
  flex: 1;
  font-size: 29px;
  font-weight: 700;
  color: #080b10;
}
.company-line {
  margin: 4px 0 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 26px;
  color: var(--color-muted);
  font-size: 17px;
}
.company-line span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.detail-actions {
  display: flex;
  gap: 19px;
  margin-bottom: 28px;
}
.detail-actions > button {
  flex: 1;
  justify-content: center;
  padding: 12px 8px;
  min-height: 53px;
  gap: 12px;
  font-size: 16px;
  white-space: nowrap;
}
.secondary-button {
  border: 1px solid #c5d1e2;
  border-radius: var(--radius-control);
  background: #fff;
  color: #33435e;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px 16px;
}
.secondary-button:hover,
.edit-profile:hover {
  border-color: var(--color-signal);
  color: var(--color-signal);
  background: var(--color-tint);
}
.requirements {
  border-top: 1px solid var(--color-rule);
  padding-top: 27px;
}
.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}
.section-title h3,
.reason-section h3 {
  font-size: 19px;
  margin: 0;
}
.section-title > span {
  font-size: 13px;
  color: #64738b;
  display: flex;
  align-items: center;
  gap: 9px;
}
.requirements blockquote {
  margin: 0;
  background: #f6f8fa;
  border-radius: 6px;
  padding: 18px 22px;
  color: var(--color-muted);
  font-size: 17px;
  line-height: 1.8;
}
.requirements blockquote svg {
  color: #9eabbd;
  margin-right: 8px;
  vertical-align: -2px;
}
.reason-section {
  margin-top: 32px;
  scroll-margin-top: 24px;
}
.reason-section ol {
  margin: 19px 0 0;
  list-style: none;
  padding: 0;
}
.reason-section li {
  display: flex;
  gap: 23px;
  margin-bottom: 20px;
}
.reason-number {
  flex-shrink: 0;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: var(--color-signal);
  color: #fff;
  display: grid;
  place-items: center;
  font-size: 16px;
}
.reason-section strong {
  font-size: 18px;
  font-weight: 600;
  display: block;
  margin: 0 0 4px;
}
.reason-section p {
  color: var(--color-muted);
  font-size: 16px;
  line-height: 1.7;
  margin: 0;
}
.concept-footer {
  border-top: 1px solid var(--color-rule);
  padding: 18px 30px;
  font-size: 12px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  color: var(--color-muted);
}
.preview-dialog {
  border: 1px solid var(--color-rule);
  border-radius: 8px;
  padding: 38px;
  width: min(480px, calc(100vw - 40px));
  color: var(--color-ink);
}
.preview-dialog::backdrop {
  background: #14233d66;
}
.dialog-close {
  position: absolute;
  right: 16px;
  top: 12px;
}
.preview-dialog p {
  margin-bottom: 28px;
}
@media (max-width: 1250px) and (min-width: 1001px) {
  .explore-layout {
    grid-template-columns: 160px minmax(0, 1.124fr) minmax(0, 1fr);
  }
  .profile-sidebar {
    padding-inline: 16px;
  }
  .job-name strong {
    font-size: 15px;
  }
  .job-name > span,
  .job-city,
  .job-skills {
    font-size: 12px;
  }
  .job-select {
    grid-template-columns: 28px minmax(0, 1.7fr) minmax(62px, 0.7fr) minmax(0, 1fr);
  }
  .list-columns {
    grid-template-columns: 28px minmax(0, 1.7fr) minmax(62px, 0.7fr) minmax(0, 1fr) 32px;
  }
  .detail-title-line h2 {
    font-size: 24px;
  }
  .detail-actions {
    gap: 10px;
  }
  .detail-actions > button {
    font-size: 13px;
    gap: 7px;
  }
}
@media (max-width: 1000px) {
  .explore-layout {
    grid-template-columns: 160px minmax(0, 1fr);
  }
  .profile-sidebar {
    grid-row: span 2;
    padding-inline: 16px;
  }
  .job-detail {
    grid-column: 2;
    border-top: 1px solid var(--color-rule);
    padding: 24px;
  }
  .desk-photo {
    width: 100%;
  }
  .concept-brand {
    width: 130px;
  }
  .concept-header nav {
    padding-left: 0;
    gap: 25px;
  }
  .concept-account span {
    display: none;
  }
}
@media (max-width: 650px) {
  .concept-header {
    padding: 0 18px;
    height: 64px;
    gap: 20px;
  }
  .concept-brand {
    font-size: 20px;
    width: auto;
  }
  .concept-header nav {
    flex: 1;
    gap: 16px;
    justify-content: flex-end;
  }
  .concept-header nav button {
    font-size: 12px;
    gap: 0;
  }
  .concept-header nav svg,
  .concept-account {
    display: none;
  }
  .explore-layout {
    grid-template-columns: 1fr;
  }
  .profile-sidebar {
    padding: 18px;
    grid-row: auto;
    border-right: 0;
    border-bottom: 1px solid var(--color-rule);
  }
  .profile-sidebar h2 {
    margin: 0 0 12px;
    font-size: 13px;
  }
  .profile-sidebar dl {
    display: flex;
    justify-content: space-between;
    gap: 12px;
  }
  .profile-sidebar dl > div {
    padding: 0;
    margin: 0;
    gap: 8px;
  }
  .profile-sidebar dl svg {
    width: 18px;
    margin-top: 3px;
  }
  .profile-sidebar dd {
    font-size: 13px;
  }
  .profile-sidebar dt {
    font-size: 11px;
  }
  .edit-profile {
    width: auto;
    margin-top: 0;
    padding: 6px 12px;
    font-size: 12px;
  }
  .sidebar-actions {
    margin-top: 16px;
    padding-top: 12px;
  }
  .job-list-panel {
    padding: 26px 18px;
  }
  .job-list-panel h1 {
    font-size: 28px;
    margin-inline: 0;
  }
  .list-intro {
    font-size: 14px;
    margin: 6px 0 22px;
  }
  .list-columns {
    display: none;
  }
  .job-list li {
    padding-right: 8px;
    min-height: 96px;
  }
  .job-select {
    grid-template-columns: 25px minmax(0, 1fr) 58px;
    padding: 14px 0 14px 10px;
    row-gap: 2px;
  }
  .job-name strong {
    font-size: 14px;
  }
  .job-name > span,
  .job-city {
    font-size: 12px;
  }
  .job-rank {
    grid-row: span 2;
    font-size: 13px;
  }
  .job-skills {
    grid-column: 2 / 4;
    font-size: 12px;
  }
  .job-detail {
    grid-column: 1;
    border-left: 0;
    padding: 18px;
  }
  .desk-photo {
    height: 160px;
  }
  .detail-title-line h2 {
    font-size: 23px;
  }
  .company-line {
    font-size: 14px;
    margin-block: 8px 16px;
    gap: 14px;
  }
  .detail-actions {
    gap: 10px;
  }
  .detail-actions > button {
    font-size: 13px;
    gap: 7px;
  }
  .section-title h3,
  .reason-section h3 {
    font-size: 17px;
  }
  .section-title > span {
    font-size: 11px;
    gap: 4px;
  }
  .requirements blockquote {
    font-size: 14px;
    padding: 16px;
  }
  .reason-section li {
    gap: 14px;
  }
  .reason-section strong {
    font-size: 16px;
  }
  .reason-section p {
    font-size: 14px;
  }
  .concept-footer {
    padding-inline: 18px;
    flex-wrap: wrap;
  }
}
</style>
