<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'

interface CollegeData {
  college: string
  total: number
  employed: number
  rate: number
}

interface Props {
  data?: CollegeData[]
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

const lightTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '学院就业对比',
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    formatter: (params: any) => {
      const college = params[0].name
      const employed = params[0].value
      const unemployed = params[1].value
      const rate = props.data.find(d => d.college === college)?.rate || 0
      return `${college}<br/>已就业: ${employed}<br/>待就业: ${unemployed}<br/>就业率: ${rate}%`
    }
  },
  legend: {
    data: ['已就业', '待就业'],
    bottom: 10,
    textStyle: { color: '#606266' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '15%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: [],
    axisLabel: {
      color: '#606266',
      rotate: 45
    },
    axisLine: { lineStyle: { color: '#d9d9d9' } }
  },
  yAxis: {
    type: 'value',
    name: '人数',
    axisLabel: { color: '#606266' },
    axisLine: { lineStyle: { color: '#d9d9d9' } },
    splitLine: { lineStyle: { color: '#eee' } }
  }
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '学院就业对比',
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
      const college = params[0].name
      const employed = params[0].value
      const unemployed = params[1].value
      const rate = props.data.find(d => d.college === college)?.rate || 0
      return `${college}<br/>已就业: ${employed}<br/>待就业: ${unemployed}<br/>就业率: ${rate}%`
    }
  },
  legend: {
    data: ['已就业', '待就业'],
    bottom: 10,
    textStyle: { color: 'rgba(255,255,255,0.7)' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '15%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: [],
    axisLabel: {
      color: 'rgba(255,255,255,0.7)',
      rotate: 45
    },
    axisLine: { lineStyle: { color: '#00f0ff' } }
  },
  yAxis: {
    type: 'value',
    name: '人数',
    axisLabel: { color: 'rgba(255,255,255,0.7)' },
    axisLine: { lineStyle: { color: '#00f0ff' } },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
  }
}

const chartOptions = computed(() => {
  const themeConfig = props.theme === 'dark' ? darkTheme : lightTheme

  const colleges = props.data.map(item => item.college)
  const employedData = props.data.map(item => item.employed)
  const unemployedData = props.data.map(item => item.total - item.employed)

  return {
    ...themeConfig,
    xAxis: {
      ...themeConfig.xAxis,
      data: colleges
    },
    series: [
      {
        name: '已就业',
        type: 'bar',
        stack: 'total',
        data: employedData,
        itemStyle: { color: '#52c41a' },
        barWidth: '50%'
      },
      {
        name: '待就业',
        type: 'bar',
        stack: 'total',
        data: unemployedData,
        itemStyle: { color: '#ff4d4f' },
        barWidth: '50%'
      }
    ]
  }
})

watch(() => props.theme, () => {
  resize()
})
</script>

<template>
  <div ref="chartRef" class="college-bar">
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
.college-bar {
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
