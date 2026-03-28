<script setup lang="ts">
/**
 * DataTable - 数据表格组件
 * 基于 Element Plus Table 封装，支持分页、多选、排序
 */
import { computed } from 'vue'

export interface TableColumn {
  prop: string
  label: string
  width?: string
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  formatter?: (row: any, column: any, cellValue: any) => any
}

export interface Pagination {
  current: number
  pageSize: number
  total: number
}

interface Props {
  columns: TableColumn[]
  data: any[]
  loading?: boolean
  pagination?: Pagination
  selectable?: boolean
  rowKey?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  selectable: false,
  rowKey: 'id'
})

const emit = defineEmits<{
  (e: 'selection-change', selection: any[]): void
  (e: 'page-change', page: number): void
}>()

// 计算分页配置
const paginationConfig = computed(() => {
  if (!props.pagination) return null
  return {
    currentPage: props.pagination.current,
    pageSize: props.pagination.pageSize,
    total: props.pagination.total,
    layout: 'total, prev, pager, next',
    background: true
  }
})

// 处理分页变化
const handlePageChange = (page: number) => {
  emit('page-change', page)
}

// 处理选择变化
const handleSelectionChange = (selection: any[]) => {
  emit('selection-change', selection)
}

// 获取单元格内容
const getCellValue = (row: any, column: TableColumn) => {
  if (column.formatter) {
    return column.formatter(row, column, row[column.prop])
  }
  return row[column.prop]
}
</script>

<template>
  <div class="data-table">
    <el-table
      :data="data"
      :loading="loading"
      :row-key="rowKey"
      @selection-change="handleSelectionChange"
      stripe
      border
      class="data-table__table"
    >
      <!-- 多选列 -->
      <el-table-column
        v-if="selectable"
        type="selection"
        width="55"
        align="center"
      />

      <!-- 数据列 -->
      <el-table-column
        v-for="column in columns"
        :key="column.prop"
        :prop="column.prop"
        :label="column.label"
        :width="column.width"
        :align="column.align || 'left'"
        :sortable="column.sortable ? 'custom' : false"
      >
        <template #default="{ row }">
          <slot :name="`column-${column.prop}`" :row="row" :value="getCellValue(row, column)">
            {{ getCellValue(row, column) }}
          </slot>
        </template>
      </el-table-column>

      <!-- 默认插槽用于自定义列 -->
      <slot />
    </el-table>

    <!-- 分页 -->
    <div v-if="paginationConfig" class="data-table__pagination">
      <el-pagination
        v-model:current-page="paginationConfig.currentPage"
        v-model:page-size="paginationConfig.pageSize"
        :total="paginationConfig.total"
        :layout="paginationConfig.layout"
        :background="paginationConfig.background"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.data-table {
  background: #fff;
  border-radius: 8px;
  padding: 16px;

  &__table {
    width: 100%;
  }

  &__pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
  }
}
</style>
