import { ref } from 'vue'
import type { Ref } from 'vue'

export function useLoading(initialState = false) {
  const loading = ref(initialState) as Ref<boolean>

  const startLoading = () => {
    loading.value = true
  }

  const stopLoading = () => {
    loading.value = false
  }

  return {
    loading,
    startLoading,
    stopLoading
  }
}
