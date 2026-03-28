<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'

interface TrendData {
  year: string
  employmentRate: number
  studyRate: number
  abroadRate?: number
}

interface Props {
  data?: TrendData[]
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
    text: '历年就业趋势',
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' },
    formatter: (params: any) => {
      let result = params[0].name + '<br/>'
      params.forEach((item: any) => {
        result += `${item.marker} ${item.seriesName}: ${item.value}%<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['就业率', '升学率', '出国率'],
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
    boundaryGap: false,
    data: [],
    axisLabel: { color: '#606266' },
    axisLine: { lineStyle: { color: '#d9d9d9' } }
  },
  yAxis: {
    type: 'value',
    name: '百分比(%)',
    min: 0,
    max: 100,
    axisLabel: {
      color: '#606266',
      formatter: '{value}%'
    },
    axisLine: { lineStyle: { color: '#d9d9d9' } },
    splitLine: { lineStyle: { color: '#eee' } }
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      start: 0,
      end: 100
    }
  ]
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '历年就业趋势',
    left: 'center',
    textStyle: { color: '#ffffff' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' },
    backgroundColor: 'rgba(26, 31, 60, 0.9)',
    borderColor: '#00f0ff',
    textStyle: { color: '#ffffff' },
    formatter: (params: any) => {
      let result = params[0].name + '<br/>'
      params.forEach((item: any) => {
        result += `${item.marker} ${item.seriesName}: ${item.value}%<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['就业率', '升学率', '出国率'],
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
    boundaryGap: false,
    data: [],
    axisLabel: { color: 'rgba(255,255,255,0.7)' },
    axisLine: { lineStyle: { color: '#00f0ff' } }
  },
  yAxis: {
    type: 'value',
    name: '百分比(%)',
    min: 0,
    max: 100,
    axisLabel: {
      color: 'rgba(255,255,255,0.7)',
      formatter: '{value}%'
    },
    axisLine: { lineStyle: { color: '#00f0ff' } },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      start: 0,
      end: 100,
      backgroundColor: 'rgba(26, 31, 60, 0.9)',
      borderColor: '#00f0ff',
      textStyle: { color: '#00f0ff' }
    }
  ]
}

const chartOptions = computed(() => {
  const themeConfig = props.theme === 'dark' ? darkTheme : lightTheme

  const years = props.data.map(item => item.year)
  const employmentRates = props.data.map(item => item.employmentRate)
  const studyRates = props.data.map(item => item.studyRate)
  const abroadRates = props.data.map(item => item.abroadRate || 0)

  return {
    ...themeConfig,
    xAxis: {
      ...themeConfig.xAxis,
      data: years
    },
    series: [
      {
        name: '就业率',
        type: 'line',
        data: employmentRates,
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#52c41a' },
        areaStyle: props.theme === 'dark' ? {
          color: 'rgba(82, 196, 26, 0.2)'
        } : {
          color: 'rgba(82, 196, 26, 0.1)'
        }
      },
      {
        name: '升学率',
        type: 'line',
        data: studyRates,
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#1890ff' },
        areaStyle: props.theme === 'dark' ? {
          color: 'rgba(24, 144, 255, 0.2)'
        } : {
          color: 'rgba(24, 144, 255, 0.1)'
        }
      },
      {
        name: '出国率',
        type: 'line',
        data: abroadRates,
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#722ed1' },
        areaStyle: props.theme === 'dark' ? {
          color: 'rgba(114, 46, 209, 0.2)'
        } : {
          color: 'rgba(114, 46, 209, 0.1)'
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
  <div ref="chartRef" class="trend-line">
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
.trend-line {
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
