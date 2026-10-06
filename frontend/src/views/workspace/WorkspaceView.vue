<script setup lang="ts">
import { computed } from 'vue'
import { PhArrowRight } from '@phosphor-icons/vue'
import AppHeader from '../../components/AppHeader.vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const isStudent = computed(() => auth.user?.role === 'student')
const profile = computed(() => auth.user?.profile)
const education = { college: '专科', bachelor: '本科', master: '硕士' }
const categories = { python: 'Python 开发', frontend: '前端开发', data: '数据分析' }
</script>

<template>
  <AppHeader />
  <main class="page-wrap appear">
    <div class="workspace-grid">
      <section class="workspace-main">
        <p class="eyebrow">YOUR CAREER, IN PROGRESS</p>
        <h1>你好，{{ profile?.nickname ?? auth.user?.username }}。</h1>
        <p class="welcome muted">
          {{ isStudent ? '从认识自己开始，为下一步探索做好准备。' : '欢迎进入 TRACE 管理工作台。' }}
        </p>
        <section v-if="isStudent" class="profile-summary" aria-labelledby="profile-title">
          <p class="eyebrow signal">FIRST THINGS FIRST</p>
          <h2 id="profile-title">先写下你的方向</h2>
          <p class="muted">学历、目标岗位和意向城市，将成为之后探索的起点。</p>
          <dl class="profile-facts">
            <div>
              <dt>学历</dt>
              <dd>{{ profile?.education ? education[profile.education] : '尚未填写' }}</dd>
            </div>
            <div>
              <dt>目标方向</dt>
              <dd>
                {{ profile?.target_category ? categories[profile.target_category] : '尚未填写' }}
              </dd>
            </div>
            <div>
              <dt>意向城市</dt>
              <dd>
                {{
                  profile?.preferred_cities.length
                    ? profile.preferred_cities.join('、')
                    : '尚未填写'
                }}
              </dd>
            </div>
          </dl>
          <RouterLink class="primary-button" to="/profile"
            >{{ profile?.target_category ? '编辑个人资料' : '完善个人资料'
            }}<PhArrowRight :size="20"
          /></RouterLink>
        </section>
        <section v-else class="profile-summary">
          <h2>公共内容维护</h2>
          <p class="muted">岗位与面试题库管理将在后续开放。</p>
        </section>
      </section>
      <aside class="journey" aria-labelledby="journey-title">
        <p class="eyebrow">THE NEXT CHAPTERS</p>
        <h2 id="journey-title">接下来的探索</h2>
        <ol>
          <li>
            <span>01</span>
            <div>
              <h3>职业诊断</h3>
              <p>梳理能力，认识自己的长处。</p>
              <small>即将开放</small>
            </div>
          </li>
          <li>
            <span>02</span>
            <div>
              <h3>岗位探索</h3>
              <p>发现机会，理解匹配依据。</p>
              <small>即将开放</small>
            </div>
          </li>
          <li>
            <span>03</span>
            <div>
              <h3>面试练习</h3>
              <p>练习表达，积累面试经验。</p>
              <small>即将开放</small>
            </div>
          </li>
        </ol>
      </aside>
    </div>
    <footer class="page-footer">
      <span>TRACE · 大学生就业赋能平台</span><span v-if="auth.user?.is_demo">当前为演示环境</span>
    </footer>
  </main>
</template>

<style scoped>
.workspace-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 50px;
  min-height: calc(100vh - 208px);
  padding-bottom: 60px;
}
.workspace-main h1 {
  margin: 20px 0 25px;
  overflow-wrap: anywhere;
}
.welcome {
  font-size: 17px;
}
.profile-summary {
  margin-top: 36px;
  border: 1px solid var(--color-rule);
  background: var(--color-soft);
  border-radius: 8px;
  padding: 30px;
}
.profile-summary h2 {
  margin: 12px 0;
}
.profile-facts {
  display: grid;
  grid-template-columns: 1fr 1fr 1.3fr;
  gap: 20px;
  margin: 36px 0;
}
.profile-facts dt {
  color: var(--color-muted);
  font-size: 12px;
  margin-bottom: 8px;
}
.profile-facts dd {
  margin: 0;
  font-weight: 600;
  overflow-wrap: anywhere;
}
.journey {
  border-left: 1px solid var(--color-rule);
  padding-left: 44px;
}
.journey h2 {
  margin: 12px 0 44px;
}
.journey ol {
  list-style: none;
  margin: 0;
  padding: 0;
}
.journey li {
  padding: 26px 0;
  display: flex;
  gap: 24px;
  border-bottom: 1px solid var(--color-rule);
}
.journey li:first-child {
  padding-top: 0;
}
.journey li > span {
  font: 500 26px/1.4 var(--font-number);
  color: var(--color-signal);
}
.journey h3 {
  margin: 0 0 8px;
}
.journey p {
  font-size: 13px;
  color: var(--color-muted);
  margin-bottom: 12px;
}
.journey small {
  font-size: 11px;
  color: #6d6d6d;
}
@media (max-width: 900px) {
  .workspace-grid {
    grid-template-columns: 1fr;
    gap: 55px;
  }
  .journey {
    padding-left: 0;
    border-left: 0;
  }
  .journey h2 {
    margin-bottom: 25px;
  }
  .profile-summary {
    margin-top: 42px;
  }
}
@media (max-width: 550px) {
  .profile-facts {
    grid-template-columns: 1fr;
  }
}
</style>
