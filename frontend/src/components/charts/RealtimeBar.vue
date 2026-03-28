<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'

interface RealtimeItem {
  id: string | number
  text: string
  time?: string
}

interface Props {
  data?: RealtimeItem[]
  speed?: number
  height?: string
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  speed: 50,
  height: '40px',
  theme: 'light'
})

const scrollRef = ref<HTMLElement | null>(null)
const isPaused = ref(false)
let animationId: number | null = null

const isEmpty = computed(() => {
  return !props.data || props.data.length === 0
})

const combinedText = computed(() => {
  return props.data.map(item => item.text).join('  |  ')
})

const containerStyle = computed(() => ({
  height: props.height,
  lineHeight: props.height,
  overflow: 'hidden',
  backgroundColor: props.theme === 'dark' ? 'rgba(26, 31, 60, 0.8)' : '#f5f7fa',
  borderRadius: props.theme === 'dark' ? '0' : '4px',
  border: props.theme === 'dark' ? '1px solid rgba(0, 240, 255, 0.3)' : '1px solid #d9d9d9'
}))

const textStyle = computed(() => ({
  color: props.theme === 'dark' ? '#00ffcc' : '#409EFF',
  fontSize: '14px',
  whiteSpace: 'nowrap'
}))

const iconStyle = computed(() => ({
  color: props.theme === 'dark' ? '#00f0ff' : '#409EFF'
}))

const startAnimation = () => {
  if (!scrollRef.value || isEmpty.value) return

  const el = scrollRef.value.querySelector('.scroll-content') as HTMLElement
  if (!el) return

  let position = 0
  const containerWidth = scrollRef.value.offsetWidth
  const textWidth = el.scrollWidth

  const animate = () => {
    if (isPaused.value) {
      animationId = requestAnimationFrame(animate)
      return
    }

    position -= props.speed

    if (Math.abs(position) >= textWidth) {
      position = containerWidth
    }

    el.style.transform = `translateX(${position}px)`
    animationId = requestAnimationFrame(animate)
  }

  animationId = requestAnimationFrame(animate)
}

const stopAnimation = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
}

const handleMouseEnter = () => {
  isPaused.value = true
}

const handleMouseLeave = () => {
  isPaused.value = false
}

onMounted(() => {
  startAnimation()
})

onUnmounted(() => {
  stopAnimation()
})
</script>

<template>
  <div
    ref="scrollRef"
    class="realtime-bar"
    :style="containerStyle"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div class="icon-wrapper" :style="iconStyle">
      <slot name="icon">
        <span class="default-icon">&#128276;</span>
      </slot>
    </div>
    <div class="scroll-content" :style="textStyle">
      {{ combinedText }}
    </div>
  </div>
</template>

<style scoped>
.realtime-bar {
  display: flex;
  align-items: center;
  padding: 0 16px;
  width: 100%;
}

.icon-wrapper {
  flex-shrink: 0;
  margin-right: 12px;
  font-size: 18px;
}

.default-icon {
  font-size: 18px;
}

.scroll-content {
  flex: 1;
  overflow: hidden;
  will-change: transform;
}
</style>
