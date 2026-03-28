<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// Chart options
const lineChartOptions = {
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: { type: 'value' },
  series: [
    {
      name: '访问量',
      type: 'line',
      smooth: true,
      areaStyle: { color: 'rgba(102, 126, 234, 0.3)' },
      lineStyle: { color: '#667eea', width: 2 },
      itemStyle: { color: '#667eea' },
      data: [820, 932, 901, 1234, 1290, 1330, 1520]
    }
  ]
}

const barChartOptions = {
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
  xAxis: { type: 'category', data: ['北京', '上海', '广州', '深圳', '杭州', '成都'] },
  yAxis: { type: 'value' },
  series: [
    {
      name: '用户数',
      type: 'bar',
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#764ba2' },
            { offset: 1, color: '#667eea' }
          ]
        },
        borderRadius: [8, 8, 0, 0]
      },
      data: [1200, 1800, 900, 1500, 800, 1100]
    }
  ]
}

const pieChartOptions = {
  tooltip: { trigger: 'item' },
  legend: { bottom: '5%', left: 'center' },
  series: [
    {
      name: '访问来源',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' }
      },
      data: [
        { value: 1048, name: '搜索引擎', itemStyle: { color: '#667eea' } },
        { value: 735, name: '直接访问', itemStyle: { color: '#764ba2' } },
        { value: 580, name: '邮件营销', itemStyle: { color: '#f093fb' } },
        { value: 484, name: '联盟广告', itemStyle: { color: '#4facfe' } }
      ]
    }
  ]
}

// Stats cards
const stats = [
  { label: '总访问量', value: '128,956', trend: '+12.5%', icon: 'View' },
  { label: '活跃用户', value: '8,846', trend: '+8.2%', icon: 'User' },
  { label: '平均停留', value: '3分42秒', trend: '+2.1%', icon: 'Clock' },
  { label: '转化率', value: '3.28%', trend: '-0.3%', icon: 'TrendCharts' }
]

// Real-time update
const currentTime = ref(new Date().toLocaleTimeString())
let timer: ReturnType<typeof setInterval>

onMounted(() => {
  timer = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<template>
  <div class="dashboard-view">
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">数据看板</h1>
        <p class="page-subtitle">实时业务数据监控</p>
      </div>
      <div class="header-time">
        <el-icon><Clock /></el-icon>
        {{ currentTime }}
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card card">
        <div class="stat-icon">
          <el-icon :size="32"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-label">{{ stat.label }}</span>
          <span class="stat-value">{{ stat.value }}</span>
          <span
            class="stat-trend"
            :class="{ positive: stat.trend.startsWith('+'), negative: stat.trend.startsWith('-') }"
          >
            {{ stat.trend }}
          </span>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <div class="chart-card card">
        <h3 class="chart-title">访问趋势</h3>
        <v-chart class="chart" :option="lineChartOptions" autoresize />
      </div>
      <div class="chart-card card">
        <h3 class="chart-title">用户分布</h3>
        <v-chart class="chart" :option="barChartOptions" autoresize />
      </div>
      <div class="chart-card card">
        <h3 class="chart-title">访问来源</h3>
        <v-chart class="chart" :option="pieChartOptions" autoresize />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #64748b;
  font-size: 16px;
}

.header-time {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 18px;
  background: white;
  padding: 12px 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 16px;
  color: #667eea;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 14px;
  font-weight: 500;
}

.stat-trend.positive {
  color: #22c55e;
}

.stat-trend.negative {
  color: #ef4444;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.chart-card {
  padding: 24px;
}

.chart-title {
  color: #1e293b;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
}

.chart {
  height: 300px;
}

.card {
  background: white;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid > :last-child {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .stats-grid,
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid > :last-child {
    grid-column: span 1;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
