<script setup lang="ts">
/**
 * ChartCard - 图表卡片组件
 * 用于包裹 ECharts 图表，提供标题、加载状态和刷新功能
 */
import { ref } from 'vue'
import { Refresh, Loading } from '@element-plus/icons-vue'

interface Props {
  title: string
  subTitle?: string
  height?: string
  loading?: boolean
  refreshable?: boolean
}

withDefaults(defineProps<Props>(), {
  height: '300px',
  loading: false,
  refreshable: false
})

const emit = defineEmits<{
  (e: 'refresh'): void
}>()

const chartRef = ref<HTMLElement | null>(null)

const handleRefresh = () => {
  emit('refresh')
}
</script>

<template>
  <div class="chart-card">
    <div class="chart-card__header">
      <div class="chart-card__title-wrapper">
        <h3 class="chart-card__title">{{ title }}</h3>
        <span v-if="subTitle" class="chart-card__sub-title">{{ subTitle }}</span>
      </div>
      <div v-if="refreshable || $slots.actions" class="chart-card__actions">
        <slot name="actions" />
        <el-button
          v-if="refreshable"
          :icon="Refresh"
          circle
          size="small"
          @click="handleRefresh"
        />
      </div>
    </div>

    <div
      ref="chartRef"
      class="chart-card__body"
      :style="{ height }"
    >
      <div v-if="loading" class="chart-card__loading">
        <el-icon class="is-loading" :size="32">
          <Loading />
        </el-icon>
      </div>
      <slot v-else name="chart" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
  }

  &__title-wrapper {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  &__title {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }

  &__sub-title {
    font-size: 12px;
    color: #909399;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &__body {
    position: relative;
    width: 100%;
  }

  &__loading {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
  }
}
</style>
