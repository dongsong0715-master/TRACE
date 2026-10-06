<script setup lang="ts">
import { ref } from 'vue'
import { PhEye, PhEyeSlash } from '@phosphor-icons/vue'
defineProps<{
  id: string
  label: string
  autocomplete: 'current-password' | 'new-password'
  hint?: string
}>()
const model = defineModel<string>({ required: true })
const visible = ref(false)
</script>

<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <div class="password-wrap">
      <input
        :id="id"
        v-model="model"
        :type="visible ? 'text' : 'password'"
        required
        minlength="8"
        maxlength="128"
        :autocomplete="autocomplete"
        :aria-describedby="hint ? `${id}-hint` : undefined"
      />
      <button
        type="button"
        class="password-toggle"
        :aria-label="visible ? '隐藏密码' : '显示密码'"
        :aria-pressed="visible"
        @click="visible = !visible"
      >
        <PhEyeSlash v-if="visible" :size="20" /><PhEye v-else :size="20" />
      </button>
    </div>
    <small v-if="hint" :id="`${id}-hint`">{{ hint }}</small>
  </div>
</template>
