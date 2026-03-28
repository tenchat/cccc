<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const skills = ref([
  { id: 1, name: '人工智能', demand: 12580, supply: 4280, gap: 8300, salary: 35000, trend: 'up' },
  { id: 2, name: '大数据开发', demand: 15820, supply: 6850, gap: 8970, salary: 28000, trend: 'up' },
  { id: 3, name: '网络安全', demand: 8960, supply: 3200, gap: 5760, salary: 32000, trend: 'up' },
  { id: 4, name: '云计算', demand: 11250, supply: 5650, gap: 5600, salary: 26000, trend: 'stable' },
  { id: 5, name: '区块链', demand: 5680, supply: 1890, gap: 3790, salary: 38000, trend: 'up' },
  { id: 6, name: '5G通信', demand: 7850, supply: 3450, gap: 4400, salary: 24000, trend: 'stable' },
  { id: 7, name: '嵌入式开发', demand: 6450, supply: 2890, gap: 3560, salary: 22000, trend: 'down' },
  { id: 8, name: '芯片设计', demand: 4580, supply: 1250, gap: 3330, salary: 45000, trend: 'up' }
])

const majorDemand = ref([
  { id: 1, major: '计算机科学与技术', demand: 25680, avgSalary: 18500, rank: 1 },
  { id: 2, major: '软件工程', demand: 21250, avgSalary: 17500, rank: 2 },
  { id: 3, major: '电子信息工程', demand: 15890, avgSalary: 15000, rank: 3 },
  { id: 4, major: '通信工程', demand: 12650, avgSalary: 16000, rank: 4 },
  { id: 5, major: '自动化', demand: 11200, avgSalary: 14000, rank: 5 },
  { id: 6, major: '机械设计', demand: 9850, avgSalary: 11000, rank: 6 }
])

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}
</script>

<template>
  <div class="scarce-talents-page">
    <div class="page-header">
      <div class="header-left">
        <h2>稀缺人才分析</h2>
        <p class="page-desc">分析当前市场上的人才供需情况，为专业设置和就业指导提供参考</p>
      </div>
      <div class="header-right">
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- Summary -->
    <div class="summary-row">
      <div class="summary-card">
        <div class="summary-icon blue">
          <el-icon :size="24"><TrendCharts /></el-icon>
        </div>
        <div class="summary-info">
          <span class="summary-value">{{ skills.reduce((sum, s) => sum + s.demand, 0).toLocaleString() }}</span>
          <span class="summary-label">总需求量</span>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon green">
          <el-icon :size="24"><User /></el-icon>
        </div>
        <div class="summary-info">
          <span class="summary-value">{{ skills.reduce((sum, s) => sum + s.supply, 0).toLocaleString() }}</span>
          <span class="summary-label">总供给量</span>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon orange">
          <el-icon :size="24"><Warning /></el-icon>
        </div>
        <div class="summary-info">
          <span class="summary-value">{{ skills.reduce((sum, s) => sum + s.gap, 0).toLocaleString() }}</span>
          <span class="summary-label">人才缺口</span>
        </div>
      </div>
    </div>

    <!-- Skills Gap Table -->
    <div class="table-card">
      <h3>热门技能人才缺口TOP榜</h3>
      <el-table :data="skills" stripe>
        <el-table-column prop="rank" label="排名" width="60" align="center">
          <template #default="{$index}">
            <span :class="$index < 3 ? 'rank-top' : ''">{{ $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="技能方向" />
        <el-table-column prop="demand" label="市场需求" width="120" align="center">
          <template #default="{ row }">
            {{ row.demand.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="supply" label="人才供给" width="120" align="center">
          <template #default="{ row }">
            {{ row.supply.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="gap" label="人才缺口" width="120" align="center">
          <template #default="{ row }">
            <span class="gap-value">{{ row.gap.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="salary" label="平均薪资" width="120" align="center">
          <template #default="{ row }">
            <span class="salary-value">{{ row.salary.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="trend" label="趋势" width="80" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.trend === 'up' ? 'success' : row.trend === 'down' ? 'danger' : 'warning'"
              size="small"
            >
              {{ row.trend === 'up' ? '上升' : row.trend === 'down' ? '下降' : '平稳' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="供需比" width="180" align="center">
          <template #default="{ row }">
            <el-progress
              :percentage="Math.round((row.supply / row.demand) * 100)"
              :color="row.gap > 5000 ? '#ef4444' : row.gap > 3000 ? '#f59e0b' : '#22c55e'"
              :stroke-width="8"
            >
              <template #default="{ percentage }">
                {{ percentage }}%
              </template>
            </el-progress>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Major Demand Table -->
    <div class="table-card">
      <h3>专业需求量TOP榜</h3>
      <el-table :data="majorDemand" stripe>
        <el-table-column prop="rank" label="排名" width="60" align="center">
          <template #default="{$index}">
            <span :class="$index < 3 ? 'rank-top' : ''">{{ $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="major" label="专业名称" />
        <el-table-column prop="demand" label="需求量" width="120" align="center">
          <template #default="{ row }">
            {{ row.demand.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="avgSalary" label="平均薪资" width="120" align="center">
          <template #default="{ row }">
            <span class="salary-value">{{ row.avgSalary.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column label="供需比" width="180" align="center">
          <template #default="{ row }">
            <el-progress
              :percentage="Math.round((row.demand / 30000) * 100)"
              color="#667eea"
              :stroke-width="8"
            >
              <template #default="{ percentage }">
                {{ percentage }}%
              </template>
            </el-progress>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.scarce-talents-page {
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

.summary-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.summary-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-icon.blue { background: rgba(102, 126, 234, 0.1); color: #667eea; }
.summary-icon.green { background: rgba(34, 197, 94, 0.1); color: #22c55e; }
.summary-icon.orange { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }

.summary-info {
  display: flex;
  flex-direction: column;
}

.summary-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.summary-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.table-card {
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
  margin: 0 0 20px;
}

.rank-top {
  color: #667eea;
  font-weight: 700;
}

.gap-value {
  color: #ef4444;
  font-weight: 600;
}

.salary-value {
  color: #22c55e;
  font-weight: 600;
}
</style>
