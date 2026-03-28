<script setup lang="ts">
/**
 * EmptyState - 空状态组件
 * 用于展示空数据时的友好提示
 */
interface Props {
  icon?: string
  title: string
  description?: string
  actionText?: string
}

withDefaults(defineProps<Props>(), {
  icon: 'empty'
})

const emit = defineEmits<{
  (e: 'action'): void
}>()

const handleAction = () => {
  emit('action')
}
</script>

<template>
  <div class="empty-state">
    <div class="empty-state__icon">
      <el-icon :size="64" color="#c0c4cc">
        <component :is="icon" />
      </el-icon>
    </div>
    <h3 class="empty-state__title">{{ title }}</h3>
    <p v-if="description" class="empty-state__description">{{ description }}</p>
    <el-button
      v-if="actionText"
      type="primary"
      @click="handleAction"
    >
      {{ actionText }}
    </el-button>
  </div>
</template>

<style scoped lang="scss">
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;

  &__icon {
    margin-bottom: 16px;
  }

  &__title {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
    margin: 0 0 8px;
  }

  &__description {
    font-size: 14px;
    color: #909399;
    margin: 0 0 24px;
    max-width: 300px;
  }
}
</style>
