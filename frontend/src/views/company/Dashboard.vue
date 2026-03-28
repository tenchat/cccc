<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const statsData = ref({
  totalJobs: 28,
  activeJobs: 15,
  totalApplications: 1256,
  newApplications: 86,
  viewCount: 15890,
  matchRate: 68.5
})

const recentApplications = ref([
  { id: 1, name: '张三', position: '前端开发工程师', college: '计算机学院', applyTime: '2小时前', status: '待查看' },
  { id: 2, name: '李四', position: '前端开发工程师', college: '软件学院', applyTime: '3小时前', status: '已投递' },
  { id: 3, name: '王五', position: 'React开发工程师', college: '信息工程学院', applyTime: '5小时前', status: '待查看' },
  { id: 4, name: '赵六', position: 'Vue开发工程师', college: '计算机学院', applyTime: '1天前', status: '已投递' }
])

const quickActions = [
  {
    title: '发布岗位',
    icon: 'Plus',
    color: '#667eea',
    path: '/company/post-job'
  },
  {
    title: '岗位管理',
    icon: 'Briefcase',
    color: '#22c55e',
    path: '/company/jobs'
  }
]
</script>

<template>
  <div class="company-dashboard">
    <div class="page-header">
      <h2>招聘概况</h2>
      <p class="page-desc">欢迎使用企业招聘管理系统</p>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(102, 126, 234, 0.1);">
          <el-icon :size="28" color="#667eea"><Briefcase /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.totalJobs }}</span>
          <span class="stat-label">岗位总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(34, 197, 94, 0.1);">
          <el-icon :size="28" color="#22c55e"><CircleCheck /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.activeJobs }}</span>
          <span class="stat-label">在招岗位</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1);">
          <el-icon :size="28" color="#f59e0b"><User /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.totalApplications }}</span>
          <span class="stat-label">收到简历</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(14, 165, 233, 0.1);">
          <el-icon :size="28" color="#0ea5e9"><View /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ statsData.viewCount.toLocaleString() }}</span>
          <span class="stat-label">浏览次数</span>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <!-- Quick Actions -->
      <div class="actions-card">
        <h3>快捷操作</h3>
        <div class="actions-row">
          <div
            v-for="action in quickActions"
            :key="action.title"
            class="action-item"
            @click="router.push(action.path)"
          >
            <div class="action-icon" :style="{ background: action.color + '15', color: action.color }">
              <el-icon :size="24">
                <component :is="action.icon" />
              </el-icon>
            </div>
            <span class="action-title">{{ action.title }}</span>
          </div>
        </div>
      </div>

      <!-- Recent Applications -->
      <div class="applications-card">
        <h3>最近投递</h3>
        <el-table :data="recentApplications" size="small">
          <el-table-column prop="name" label="姓名" width="80" />
          <el-table-column prop="position" label="应聘岗位" />
          <el-table-column prop="college" label="院校" />
          <el-table-column prop="applyTime" label="投递时间" width="100" />
          <el-table-column prop="status" label="状态" width="80" align="center">
            <template #default="{ row }">
              <el-tag
                :type="row.status === '待查看' ? 'warning' : 'success'"
                size="small"
              >
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- Match Rate -->
    <div class="match-card">
      <h3>岗位匹配度</h3>
      <div class="match-content">
        <el-progress
          type="dashboard"
          :percentage="statsData.matchRate"
          :width="160"
          :stroke-width="14"
          color="#667eea"
        >
          <template #default>
            <span class="match-value">{{ statsData.matchRate }}%</span>
            <span class="match-label">平均匹配度</span>
          </template>
        </el-progress>
        <div class="match-tips">
          <h4>提升匹配度建议</h4>
          <ul>
            <li>完善岗位要求描述，精准匹配人才</li>
            <li>及时查看并回复候选人投递</li>
            <li>定期更新岗位信息，保持活跃度</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.company-dashboard {
  max-width: 1100px;
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
  grid-template-columns: 300px 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.actions-card,
.applications-card,
.match-card {
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

.actions-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
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
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.match-card {
  margin-bottom: 24px;
}

.match-content {
  display: flex;
  align-items: center;
  gap: 48px;
}

.match-value {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: #667eea;
}

.match-label {
  display: block;
  font-size: 12px;
  color: #64748b;
}

.match-tips {
  flex: 1;
}

.match-tips h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px;
}

.match-tips ul {
  margin: 0;
  padding-left: 20px;
}

.match-tips li {
  font-size: 13px;
  color: #64748b;
  line-height: 1.8;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .match-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>
