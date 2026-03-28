<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent])

const userStore = useUserStore()

const employmentStatus = ref({
  status: 'employed',
  company: '阿里巴巴',
  position: '前端开发工程师',
  salary: '25K'
})

const radarOptions = ref({
  tooltip: {},
  radar: {
    indicator: [
      { name: '技术能力', max: 100 },
      { name: '项目经验', max: 100 },
      { name: '学术成绩', max: 100 },
      { name: '沟通表达', max: 100 },
      { name: '团队协作', max: 100 },
      { name: '创新能力', max: 100 }
    ],
    radius: '65%'
  },
  series: [
    {
      type: 'radar',
      data: [
        {
          value: [85, 78, 92, 80, 88, 75],
          name: '就业竞争力评估',
          areaStyle: {
            color: 'rgba(102, 126, 234, 0.3)'
          },
          lineStyle: {
            color: '#667eea'
          },
          itemStyle: {
            color: '#667eea'
          }
        }
      ]
    }
  ]
})

const recommendedJobs = ref([
  {
    id: 1,
    title: '前端开发工程师',
    company: '阿里巴巴',
    city: '杭州',
    salary: '25K-35K',
    tags: ['Vue', 'React', 'TypeScript'],
    match: 95
  },
  {
    id: 2,
    title: 'React开发工程师',
    company: '字节跳动',
    city: '北京',
    salary: '30K-40K',
    tags: ['React', 'Redux', 'Node.js'],
    match: 88
  },
  {
    id: 3,
    title: '全栈开发工程师',
    company: '腾讯',
    city: '深圳',
    salary: '28K-38K',
    tags: ['Node.js', 'Vue', 'MongoDB'],
    match: 82
  }
])

const greeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return '上午好'
  if (hour < 18) return '下午好'
  return '晚上好'
}
</script>

<template>
  <div class="student-dashboard">
    <!-- Welcome Card -->
    <div class="welcome-card">
      <div class="welcome-content">
        <h2 class="welcome-title">{{ greeting() }}，{{ userStore.realName || '同学' }}</h2>
        <p class="welcome-subtitle">欢迎使用大学生就业信息智能分析平台</p>
      </div>
      <div class="welcome-chart">
        <VChart class="mini-chart" :option="radarOptions" autoresize />
      </div>
    </div>

    <!-- Employment Status -->
    <div class="status-card">
      <div class="status-header">
        <el-icon :size="24" color="#22c55e"><CircleCheckFilled /></el-icon>
        <h3>就业状态</h3>
      </div>
      <div class="status-content">
        <div class="status-item">
          <span class="label">状态</span>
          <span class="value status-employed">已就业</span>
        </div>
        <div class="status-item">
          <span class="label">公司</span>
          <span class="value">{{ employmentStatus.company }}</span>
        </div>
        <div class="status-item">
          <span class="label">岗位</span>
          <span class="value">{{ employmentStatus.position }}</span>
        </div>
        <div class="status-item">
          <span class="label">薪资</span>
          <span class="value salary">{{ employmentStatus.salary }}</span>
        </div>
      </div>
    </div>

    <!-- AI Score Card -->
    <div class="ai-score-card">
      <div class="score-header">
        <el-icon :size="24" color="#667eea"><Cpu /></el-icon>
        <h3>AI就业评分</h3>
      </div>
      <div class="score-display">
        <el-progress
          type="dashboard"
          :percentage="85"
          :width="140"
          :stroke-width="12"
          color="#667eea"
        >
          <template #default>
            <span class="score-value">85</span>
            <span class="score-label">分</span>
          </template>
        </el-progress>
      </div>
      <p class="score-tip">您的就业竞争力高于 85% 的应届毕业生</p>
    </div>

    <!-- Recommended Jobs -->
    <div class="jobs-section">
      <div class="section-header">
        <h3>推荐岗位</h3>
        <router-link to="/student/jobs" class="see-more">
          查看更多
          <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <div class="jobs-grid">
        <div
          v-for="job in recommendedJobs"
          :key="job.id"
          class="job-card"
        >
          <div class="job-header">
            <h4 class="job-title">{{ job.title }}</h4>
            <el-tag type="success" size="small">匹配度 {{ job.match }}%</el-tag>
          </div>
          <p class="job-company">{{ job.company }}</p>
          <div class="job-info">
            <span class="job-city">
              <el-icon><Location /></el-icon>
              {{ job.city }}
            </span>
            <span class="job-salary">{{ job.salary }}</span>
          </div>
          <div class="job-tags">
            <el-tag
              v-for="tag in job.tags"
              :key="tag"
              size="small"
              effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>
          <el-button type="primary" size="small" class="apply-btn">投递简历</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.welcome-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.mini-chart {
  width: 200px;
  height: 180px;
}

.status-card,
.ai-score-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.status-header,
.score-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.status-header h3,
.score-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.status-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-item .label {
  font-size: 12px;
  color: #64748b;
}

.status-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.status-employed {
  color: #22c55e;
}

.salary {
  color: #667eea;
}

.score-display {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.score-value {
  font-size: 48px;
  font-weight: 700;
  color: #667eea;
}

.score-label {
  font-size: 18px;
  color: #64748b;
  margin-left: 4px;
}

.score-tip {
  text-align: center;
  color: #64748b;
  font-size: 14px;
  margin-top: 16px;
}

.jobs-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.see-more {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #667eea;
  font-size: 14px;
  text-decoration: none;
}

.see-more:hover {
  text-decoration: underline;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.job-card {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
}

.job-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.job-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.job-company {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 12px;
}

.job-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.job-city {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.job-salary {
  font-size: 16px;
  font-weight: 600;
  color: #22c55e;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.apply-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

@media (max-width: 1200px) {
  .jobs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .welcome-card {
    flex-direction: column;
    gap: 20px;
  }

  .mini-chart {
    width: 100%;
    height: 150px;
  }

  .jobs-grid {
    grid-template-columns: 1fr;
  }

  .status-content {
    grid-template-columns: 1fr;
  }
}
</style>
