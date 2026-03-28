<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'

interface Props {
  employed?: number
  unemployed?: number
  furtherStudy?: number
  abroad?: number
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  employed: 0,
  unemployed: 0,
  furtherStudy: 0,
  abroad: 0,
  theme: 'light'
})

const chartRef = ref<HTMLElement | null>(null)
const { resize } = useChart(chartRef)

const isEmpty = computed(() => {
  return props.employed === 0 && props.unemployed === 0 && props.furtherStudy === 0 && props.abroad === 0
})

const lightTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '就业率分布',
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'horizontal',
    bottom: 10,
    textStyle: { color: '#606266' }
  },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '45%'],
      data: [
        { value: 0, name: '已就业', itemStyle: { color: '#52c41a' } },
        { value: 0, name: '待就业', itemStyle: { color: '#ff4d4f' } },
        { value: 0, name: '升学', itemStyle: { color: '#1890ff' } },
        { value: 0, name: '出国', itemStyle: { color: '#722ed1' } }
      ],
      label: {
        formatter: '{b}: {c} ({d}%)',
        color: '#606266'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '就业率分布',
    left: 'center',
    textStyle: { color: '#ffffff' }
  },
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)',
    backgroundColor: 'rgba(26, 31, 60, 0.9)',
    borderColor: '#00f0ff',
    textStyle: { color: '#ffffff' }
  },
  legend: {
    orient: 'horizontal',
    bottom: 10,
    textStyle: { color: 'rgba(255,255,255,0.7)' }
  },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '45%'],
      data: [
        { value: 0, name: '已就业', itemStyle: { color: '#52c41a' } },
        { value: 0, name: '待就业', itemStyle: { color: '#ff4d4f' } },
        { value: 0, name: '升学', itemStyle: { color: '#1890ff' } },
        { value: 0, name: '出国', itemStyle: { color: '#722ed1' } }
      ],
      label: {
        formatter: '{b}: {c} ({d}%)',
        color: 'rgba(255,255,255,0.7)'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}

const chartOptions = computed(() => {
  const themeConfig = props.theme === 'dark' ? darkTheme : lightTheme
  const seriesData = [
    { value: props.employed, name: '已就业', itemStyle: { color: '#52c41a' } },
    { value: props.unemployed, name: '待就业', itemStyle: { color: '#ff4d4f' } },
    { value: props.furtherStudy, name: '升学', itemStyle: { color: '#1890ff' } },
    { value: props.abroad, name: '出国', itemStyle: { color: '#722ed1' } }
  ]

  return {
    ...themeConfig,
    series: [{ ...themeConfig.series[0], data: seriesData }]
  }
})

watch(() => props.theme, () => {
  resize()
})
</script>

<template>
  <div ref="chartRef" class="employment-pie">
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
.employment-pie {
  width: 100%;
  height: 100%;
  min-height: 300px;
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
