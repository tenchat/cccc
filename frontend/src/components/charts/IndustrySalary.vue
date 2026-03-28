<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'

interface IndustryData {
  industry: string
  avgSalary: number
}

interface Props {
  data?: IndustryData[]
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  theme: 'light'
})

const chartRef = ref<HTMLElement | null>(null)
const { resize } = useChart(chartRef)

const isEmpty = computed(() => {
  return !props.data || props.data.length === 0
})

// Sort data by salary descending
const sortedData = computed(() => {
  return [...props.data].sort((a, b) => b.avgSalary - a.avgSalary)
})

// Get color based on salary rank
const getSalaryColor = (index: number, total: number, isDark: boolean) => {
  const ratio = index / total
  if (isDark) {
    // Dark theme: cyan gradient
    if (ratio < 0.25) return '#00ffcc'
    if (ratio < 0.5) return '#00f0ff'
    if (ratio < 0.75) return '#409EFF'
    return '#667799'
  } else {
    // Light theme: blue gradient
    if (ratio < 0.25) return '#409EFF'
    if (ratio < 0.5) return '#67C23A'
    if (ratio < 0.75) return '#E6A23C'
    return '#F56C6C'
  }
}

const lightTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '行业薪资排行',
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    formatter: (params: any) => {
      const item = params[0]
      return `${item.name}<br/>平均薪资: ${item.value.toLocaleString()}元/月`
    }
  },
  grid: {
    left: '3%',
    right: '10%',
    bottom: '3%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '薪资(元/月)',
    axisLabel: {
      color: '#606266',
      formatter: (value: number) => `${(value / 1000).toFixed(0)}k`
    },
    axisLine: { lineStyle: { color: '#d9d9d9' } },
    splitLine: { lineStyle: { color: '#eee' } }
  },
  yAxis: {
    type: 'category',
    data: [],
    inverse: true,
    axisLabel: { color: '#606266' },
    axisLine: { lineStyle: { color: '#d9d9d9' } }
  }
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '行业薪资排行',
    left: 'center',
    textStyle: { color: '#ffffff' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    backgroundColor: 'rgba(26, 31, 60, 0.9)',
    borderColor: '#00f0ff',
    textStyle: { color: '#ffffff' },
    formatter: (params: any) => {
      const item = params[0]
      return `${item.name}<br/>平均薪资: ${item.value.toLocaleString()}元/月`
    }
  },
  grid: {
    left: '3%',
    right: '10%',
    bottom: '3%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '薪资(元/月)',
    axisLabel: {
      color: 'rgba(255,255,255,0.7)',
      formatter: (value: number) => `${(value / 1000).toFixed(0)}k`
    },
    axisLine: { lineStyle: { color: '#00f0ff' } },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
  },
  yAxis: {
    type: 'category',
    data: [],
    inverse: true,
    axisLabel: { color: 'rgba(255,255,255,0.7)' },
    axisLine: { lineStyle: { color: '#00f0ff' } }
  }
}

const chartOptions = computed(() => {
  const isDark = props.theme === 'dark'
  const themeConfig = isDark ? darkTheme : lightTheme

  const industries = sortedData.value.map(item => item.industry)
  const salaries = sortedData.value.map(item => item.avgSalary)
  const total = industries.length

  const barColors = salaries.map((_, index) => getSalaryColor(index, total, isDark))

  return {
    ...themeConfig,
    yAxis: {
      ...themeConfig.yAxis,
      data: industries
    },
    series: [
      {
        type: 'bar',
        data: salaries,
        barWidth: '60%',
        itemStyle: {
          color: (params: any) => barColors[params.dataIndex]
        },
        label: {
          show: true,
          position: 'right',
          formatter: (params: any) => `${params.value.toLocaleString()}`,
          color: isDark ? '#ffffff' : '#606266'
        }
      }
    ]
  }
})

watch(() => props.theme, () => {
  resize()
})
</script>

<template>
  <div ref="chartRef" class="industry-salary">
    <div v-if="isEmpty" class="empty-tip">
      暂无数据
    </div>
    <v-chart
      v-else
      :option="chartOptions"
      autoresize
      @resize="resize"
    />
  </div>
</template>

<style scoped>
.industry-salary {
  width: 100%;
  height: 100%;
  min-height: 350px;
  position: relative;
}

.empty-tip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #909399;
  font-size: 14px;
}
</style>
