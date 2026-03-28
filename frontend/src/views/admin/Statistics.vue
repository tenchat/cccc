<script setup lang="ts">
import { ref, reactive } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, LineChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const timeRange = ref('month')

const summaryData = reactive({
  totalStudents: 125680,
  employedStudents: 98656,
  employmentRate: 78.5,
  avgSalary: 12850,
  schoolCount: 45,
  companyCount: 1258
})

const pieOptions = {
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', right: '5%', top: 'center' },
  series: [
    {
      type: 'pie',
      center: ['40%', '50%'],
      radius: ['45%', '70%'],
      itemStyle: { borderRadius: 8 },
      label: { show: false },
      data: [
        { value: 98656, name: '已就业', itemStyle: { color: '#22c55e' } },
        { value: 14832, name: '求职中', itemStyle: { color: '#f59e0b' } },
        { value: 12192, name: '未签约', itemStyle: { color: '#ef4444' } }
      ]
    }
  ]
}

const trendOptions = {
  tooltip: { trigger: 'axis' },
  legend: { data: ['就业率', '签约率'], top: 10 },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisLabel: { color: '#64748b' }
  },
  yAxis: {
    type: 'value',
    max: 100,
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    splitLine: { lineStyle: { color: '#f1f5f9' } },
    axisLabel: { color: '#64748b' }
  },
  series: [
    {
      name: '就业率',
      type: 'line',
      data: [45, 48, 52, 58, 63, 68, 72, 75, 76, 77, 78, 78.5],
      smooth: true,
      lineStyle: { color: '#667eea', width: 3 },
      itemStyle: { color: '#667eea' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
            { offset: 1, color: 'rgba(102, 126, 234, 0)' }
          ]
        }
      }
    },
    {
      name: '签约率',
      type: 'line',
      data: [30, 35, 40, 45, 52, 58, 62, 65, 67, 69, 70, 72],
      smooth: true,
      lineStyle: { color: '#22c55e', width: 3 },
      itemStyle: { color: '#22c55e' }
    }
  ]
}

const majorSalaryOptions = {
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '3%', containLabel: true },
  xAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisLabel: { color: '#64748b' }
  },
  yAxis: {
    type: 'category',
    data: ['哲学', '历史学', '法学', '教育学', '文学', '经济学', '管理学', '理学', '工学'],
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    axisLabel: { color: '#64748b' }
  },
  series: [
    {
      type: 'bar',
      data: [6500, 6800, 7500, 8000, 7800, 9500, 9200, 11000, 13500],
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

const cityDistributionOptions = {
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', right: '5%', top: 'center' },
  series: [
    {
      type: 'pie',
      center: ['40%', '50%'],
      radius: ['45%', '70%'],
      itemStyle: { borderRadius: 8 },
      label: { show: false },
      data: [
        { value: 35, name: '一线城市', itemStyle: { color: '#667eea' } },
        { value: 30, name: '新一线城市', itemStyle: { color: '#22c55e' } },
        { value: 20, name: '二线城市', itemStyle: { color: '#f59e0b' } },
        { value: 15, name: '其他', itemStyle: { color: '#94a3b8' } }
      ]
    }
  ]
}
</script>

<template>
  <div class="statistics-page">
    <div class="page-header">
      <div class="header-left">
        <h2>统计分析</h2>
        <p class="page-desc">全面分析就业数据，了解人才市场趋势</p>
      </div>
      <div class="header-right">
        <el-radio-group v-model="timeRange">
          <el-radio-button value="week">本周</el-radio-button>
          <el-radio-button value="month">本月</el-radio-button>
          <el-radio-button value="year">本年</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-grid">
      <div class="summary-card">
        <span class="summary-value">{{ summaryData.totalStudents.toLocaleString() }}</span>
        <span class="summary-label">学生总数</span>
      </div>
      <div class="summary-card">
        <span class="summary-value green">{{ summaryData.employedStudents.toLocaleString() }}</span>
        <span class="summary-label">已就业人数</span>
      </div>
      <div class="summary-card">
        <span class="summary-value purple">{{ summaryData.employmentRate }}%</span>
        <span class="summary-label">就业率</span>
      </div>
      <div class="summary-card">
        <span class="summary-value orange">{{ summaryData.avgSalary.toLocaleString() }}</span>
        <span class="summary-label">平均薪资</span>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="charts-row">
      <div class="chart-card span-2">
        <h3>就业状态分布</h3>
        <VChart class="pie-chart" :option="pieOptions" autoresize />
      </div>
      <div class="chart-card span-3">
        <h3>就业率趋势</h3>
        <VChart class="trend-chart" :option="trendOptions" autoresize />
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="charts-row">
      <div class="chart-card span-3">
        <h3>各专业平均薪资</h3>
        <VChart class="salary-chart" :option="majorSalaryOptions" autoresize />
      </div>
      <div class="chart-card span-2">
        <h3>就业城市分布</h3>
        <VChart class="city-chart" :option="cityDistributionOptions" autoresize />
      </div>
    </div>
  </div>
</template>

<style scoped>
.statistics-page {
  max-width: 1400px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-left h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-desc {
  color: #64748b;
  font-size: 14px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.summary-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.summary-value.green { color: #22c55e; }
.summary-value.purple { color: #667eea; }
.summary-value.orange { color: #f59e0b; }

.summary-label {
  font-size: 13px;
  color: #64748b;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.chart-card.span-2 { grid-column: span 2; }
.chart-card.span-3 { grid-column: span 3; }

h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px;
}

.pie-chart,
.trend-chart,
.salary-chart,
.city-chart {
  height: 280px;
}

@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .chart-card.span-2,
  .chart-card.span-3 {
    grid-column: span 1;
  }
}
</style>
