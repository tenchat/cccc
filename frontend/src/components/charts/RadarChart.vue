<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'
import * as echarts from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import {
  RadarComponent
} from 'echarts/components'

// Register necessary ECharts components
echarts.use([RadarChart, RadarComponent, CanvasRenderer])

interface Indicator {
  name: string
  max: number
}

interface Props {
  indicator?: Indicator[]
  value?: number[]
  title?: string
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  indicator: () => [],
  value: () => [],
  title: '竞争力评分',
  theme: 'light'
})

const chartRef = ref<HTMLElement | null>(null)
const { resize } = useChart(chartRef)

const isEmpty = computed(() => {
  return !props.indicator || props.indicator.length === 0 || !props.value || props.value.length === 0
})

const lightTheme = {
  backgroundColor: 'transparent',
  title: {
    text: props.title,
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    data: [props.title],
    bottom: 10,
    textStyle: { color: '#606266' }
  },
  radar: {
    indicator: [],
    center: ['50%', '55%'],
    radius: '65%',
    name: {
      textStyle: { color: '#606266' }
    },
    splitLine: {
      lineStyle: { color: '#d9d9d9' }
    },
    splitArea: {
      areaStyle: { color: ['#fff', '#f7f7f7'] }
    },
    axisLine: {
      lineStyle: { color: '#d9d9d9' }
    }
  }
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: props.title,
    left: 'center',
    textStyle: { color: '#ffffff' }
  },
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(26, 31, 60, 0.9)',
    borderColor: '#00f0ff',
    textStyle: { color: '#ffffff' }
  },
  legend: {
    data: [props.title],
    bottom: 10,
    textStyle: { color: 'rgba(255,255,255,0.7)' }
  },
  radar: {
    indicator: [],
    center: ['50%', '55%'],
    radius: '65%',
    name: {
      textStyle: { color: 'rgba(255,255,255,0.7)' }
    },
    splitLine: {
      lineStyle: { color: 'rgba(0, 240, 255, 0.3)' }
    },
    splitArea: {
      areaStyle: { color: ['rgba(26, 31, 60, 0.8)', 'rgba(26, 31, 60, 0.5)'] }
    },
    axisLine: {
      lineStyle: { color: '#00f0ff' }
    }
  }
}

const chartOptions = computed(() => {
  const themeConfig = props.theme === 'dark' ? darkTheme : lightTheme

  return {
    ...themeConfig,
    title: {
      ...themeConfig.title,
      text: props.title
    },
    legend: {
      ...themeConfig.legend,
      data: [props.title]
    },
    radar: {
      ...themeConfig.radar,
      indicator: props.indicator
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: props.value,
            name: props.title,
            lineStyle: {
              width: 2,
              color: props.theme === 'dark' ? '#00ffcc' : '#409EFF'
            },
            areaStyle: {
              color: props.theme === 'dark'
                ? 'rgba(0, 255, 204, 0.3)'
                : 'rgba(64, 158, 255, 0.3)'
            },
            itemStyle: {
              color: props.theme === 'dark' ? '#00ffcc' : '#409EFF'
            }
          }
        ]
      }
    ]
  }
})

watch(() => props.theme, () => {
  resize()
})
</script>

<template>
  <div ref="chartRef" class="radar-chart">
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
.radar-chart {
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
