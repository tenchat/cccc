<script setup lang="ts">
/**
 * StatCard - 统计卡片组件
 * 用于展示关键数据指标，带有趋势指示
 */
interface Props {
  title: string
  value: string | number
  icon?: string
  suffix?: string
  trend?: 'up' | 'down' | 'none'
  trendValue?: string
  color?: string
}

withDefaults(defineProps<Props>(), {
  icon: 'chart',
  trend: 'none',
  color: '#409EFF'
})
</script>

<template>
  <div class="stat-card">
    <div class="stat-card__header">
      <span class="stat-card__title">{{ title }}</span>
      <div v-if="icon" class="stat-card__icon" :style="{ backgroundColor: color + '15' }">
        <el-icon :size="20" :style="{ color }">
          <component :is="icon" />
        </el-icon>
      </div>
    </div>
    <div class="stat-card__body">
      <span class="stat-card__value">{{ value }}</span>
      <span v-if="suffix" class="stat-card__suffix">{{ suffix }}</span>
    </div>
    <div v-if="trend !== 'none'" class="stat-card__trend" :class="`stat-card__trend--${trend}`">
      <el-icon v-if="trend === 'up'" :size="14"><ArrowUp /></el-icon>
      <el-icon v-else-if="trend === 'down'" :size="14"><ArrowDown /></el-icon>
      <span v-if="trendValue">{{ trendValue }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  &__title {
    font-size: 14px;
    color: #606266;
    font-weight: 500;
  }

  &__icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__body {
    display: flex;
    align-items: baseline;
    gap: 4px;
  }

  &__value {
    font-size: 28px;
    font-weight: 700;
    color: #303133;
  }

  &__suffix {
    font-size: 14px;
    color: #909399;
  }

  &__trend {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 8px;
    font-size: 12px;
    font-weight: 500;

    &--up {
      color: #67c23a;
    }

    &--down {
      color: #f56c6c;
    }
  }
}
</style>
