import { Ref, onMounted, onUnmounted } from 'vue'

export interface ChartInstance {
  resize: () => void
  getInstance: () => any
}

export function useChart(_chartRef: Ref<HTMLElement | null>) {
  let chartInstance: any = null

  const resize = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }

  const getInstance = () => chartInstance

  const setInstance = (instance: any) => {
    chartInstance = instance
  }

  onMounted(() => {
    window.addEventListener('resize', resize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resize)
    if (chartInstance) {
      chartInstance.dispose()
      chartInstance = null
    }
  })

  return {
    resize,
    getInstance,
    setInstance
  }
}
