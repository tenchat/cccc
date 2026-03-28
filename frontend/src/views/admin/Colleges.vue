<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const selectedYear = ref('2024')

const collegeData = ref([
  { id: 1, name: '计算机学院', code: 'CS', total: 520, employed: 458, rate: 88.1, avgSalary: 18500, rank: 1 },
  { id: 2, name: '软件学院', code: 'SE', total: 380, employed: 328, rate: 86.3, avgSalary: 17500, rank: 2 },
  { id: 3, name: '信息工程学院', code: 'IE', total: 420, employed: 356, rate: 84.8, avgSalary: 15200, rank: 3 },
  { id: 4, name: '机械工程学院', code: 'ME', total: 350, employed: 285, rate: 81.4, avgSalary: 11000, rank: 4 },
  { id: 5, name: '经济管理学院', code: 'EM', total: 580, employed: 458, rate: 79.0, avgSalary: 12500, rank: 5 },
  { id: 6, name: '外语学院', code: 'FL', total: 280, employed: 198, rate: 70.7, avgSalary: 8500, rank: 6 },
  { id: 7, name: '化学化工学院', code: 'CE', total: 260, employed: 189, rate: 72.7, avgSalary: 9800, rank: 7 },
  { id: 8, name: '生物学院', code: 'BIO', total: 220, employed: 154, rate: 70.0, avgSalary: 9200, rank: 8 },
  { id: 9, name: '数学学院', code: 'MA', total: 180, employed: 126, rate: 70.0, avgSalary: 11500, rank: 9 },
  { id: 10, name: '物理学院', code: 'PH', total: 170, employed: 112, rate: 65.9, avgSalary: 10800, rank: 10 }
])

const barOptions = {
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  legend: { data: ['就业率', '签约率'], top: 10 },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
  xAxis: {
    type: 'category',
    data: collegeData.value.map(c => c.code),
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
      type: 'bar',
      data: collegeData.value.map(c => c.rate),
      itemStyle: {
        color: (params: any) => {
          const color = params.value >= 85 ? '#22c55e' : params.value >= 75 ? '#f59e0b' : '#ef4444'
          return color
        },
        borderRadius: [4, 4, 0, 0]
      }
    }
  ]
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}
</script>

<template>
  <div class="colleges-page">
    <div class="page-header">
      <div class="header-left">
        <h2>学院就业率</h2>
        <p class="page-desc">查看各学院的就业情况统计</p>
      </div>
      <div class="header-right">
        <el-select v-model="selectedYear" style="width: 120px; margin-right: 12px;">
          <el-option label="2024年" value="2024" />
          <el-option label="2023年" value="2023" />
          <el-option label="2022年" value="2022" />
        </el-select>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- Chart -->
    <div class="chart-card">
      <h3>就业率排名</h3>
      <VChart class="bar-chart" :option="barOptions" autoresize />
    </div>

    <!-- Table -->
    <div class="table-card">
      <el-table :data="collegeData" stripe>
        <el-table-column prop="rank" label="排名" width="80" align="center" />
        <el-table-column prop="name" label="学院名称" />
        <el-table-column prop="code" label="代码" width="80" align="center" />
        <el-table-column prop="total" label="毕业生数" width="100" align="center" />
        <el-table-column prop="employed" label="已就业" width="100" align="center" />
        <el-table-column prop="rate" label="就业率" width="100" align="center">
          <template #default="{ row }">
            <span :class="row.rate >= 85 ? 'rate-high' : row.rate >= 75 ? 'rate-medium' : 'rate-low'">
              {{ row.rate }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="avgSalary" label="平均薪资" width="120" align="center">
          <template #default="{ row }">
            {{ row.avgSalary.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template #default>
            <el-button type="primary" size="small" text>详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.colleges-page {
  max-width: 1200px;
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

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px;
}

.bar-chart {
  height: 350px;
}

.table-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
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
</style>
