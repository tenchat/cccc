<script setup lang="ts">
interface Props {
  title: string
  breadcrumb?: string[]
}

withDefaults(defineProps<Props>(), {
  breadcrumb: () => []
})
</script>

<template>
  <div class="page-header">
    <div class="header-content">
      <div class="header-left">
        <h1 class="page-title">{{ title }}</h1>
        <el-breadcrumb v-if="breadcrumb.length > 0" separator="/">
          <el-breadcrumb-item
            v-for="(item, index) in breadcrumb"
            :key="index"
            :to="{ path: index < breadcrumb.length - 1 ? item : undefined }"
          >
            {{ item }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div class="header-right">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

:deep(.el-breadcrumb) {
  font-size: 14px;
}

:deep(.el-breadcrumb__item) {
  color: #64748b;
}

:deep(.el-breadcrumb__inner) {
  color: #64748b;
}

:deep(.el-breadcrumb__inner.is-link:hover) {
  color: #667eea;
}

:deep(.el-breadcrumb__separator) {
  color: #cbd5e1;
}
</style>
