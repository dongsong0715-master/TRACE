<script setup lang="ts">
import AppHeader from '../../components/AppHeader.vue'
</script>
<template>
  <AppHeader guest />
  <main class="page-wrap">
    <p class="eyebrow">404 / PAGE NOT FOUND</p>
    <h1>这里还没有页面。</h1>
    <p class="muted">检查一下地址，或回到你的工作台。</p>
    <RouterLink class="primary-button" to="/workspace">回到工作台</RouterLink>
  </main>
</template>
