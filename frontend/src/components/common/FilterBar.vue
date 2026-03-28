<script setup lang="ts">
/**
 * FilterBar - 筛选工具栏组件
 * 支持 select、input、dateRange、cascader 四种筛选类型
 */
import { ref, watch } from 'vue'

export interface FilterConfig {
  key: string
  label: string
  type: 'select' | 'input' | 'dateRange' | 'cascader'
  options?: { label: string; value: any }[]
  placeholder?: string
  props?: Record<string, any>
}

interface Props {
  filters: FilterConfig[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'filter-change', values: Record<string, any>): void
}>()

const filterValues = ref<Record<string, any>>({})

// 初始化筛选值
props.filters.forEach((filter) => {
  filterValues.value[filter.key] = filter.type === 'select' ? '' : ''
})

// 监听筛选值变化
watch(
  filterValues,
  (newValues) => {
    emit('filter-change', { ...newValues })
  },
  { deep: true }
)

// 重置筛选
const resetFilters = () => {
  props.filters.forEach((filter) => {
    filterValues.value[filter.key] = filter.type === 'select' ? '' : ''
  })
}

// 触发筛选（用于输入框回车）
const triggerFilter = () => {
  emit('filter-change', { ...filterValues.value })
}

defineExpose({
  resetFilters
})
</script>

<template>
  <div class="filter-bar">
    <div class="filter-bar__items">
      <div
        v-for="filter in filters"
        :key="filter.key"
        class="filter-bar__item"
      >
        <span class="filter-bar__label">{{ filter.label }}</span>

        <!-- Select 筛选 -->
        <el-select
          v-if="filter.type === 'select'"
          v-model="filterValues[filter.key]"
          :placeholder="filter.placeholder || `请选择${filter.label}`"
          clearable
          v-bind="filter.props"
          class="filter-bar__select"
        >
          <el-option
            v-for="option in filter.options"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>

        <!-- Input 筛选 -->
        <el-input
          v-else-if="filter.type === 'input'"
          v-model="filterValues[filter.key]"
          :placeholder="filter.placeholder || `请输入${filter.label}`"
          clearable
          v-bind="filter.props"
          class="filter-bar__input"
          @keyup.enter="triggerFilter"
        />

        <!-- DateRange 筛选 -->
        <el-date-picker
          v-else-if="filter.type === 'dateRange'"
          v-model="filterValues[filter.key]"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          v-bind="filter.props"
          class="filter-bar__date"
        />

        <!-- Cascader 筛选 -->
        <el-cascader
          v-else-if="filter.type === 'cascader'"
          v-model="filterValues[filter.key]"
          :options="filter.options"
          :placeholder="filter.placeholder || `请选择${filter.label}`"
          clearable
          v-bind="filter.props"
          class="filter-bar__cascader"
        />
      </div>
    </div>

    <div class="filter-bar__actions">
      <el-button @click="resetFilters">重置</el-button>
      <el-button type="primary" @click="triggerFilter">筛选</el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.filter-bar {
  background: #fff;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;

  &__items {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    flex: 1;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 180px;
  }

  &__label {
    font-size: 14px;
    color: #606266;
    white-space: nowrap;
  }

  &__select,
  &__input,
  &__date,
  &__cascader {
    flex: 1;
    min-width: 140px;
  }

  &__actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;

    &__items {
      width: 100%;
    }

    &__item {
      width: 100%;
      min-width: unset;
    }

    &__select,
    &__input,
    &__date,
    &__cascader {
      width: 100%;
    }
  }
}
</style>
