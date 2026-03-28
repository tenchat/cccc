<script setup lang="ts">
/**
 * PageHeader - 页面头部组件
 * 提供页面标题和面包屑导航
 */
interface Props {
  title: string
  breadcrumb?: string[]
}

defineProps<Props>()
</script>

<template>
  <div class="page-header">
    <div class="page-header__main">
      <h1 class="page-header__title">{{ title }}</h1>
      <el-breadcrumb v-if="breadcrumb && breadcrumb.length > 0" separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item
          v-for="(item, index) in breadcrumb"
          :key="index"
          :to="index < breadcrumb.length - 1 ? { path: '/' } : undefined"
        >
          {{ item }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="page-header__actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);

  &__main {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__title {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;

    &__actions {
      width: 100%;
      justify-content: flex-start;
    }
  }
}
</style>
