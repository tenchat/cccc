<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import VChart from 'vue-echarts'
import { useChart } from '@/composables/useChart'
import * as echarts from 'echarts/core'
import { MapChart } from 'echarts/charts'
import { GeoComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

// Register necessary ECharts components
echarts.use([MapChart, GeoComponent, CanvasRenderer])

interface ProvinceData {
  name: string
  value: number
}

interface Props {
  data?: ProvinceData[]
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  theme: 'light'
})

const chartRef = ref<HTMLElement | null>(null)
const { resize } = useChart(chartRef)
const mapLoaded = ref(false)

// Province name mapping for matching
const provinceMap: Record<string, string> = {
  '北京': 'Beijing',
  '天津': 'Tianjin',
  '河北': 'Hebei',
  '山西': 'Shanxi',
  '内蒙古': 'Inner Mongolia',
  '辽宁': 'Liaoning',
  '吉林': 'Jilin',
  '黑龙江': 'Heilongjiang',
  '上海': 'Shanghai',
  '江苏': 'Jiangsu',
  '浙江': 'Zhejiang',
  '安徽': 'Anhui',
  '福建': 'Fujian',
  '江西': 'Jiangxi',
  '山东': 'Shandong',
  '河南': 'Henan',
  '湖北': 'Hubei',
  '湖南': 'Hunan',
  '广东': 'Guangdong',
  '广西': 'Guangxi',
  '海南': 'Hainan',
  '重庆': 'Chongqing',
  '四川': 'Sichuan',
  '贵州': 'Guizhou',
  '云南': 'Yunnan',
  '西藏': 'Tibet',
  '陕西': 'Shaanxi',
  '甘肃': 'Gansu',
  '青海': 'Qinghai',
  '宁夏': 'Ningxia',
  '新疆': 'Xinjiang',
  '台湾': 'Taiwan',
  '香港': 'Hong Kong',
  '澳门': 'Macau'
}

const isEmpty = computed(() => {
  return !props.data || props.data.length === 0
})

const lightTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '全国就业分布',
    left: 'center',
    textStyle: { color: '#303133' }
  },
  tooltip: {
    trigger: 'item',
    formatter: (params: any) => {
      return `${params.name}: ${params.value || 0}`
    }
  },
  visualMap: {
    min: 0,
    max: 100,
    left: 'left',
    top: 'bottom',
    text: ['高', '低'],
    textStyle: { color: '#606266' },
    calculable: true,
    inRange: {
      color: ['#50a3ba', '#eac736', '#d94e5d']
    }
  },
  geo: {
    map: 'china',
    roam: true,
    label: {
      show: false
    },
    itemStyle: {
      areaColor: '#eee',
      borderColor: '#666'
    },
    emphasis: {
      label: {
        show: true,
        color: '#fff'
      },
      itemStyle: {
        areaColor: '#409EFF'
      }
    }
  },
  series: []
}

const darkTheme = {
  backgroundColor: 'transparent',
  title: {
    text: '全国就业分布',
    left: 'center',
    textStyle: { color: '#ffffff' }
  },
  tooltip: {
    trigger: 'item',
    formatter: (params: any) => {
      return `${params.name}: ${params.value || 0}`
    },
    backgroundColor: 'rgba(26, 31, 60, 0.9)',
    borderColor: '#00f0ff',
    textStyle: { color: '#ffffff' }
  },
  visualMap: {
    min: 0,
    max: 100,
    left: 'left',
    top: 'bottom',
    text: ['高', '低'],
    textStyle: { color: 'rgba(255,255,255,0.7)' },
    calculable: true,
    inRange: {
      color: ['#1a3f6f', '#409EFF', '#00ffcc']
    }
  },
  geo: {
    map: 'china',
    roam: true,
    label: {
      show: false
    },
    itemStyle: {
      areaColor: '#1a1f3c',
      borderColor: '#00f0ff'
    },
    emphasis: {
      label: {
        show: true,
        color: '#fff'
      },
      itemStyle: {
        areaColor: '#00f0ff'
      }
    }
  },
  series: []
}

const chartOptions = computed(() => {
  const themeConfig = props.theme === 'dark' ? darkTheme : lightTheme

  const mapData = props.data.map(item => ({
    name: provinceMap[item.name] || item.name,
    value: item.value
  }))

  return {
    ...themeConfig,
    series: [
      {
        type: 'map',
        map: 'china',
        geoIndex: 0,
        data: mapData
      }
    ]
  }
})

const initMap = async () => {
  try {
    // Fetch China geo JSON from public CDN
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const geoJSON = await response.json()

    echarts.registerMap('china', geoJSON)
    mapLoaded.value = true
  } catch (error) {
    console.error('Failed to load China map:', error)
  }
}

onMounted(() => {
  initMap()
})

watch(() => props.theme, () => {
  resize()
})
</script>

<template>
  <div ref="chartRef" class="china-heatmap">
    <div v-if="isEmpty" class="empty-tip">
      暂无数据
    </div>
    <v-chart
      v-else-if="mapLoaded"
      :option="chartOptions"
      autoresize
      @resize="resize"
    />
    <div v-else class="loading-tip">
      地图加载中...
    </div>
  </div>
</template>

<style scoped>
.china-heatmap {
  width: 100%;
  height: 100%;
  min-height: 400px;
  position: relative;
}

.empty-tip,
.loading-tip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #909399;
  font-size: 14px;
}
</style>
