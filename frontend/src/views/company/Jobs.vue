<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const statusFilter = ref('all')

const jobList = ref([
  {
    id: 1,
    title: '前端开发工程师',
    city: '杭州',
    salary: '25K-35K',
    experience: '1-3年',
    education: '本科',
    tags: ['Vue', 'React', 'TypeScript'],
    status: 'active',
    publishTime: '2024-03-15',
    viewCount: 1256,
    applicationCount: 45
  },
  {
    id: 2,
    title: 'React开发工程师',
    city: '北京',
    salary: '30K-40K',
    experience: '1-3年',
    education: '本科',
    tags: ['React', 'Redux', 'Node.js'],
    status: 'active',
    publishTime: '2024-03-10',
    viewCount: 985,
    applicationCount: 32
  },
  {
    id: 3,
    title: '全栈开发工程师',
    city: '深圳',
    salary: '28K-38K',
    experience: '3-5年',
    education: '本科',
    tags: ['Node.js', 'Vue', 'MongoDB'],
    status: 'paused',
    publishTime: '2024-02-28',
    viewCount: 756,
    applicationCount: 28
  },
  {
    id: 4,
    title: 'Vue开发工程师',
    city: '上海',
    salary: '22K-32K',
    experience: '1-3年',
    education: '本科',
    tags: ['Vue', 'JavaScript', 'CSS'],
    status: 'closed',
    publishTime: '2024-02-15',
    viewCount: 562,
    applicationCount: 18
  }
])

const handleEdit = (row: typeof jobList.value[0]) => {
  ElMessage.info(`编辑岗位: ${row.title}`)
}

const handleDelete = (_row: typeof jobList.value[0]) => {
  ElMessageBox.confirm('确定要删除该岗位吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  })
}

const handleToggleStatus = (row: typeof jobList.value[0]) => {
  const newStatus = row.status === 'active' ? 'paused' : 'active'
  ElMessage.success(`${newStatus === 'active' ? '启用' : '暂停'}岗位成功`)
}
</script>

<template>
  <div class="jobs-page">
    <div class="page-header">
      <div class="header-left">
        <h2>岗位管理</h2>
        <p class="page-desc">管理企业发布的招聘信息</p>
      </div>
      <div class="header-right">
        <router-link to="/company/post-job">
          <el-button type="primary">
            <el-icon><Plus /></el-icon>
            发布新岗位
          </el-button>
        </router-link>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-card">
      <el-radio-group v-model="statusFilter">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button value="active">招聘中</el-radio-button>
        <el-radio-button value="paused">已暂停</el-radio-button>
        <el-radio-button value="closed">已结束</el-radio-button>
      </el-radio-group>
    </div>

    <!-- Job List -->
    <div class="job-list">
      <div
        v-for="job in jobList"
        :key="job.id"
        class="job-card"
      >
        <div class="job-main">
          <div class="job-header">
            <h3 class="job-title">{{ job.title }}</h3>
            <el-tag
              :type="job.status === 'active' ? 'success' : job.status === 'paused' ? 'warning' : 'info'"
              size="small"
            >
              {{ job.status === 'active' ? '招聘中' : job.status === 'paused' ? '已暂停' : '已结束' }}
            </el-tag>
          </div>

          <div class="job-info">
            <span class="info-item">
              <el-icon><Location /></el-icon>
              {{ job.city }}
            </span>
            <span class="info-item">
              <el-icon><Money /></el-icon>
              {{ job.salary }}
            </span>
            <span class="info-item">
              <el-icon><Clock /></el-icon>
              {{ job.experience }}
            </span>
            <span class="info-item">
              <el-icon><Medal /></el-icon>
              {{ job.education }}
            </span>
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

          <div class="job-stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              浏览 {{ job.viewCount }}
            </span>
            <span class="stat-item">
              <el-icon><Document /></el-icon>
              收到 {{ job.applicationCount }} 份简历
            </span>
            <span class="stat-item">
              <el-icon><Calendar /></el-icon>
              {{ job.publishTime }}
            </span>
          </div>
        </div>

        <div class="job-actions">
          <el-button type="primary" size="small" text @click="handleEdit(job)">
            编辑
          </el-button>
          <el-button
            :type="job.status === 'active' ? 'warning' : 'success'"
            size="small"
            text
            @click="handleToggleStatus(job)"
          >
            {{ job.status === 'active' ? '暂停' : '启用' }}
          </el-button>
          <el-button type="danger" size="small" text @click="handleDelete(job)">
            删除
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.jobs-page {
  max-width: 1100px;
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

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.job-main {
  flex: 1;
}

.job-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.job-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.job-info {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.job-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.job-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-left: 24px;
}
</style>
