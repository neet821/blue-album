import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 从 localStorage 读取主题设置，默认为 light
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  // 切换主题
  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  // 监听主题变化，保存到 localStorage 并应用到 body
  watch(isDark, (newValue) => {
    localStorage.setItem('theme', newValue ? 'dark' : 'light')
    if (newValue) {
      document.body.classList.add('dark-mode')
    } else {
      document.body.classList.remove('dark-mode')
    }
  }, { immediate: true })

  return {
    isDark,
    toggleTheme
  }
})
