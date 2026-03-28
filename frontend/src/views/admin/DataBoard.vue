<script setup lang="ts">
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, LineChart, MapChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  VisualMapComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  PieChart,
  BarChart,
  LineChart,
  MapChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  VisualMapComponent
])

// Employment Rate Ring Chart
const employmentRateOptions = {
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  series: [
    {
      type: 'pie',
      radius: ['55%', '75%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#0f172a',
        borderWidth: 3
      },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 18, fontWeight: 'bold' }
      },
      data: [
        { value: 98656, name: '已就业', itemStyle: { color: '#22c55e' } },
        { value: 27024, name: '未就业', itemStyle: { color: '#ef4444' } }
      ]
    }
  ]
}

// Industry Salary Bar Chart
const industrySalaryOptions = {
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '3%', containLabel: true },
  xAxis: {
    type: 'value',
    axisLine: { show: false },
    axisTick: { show: false },
    splitLine: { lineStyle: { color: '#1e293b' } },
    axisLabel: { color: '#94a3b8' }
  },
  yAxis: {
    type: 'category',
    data: ['教育培训', '金融', '房地产', '医疗健康', '互联网', '电子技术'],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#e2e8f0' }
  },
  series: [
    {
      type: 'bar',
      data: [8500, 12000, 9500, 11000, 15000, 13500],
      itemStyle: {
        borderRadius: [0, 6, 6, 0],
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 1, y2: 0,
          colorStops: [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#22c55e' }
          ]
        }
      },
      barWidth: 20
    }
  ]
}

// College Comparison Bar Chart
const collegeCompareOptions = {
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  legend: {
    data: ['就业率', '签约率'],
    textStyle: { color: '#e2e8f0' },
    top: 10
  },
  grid: { left: '3%', right: '4%', bottom: '10%', top: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    data: ['计算机学院', '软件学院', '信息工程学院', '机械学院', '经管学院', '外语学院'],
    axisLine: { lineStyle: { color: '#334155' } },
    axisLabel: { color: '#94a3b8', rotate: 15 }
  },
  yAxis: {
    type: 'value',
    max: 100,
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#1e293b' } },
    axisLabel: { color: '#94a3b8' }
  },
  series: [
    {
      name: '就业率',
      type: 'bar',
      data: [88.1, 86.3, 84.8, 81.4, 79.0, 70.7],
      itemStyle: { color: '#667eea', borderRadius: [4, 4, 0, 0] }
    },
    {
      name: '签约率',
      type: 'bar',
      data: [75.2, 72.8, 68.5, 65.3, 58.9, 52.1],
      itemStyle: { color: '#22c55e', borderRadius: [4, 4, 0, 0] }
    }
  ]
}

// Trend Line Chart
const trendOptions = {
  tooltip: { trigger: 'axis' },
  legend: {
    data: ['就业率', '薪资涨幅'],
    textStyle: { color: '#e2e8f0' },
    top: 10
  },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['2020', '2021', '2022', '2023', '2024'],
    axisLine: { lineStyle: { color: '#334155' } },
    axisLabel: { color: '#94a3b8' }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#1e293b' } },
    axisLabel: { color: '#94a3b8' }
  },
  series: [
    {
      name: '就业率',
      type: 'line',
      data: [68.5, 71.2, 73.8, 75.2, 78.5],
      smooth: true,
      lineStyle: { color: '#667eea', width: 3 },
      itemStyle: { color: '#667eea' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(102, 126, 234, 0.4)' },
            { offset: 1, color: 'rgba(102, 126, 234, 0)' }
          ]
        }
      }
    },
    {
      name: '薪资涨幅',
      type: 'line',
      yAxisIndex: 0,
      data: [5.2, 6.8, 7.5, 8.2, 8.5],
      smooth: true,
      lineStyle: { color: '#22c55e', width: 3 },
      itemStyle: { color: '#22c55e' }
    }
  ]
}

