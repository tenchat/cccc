<script setup lang="ts">
/**
 * ConfirmDialog - 确认对话框组件
 * 用于需要用户确认的操作
 */
import { computed } from 'vue'

interface Props {
  visible: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  type?: 'default' | 'danger' | 'warning'
}

const props = withDefaults(defineProps<Props>(), {
  title: '确认操作',
  message: '确定要执行此操作吗？',
  confirmText: '确定',
  cancelText: '取消',
  type: 'default'
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const confirmButtonType = computed(() => {
  switch (props.type) {
    case 'danger':
      return 'danger'
    case 'warning':
      return 'warning'
    default:
      return 'primary'
  }
})

const handleConfirm = () => {
  emit('confirm')
  emit('update:visible', false)
}

const handleCancel = () => {
  emit('cancel')
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="420px"
    :close-on-click-modal="false"
    class="confirm-dialog"
    @closed="handleCancel"
  >
    <div class="confirm-dialog__content">
      <div v-if="type !== 'default'" class="confirm-dialog__icon">
        <el-icon :size="48" :color="type === 'danger' ? '#f56c6c' : '#e6a23c'">
          <component :is="type === 'danger' ? 'WarnTriangleFilled' : 'WarningFilled'" />
        </el-icon>
      </div>
      <p class="confirm-dialog__message">{{ message }}</p>
    </div>
    <template #footer>
      <span class="confirm-dialog__footer">
        <el-button @click="handleCancel">{{ cancelText }}</el-button>
        <el-button :type="confirmButtonType" @click="handleConfirm">
          {{ confirmText }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.confirm-dialog {
  &__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0;
    text-align: center;
  }

  &__icon {
    margin-bottom: 16px;
  }

  &__message {
    font-size: 14px;
    color: #606266;
    line-height: 1.6;
    margin: 0;
  }

  &__footer {
    display: flex;
    justify-content: center;
    gap: 12px;
  }
}
</style>
