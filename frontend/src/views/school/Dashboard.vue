<script setup lang="ts">
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const statsData = ref({
  totalStudents: 2847,
  employedStudents: 2156,
  employmentRate: 75.7,
  avgSalary: 12500,
  rateChange: 2.3,
  salaryChange: 8.5
})

const collegeRanking = ref([
  { rank: 1, name: '计算机学院', total: 520, employed: 458, rate: 88.1 },
  { rank: 2, name: '软件学院', total: 380, employed: 328, rate: 86.3 },
  { rank: 3, name: '信息工程学院', total: 420, employed: 356, rate: 84.8 },
  { rank: 4, name: '机械工程学院', total: 350, employed: 285, rate: 81.4 },
  { rank: 5, name: '经济管理学院', total: 580, employed: 458, rate: 79.0 },
  { rank: 6, name: '外语学院', total: 280, employed: 198, rate: 70.7 }
])

const warningStudents = ref([
  { id: 1, name: '李四', college: '计算机学院', status: '未签约', gpa: 2.1 },
  { id: 2, name: '王五', college: '机械工程学院', status: '求职中', gpa: 2.3 },
  { id: 3, name: '赵六', college: '外语学院', status: '未签约', gpa: 2.0 }
])

const trendOptions = {
  tooltip: { trigger: 'axis' },
  legend: { data: ['就业率', '签约率'], top: 10 },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    data: ['3月', '4月', '5月', '6月', '7月', '8月', '9月'],
    axisLine: { lineStyle: { color: '#e2e8f0' } }
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#e2e8f0' } },
    splitLine: { lineStyle: { color: '#f1f5f9' } }
  },
  series: [
    {
      name: '就业率',
      type: 'line',
      data: [45, 52, 58, 65, 70, 73, 75.7],
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
      data: [30, 38, 45, 52, 58, 62, 68],
      smooth: true,
      lineStyle: { color: '#22c55e', width: 3 },
      itemStyle: { color: '#22c55e' }
    }
  ]
}
</script>

<template>
  <div class="school-dashboard">
    <!-- Stats Cards -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(102, 126, 234, 0.1);">
          <el-icon :size="28" color="#667eea"><User /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.totalStudents }}</span>
          <span class="stat-label">毕业生总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(34, 197, 94, 0.1);">
          <el-icon :size="28" color="#22c55e"><CircleCheck /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.employedStudents }}</span>
          <span class="stat-label">已就业人数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1);">
          <el-icon :size="28" color="#f59e0b"><TrendCharts /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.employmentRate }}%</span>
          <span class="stat-label">就业率</span>
          <span class="stat-change positive">+{{ statsData.rateChange }}%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(14, 165, 233, 0.1);">
          <el-icon :size="28" color="#0ea5e9"><Money /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.avgSalary.toLocaleString() }}</span>
          <span class="stat-label">平均薪资</span>
          <span class="stat-change positive">+{{ statsData.salaryChange }}%</span>
        </div>
      </div>
    </div>

    <!-- Charts and Tables -->
    <div class="content-grid">
      <!-- Employment Trend -->
      <div class="chart-card">
        <div class="card-header">
          <h3>就业趋势</h3>
        </div>
        <VChart class="trend-chart" :option="trendOptions" autoresize />
      </div>

      <!-- College Ranking -->
      <div class="ranking-card">
        <div class="card-header">
          <h3>学院就业率排名</h3>
        </div>
        <el-table :data="collegeRanking" size="small">
          <el-table-column prop="rank" label="排名" width="60" align="center" />
          <el-table-column prop="name" label="学院" />
          <el-table-column prop="total" label="总人数" align="center" />
          <el-table-column prop="employed" label="已就业" align="center" />
          <el-table-column prop="rate" label="就业率" align="center">
            <template #default="{ row }">
              <span :class="row.rate >= 85 ? 'rate-high' : row.rate >= 75 ? 'rate-medium' : 'rate-low'">
                {{ row.rate }}%
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- Warning Students -->
    <div class="warning-card">
      <div class="card-header">
        <h3>
          <el-icon color="#ef4444"><Warning /></el-icon>
          就业预警学生
        </h3>
        <router-link to="/school/warnings" class="see-more">
          查看全部
          <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <el-table :data="warningStudents" size="small">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="college" label="学院" />
        <el-table-column prop="status" label="就业状态">
          <template #default="{ row }">
            <el-tag :type="row.status === '未签约' ? 'danger' : 'warning'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="gpa" label="GPA" align="center" />
        <el-table-column label="操作" width="120" align="center">
          <template #default>
            <el-button type="primary" size="small" text>帮扶</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.school-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.stat-change {
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
}

.stat-change.positive {
  color: #22c55e;
}

.stat-change.negative {
  color: #ef4444;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-card,
.ranking-card,
.warning-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.see-more {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #667eea;
  font-size: 13px;
  text-decoration: none;
}

.see-more:hover {
  text-decoration: underline;
}

.trend-chart {
  height: 280px;
}

.rate-high {
  color: #22c55e;
  font-weight: 600;
}

.rate-medium {
  color: #f59e0b;
  font-weight: 600;
}

.rate-low {
  color: #ef4444;
  font-weight: 600;
}

@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
