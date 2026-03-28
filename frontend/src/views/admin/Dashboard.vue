<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const quickActions = [
  {
    title: '数据统计分析',
    icon: 'DataAnalysis',
    color: '#667eea',
    path: '/admin/statistics',
    desc: '查看详细统计数据'
  },
  {
    title: '学院就业率',
    icon: 'OfficeBuilding',
    color: '#22c55e',
    path: '/admin/colleges',
    desc: '各学院就业情况'
  },
  {
    title: '稀缺人才',
    icon: 'Star',
    color: '#f59e0b',
    path: '/admin/scarce-talents',
    desc: '市场稀缺人才分析'
  },
  {
    title: '数据大屏',
    icon: 'Monitor',
    color: '#0ea5e9',
    path: '/admin/databoard',
    desc: '可视化数据大屏'
  }
]

const recentActivities = ref([
  { id: 1, action: '新增学生签约', detail: '计算机学院 张三 签约 阿里巴巴', time: '10分钟前' },
  { id: 2, action: '岗位发布', detail: '字节跳动发布 前端开发工程师', time: '30分钟前' },
  { id: 3, action: '预警处理', detail: '机械学院 李四 已完成帮扶', time: '1小时前' },
  { id: 4, action: '数据更新', detail: '2024届就业数据已更新', time: '2小时前' },
  { id: 5, action: '新增企业', detail: '华为 已完成企业认证', time: '3小时前' }
])

const systemStats = ref({
  totalSchools: 45,
  totalStudents: 125680,
  totalCompanies: 1258,
  totalJobs: 5632,
  employmentRate: 78.5,
  jobGrowth: 12.3
})
</script>

<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h2>管理后台</h2>
      <p class="page-desc">欢迎使用大学生就业信息智能分析平台管理系统</p>
    </div>

    <!-- System Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(102, 126, 234, 0.1);">
          <el-icon :size="28" color="#667eea"><OfficeBuilding /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ systemStats.totalSchools }}</span>
          <span class="stat-label">入驻学校</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(34, 197, 94, 0.1);">
          <el-icon :size="28" color="#22c55e"><User /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ systemStats.totalStudents.toLocaleString() }}</span>
          <span class="stat-label">学生总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1);">
          <el-icon :size="28" color="#f59e0b"><OfficeBuilding /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ systemStats.totalCompanies.toLocaleString() }}</span>
          <span class="stat-label">入驻企业</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(14, 165, 233, 0.1);">
          <el-icon :size="28" color="#0ea5e9"><Briefcase /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ systemStats.totalJobs.toLocaleString() }}</span>
          <span class="stat-label">岗位总数</span>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <!-- Quick Actions -->
      <div class="actions-card">
        <h3>快捷入口</h3>
        <div class="actions-grid">
          <div
            v-for="action in quickActions"
            :key="action.title"
            class="action-item"
            @click="router.push(action.path)"
          >
            <div class="action-icon" :style="{ background: action.color + '15', color: action.color }">
              <el-icon :size="28">
                <component :is="action.icon" />
              </el-icon>
            </div>
            <div class="action-text">
              <span class="action-title">{{ action.title }}</span>
              <span class="action-desc">{{ action.desc }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities -->
      <div class="activities-card">
        <h3>最近动态</h3>
        <div class="activities-list">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-dot"></div>
            <div class="activity-content">
              <span class="activity-action">{{ activity.action }}</span>
              <span class="activity-detail">{{ activity.detail }}</span>
            </div>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Employment Overview -->
    <div class="overview-card">
      <h3>就业率概况</h3>
      <div class="overview-stats">
        <div class="overview-stat">
          <span class="overview-value">{{ systemStats.employmentRate }}%</span>
          <span class="overview-label">全国平均就业率</span>
        </div>
        <div class="overview-stat">
          <span class="overview-value positive">+{{ systemStats.jobGrowth }}%</span>
          <span class="overview-label">较去年增长</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
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

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.actions-card,
.activities-card,
.overview-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.02);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-text {
  display: flex;
  flex-direction: column;
}

.action-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.action-desc {
  font-size: 12px;
  color: #64748b;
}

.activities-list {
  display: flex;
  flex-direction: column;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
}

.activity-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-action {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.activity-detail {
  font-size: 12px;
  color: #64748b;
}

.activity-time {
  font-size: 12px;
  color: #94a3b8;
}

.overview-stats {
  display: flex;
  gap: 48px;
}

.overview-stat {
  display: flex;
  flex-direction: column;
}

.overview-value {
  font-size: 36px;
  font-weight: 700;
  color: #667eea;
}

.overview-value.positive {
  color: #22c55e;
}

.overview-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
