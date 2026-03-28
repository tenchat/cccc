<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const warningLevel = ref('all')

const warningList = ref([
  {
    id: 1,
    name: '李四',
    studentId: '2020010002',
    college: '计算机学院',
    major: '计算机科学与技术',
    status: '未签约',
    gpa: 2.1,
    warningLevel: 'high',
    warningReason: 'GPA过低，且未有任何求职活动',
    followUp: '待跟进',
    followUpStaff: '张老师'
  },
  {
    id: 2,
    name: '王五',
    studentId: '2020010003',
    college: '机械工程学院',
    major: '机械设计',
    status: '求职中',
    gpa: 2.3,
    warningLevel: 'medium',
    warningReason: '已参加面试但未获得offer',
    followUp: '面试辅导',
    followUpStaff: '李老师'
  },
  {
    id: 3,
    name: '赵六',
    studentId: '2020010004',
    college: '外语学院',
    major: '英语',
    status: '未签约',
    gpa: 2.0,
    warningLevel: 'high',
    warningReason: '就业意向不明确，拒绝多次推荐',
    followUp: '谈话了解',
    followUpStaff: '王老师'
  },
  {
    id: 4,
    name: '钱七',
    studentId: '2020010005',
    college: '经济管理学院',
    major: '市场营销',
    status: '求职中',
    gpa: 2.4,
    warningLevel: 'medium',
    warningReason: '面试技巧不足',
    followUp: '面试培训',
    followUpStaff: '赵老师'
  },
  {
    id: 5,
    name: '孙八',
    studentId: '2020010006',
    college: '信息工程学院',
    major: '电子信息',
    status: '未签约',
    gpa: 1.9,
    warningLevel: 'high',
    warningReason: '多门课程不及格，有退学风险',
    followUp: '学业帮扶',
    followUpStaff: '刘老师'
  }
])

const statsData = reactive({
  total: 156,
  high: 23,
  medium: 58,
  low: 75
})

const levelOptions = [
  { value: 'all', label: '全部' },
  { value: 'high', label: '高风险' },
  { value: 'medium', label: '中风险' },
  { value: 'low', label: '低风险' }
]

const handleFollowUp = (row: typeof warningList.value[0]) => {
  ElMessage.success(`开始跟进：${row.name}`)
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}
</script>

<template>
  <div class="warnings-page">
    <div class="page-header">
      <h2>就业预警</h2>
      <p class="page-desc">对就业困难学生进行预警和帮扶</p>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-card" :class="{ active: warningLevel === 'all' }" @click="warningLevel = 'all'">
        <span class="stat-value">{{ statsData.total }}</span>
        <span class="stat-label">预警总数</span>
      </div>
      <div class="stat-card high" :class="{ active: warningLevel === 'high' }" @click="warningLevel = 'high'">
        <span class="stat-value">{{ statsData.high }}</span>
        <span class="stat-label">高风险</span>
      </div>
      <div class="stat-card medium" :class="{ active: warningLevel === 'medium' }" @click="warningLevel = 'medium'">
        <span class="stat-value">{{ statsData.medium }}</span>
        <span class="stat-label">中风险</span>
      </div>
      <div class="stat-card low" :class="{ active: warningLevel === 'low' }" @click="warningLevel = 'low'">
        <span class="stat-value">{{ statsData.low }}</span>
        <span class="stat-label">低风险</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-card">
      <div class="filter-left">
        <span class="filter-label">风险等级：</span>
        <el-radio-group v-model="warningLevel">
          <el-radio-button v-for="opt in levelOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </el-radio-button>
        </el-radio-group>
      </div>
      <div class="filter-right">
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>
    </div>

    <!-- Warning List -->
    <div class="table-card">
      <el-table :data="warningList" stripe>
        <el-table-column prop="name" label="姓名" width="80" />
        <el-table-column prop="studentId" label="学号" width="110" />
        <el-table-column prop="college" label="学院" width="120" />
        <el-table-column prop="major" label="专业" />
        <el-table-column prop="status" label="就业状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.status === '未签约' ? 'danger' : 'warning'"
              size="small"
            >
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="gpa" label="GPA" width="70" align="center" />
        <el-table-column prop="warningLevel" label="风险等级" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.warningLevel === 'high' ? 'danger' : row.warningLevel === 'medium' ? 'warning' : 'info'"
              size="small"
            >
              {{ row.warningLevel === 'high' ? '高' : row.warningLevel === 'medium' ? '中' : '低' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warningReason" label="预警原因" min-width="180" />
        <el-table-column prop="followUp" label="跟进状态" width="100" align="center">
          <template #default="{ row }">
            <span :class="row.followUp === '待跟进' ? 'followup-pending' : 'followup-done'">
              {{ row.followUp }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="followUpStaff" label="跟进人" width="80" align="center" />
        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="handleFollowUp(row)">
              帮扶
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="100"
          :page-size="10"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.warnings-page {
  max-width: 1400px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-desc {
  color: #64748b;
  font-size: 14px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card.active {
  border-color: #667eea;
}

.stat-card.high .stat-value {
  color: #ef4444;
}

.stat-card.medium .stat-value {
  color: #f59e0b;
}

.stat-card.low .stat-value {
  color: #22c55e;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.filter-label {
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
}

.table-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.followup-pending {
  color: #f59e0b;
  font-weight: 500;
}

.followup-done {
  color: #22c55e;
  font-weight: 500;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .filters-card {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>