// Scrolling News
const newsList = ref([
  '全国高校就业率达到78.5%，创历史新高',
  '人工智能岗位需求同比增长35%',
  '2024届春季大型招聘会成功举办',
  '计算机专业平均薪资突破15000元',
  '全国高校就业率达到78.5%，创历史新高',
  '人工智能岗位需求同比增长35%',
  '2024届春季大型招聘会成功举办',
  '计算机专业平均薪资突破15000元'
])
</script>

<template>
  <div class="databoard-page">
    <div class="dashboard-container">
      <!-- Header -->
      <div class="dashboard-header">
        <h1>全国就业数据大屏</h1>
        <span class="current-date">{{ new Date().toLocaleDateString() }}</span>
      </div>

      <!-- Stats Row -->
      <div class="stats-row">
        <div class="stat-card">
          <span class="stat-label">学校总数</span>
          <span class="stat-value">45</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">学生总数</span>
          <span class="stat-value">125,680</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">总体就业率</span>
          <span class="stat-value green">78.5%</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">平均薪资</span>
          <span class="stat-value orange">12,850</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">入驻企业</span>
          <span class="stat-value purple">1,258</span>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-grid">
        <!-- Employment Rate -->
        <div class="chart-card span-2">
          <h3>全国就业率概览</h3>
          <div class="chart-content">
            <div class="ring-chart">
              <VChart :option="employmentRateOptions" autoresize />
            </div>
            <div class="ring-legend">
              <div class="legend-item">
                <span class="dot green"></span>
                <span>已就业</span>
                <span class="value">98,656人</span>
              </div>
              <div class="legend-item">
                <span class="dot red"></span>
                <span>未就业</span>
                <span class="value">27,024人</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Industry Salary -->
        <div class="chart-card span-2">
          <h3>行业薪资分布</h3>
          <VChart class="bar-chart" :option="industrySalaryOptions" autoresize />
        </div>

        <!-- College Comparison -->
        <div class="chart-card span-3">
          <h3>各学院就业对比</h3>
          <VChart class="compare-chart" :option="collegeCompareOptions" autoresize />
        </div>

        <!-- Trend -->
        <div class="chart-card span-2">
          <h3>历年就业趋势</h3>
          <VChart class="trend-chart" :option="trendOptions" autoresize />
        </div>
      </div>

      <!-- News Ticker -->
      <div class="news-ticker">
        <div class="news-label">
          <el-icon><Bell /></el-icon>
          最新动态
        </div>
        <div class="news-content">
          <div class="news-scroll">
            <span v-for="(news, index) in newsList" :key="index" class="news-item">
              {{ news }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.databoard-page {
  background: #0f172a;
  min-height: 100vh;
  margin: -24px -32px;
  padding: 20px;
}

.dashboard-container {
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  border-radius: 16px;
  margin-bottom: 24px;
}

.dashboard-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #e2e8f0;
  margin: 0;
}

.current-date {
  font-size: 14px;
  color: #94a3b8;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #334155;
}

.stat-label {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.stat-value.green { color: #22c55e; }
.stat-value.purple { color: #667eea; }
.stat-value.orange { color: #f59e0b; }

.charts-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.chart-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #334155;
}

.chart-card.span-2 { grid-column: span 2; }
.chart-card.span-3 { grid-column: span 3; }

.chart-card h3 {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 12px;
}

.chart-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.ring-chart {
  width: 160px;
  height: 160px;
}

.ring-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #e2e8f0;
}

.legend-item .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-item .dot.green { background: #22c55e; }
.legend-item .dot.red { background: #ef4444; }

.legend-item .value {
  margin-left: auto;
  font-weight: 600;
  color: #94a3b8;
}

.bar-chart,
.compare-chart,
.trend-chart {
  height: 220px;
}

.news-ticker {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 16px;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #334155;
}

.news-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: 600;
  font-size: 13px;
  white-space: nowrap;
}

.news-content {
  flex: 1;
  overflow: hidden;
  mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}

.news-scroll {
  display: flex;
  gap: 60px;
  animation: scroll 25s linear infinite;
}

@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.news-item {
  font-size: 13px;
  color: #94a3b8;
  white-space: nowrap;
}

@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-card.span-2,
  .chart-card.span-3 {
    grid-column: span 1;
  }
}
</style>
