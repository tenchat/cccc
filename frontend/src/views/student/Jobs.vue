<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const filters = reactive({
  city: '',
  industry: '',
  salaryRange: ''
})

const jobList = ref([
  {
    id: 1,
    title: '前端开发工程师',
    company: '阿里巴巴',
    logo: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    city: '杭州',
    salary: '25K-35K',
    experience: '1-3年',
    education: '本科',
    tags: ['Vue', 'React', 'TypeScript'],
    publishedAt: '2天前',
    match: 95
  },
  {
    id: 2,
    title: 'React开发工程师',
    company: '字节跳动',
    logo: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    city: '北京',
    salary: '30K-40K',
    experience: '1-3年',
    education: '本科',
    tags: ['React', 'Redux', 'Node.js'],
    publishedAt: '1天前',
    match: 88
  },
  {
    id: 3,
    title: '全栈开发工程师',
    company: '腾讯',
    logo: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    city: '深圳',
    salary: '28K-38K',
    experience: '3-5年',
    education: '本科',
    tags: ['Node.js', 'Vue', 'MongoDB'],
    publishedAt: '3天前',
    match: 82
  },
  {
    id: 4,
    title: 'Vue开发工程师',
    company: '美团',
    logo: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    city: '北京',
    salary: '22K-32K',
    experience: '1-3年',
    education: '本科',
    tags: ['Vue', 'JavaScript', 'CSS'],
    publishedAt: '5天前',
    match: 78
  }
])

const selectedJob = ref<typeof jobList.value[0] | null>(null)
const dialogVisible = ref(false)

const cityOptions = [
  { value: '杭州', label: '杭州' },
  { value: '北京', label: '北京' },
  { value: '深圳', label: '深圳' },
  { value: '上海', label: '上海' }
]

const industryOptions = [
  { value: '互联网', label: '互联网' },
  { value: '金融', label: '金融' },
  { value: '教育', label: '教育' },
  { value: '医疗', label: '医疗' }
]

const salaryOptions = [
  { value: '10K以下', label: '10K以下' },
  { value: '10K-20K', label: '10K-20K' },
  { value: '20K-30K', label: '20K-30K' },
  { value: '30K以上', label: '30K以上' }
]

const showJobDetail = (job: typeof jobList.value[0]) => {
  selectedJob.value = job
  dialogVisible.value = true
}

const applyJob = () => {
  ElMessage.success('简历投递成功')
  dialogVisible.value = false
}

const resetFilters = () => {
  filters.city = ''
  filters.industry = ''
  filters.salaryRange = ''
}
</script>

<template>
  <div class="jobs-page">
    <div class="page-header">
      <h2>岗位推荐</h2>
      <p class="page-desc">根据您的简历和求职意向，智能推荐最匹配的岗位</p>
    </div>

    <!-- Filters -->
    <div class="filters-card">
      <div class="filters-row">
        <el-select
          v-model="filters.city"
          placeholder="选择城市"
          clearable
          style="width: 160px"
        >
          <el-option
            v-for="city in cityOptions"
            :key="city.value"
            :label="city.label"
            :value="city.value"
          />
        </el-select>

        <el-select
          v-model="filters.industry"
          placeholder="选择行业"
          clearable
          style="width: 160px"
        >
          <el-option
            v-for="ind in industryOptions"
            :key="ind.value"
            :label="ind.label"
            :value="ind.value"
          />
        </el-select>

        <el-select
          v-model="filters.salaryRange"
          placeholder="薪资范围"
          clearable
          style="width: 160px"
        >
          <el-option
            v-for="sal in salaryOptions"
            :key="sal.value"
            :label="sal.label"
            :value="sal.value"
          />
        </el-select>

        <el-button @click="resetFilters">重置</el-button>
      </div>
    </div>

    <!-- Job List -->
    <div class="job-list">
      <div
        v-for="job in jobList"
        :key="job.id"
        class="job-card"
        @click="showJobDetail(job)"
      >
        <div class="job-main">
          <div class="job-header">
            <h3 class="job-title">{{ job.title }}</h3>
            <el-tag type="success" size="small">匹配度 {{ job.match }}%</el-tag>
          </div>
          <div class="job-company">
            <el-avatar :size="32" :src="job.logo" />
            <span class="company-name">{{ job.company }}</span>
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
        </div>
        <div class="job-side">
          <span class="publish-time">{{ job.publishedAt }}</span>
          <el-button type="primary" size="small" @click.stop="applyJob">
            投递简历
          </el-button>
        </div>
      </div>
    </div>

    <!-- Job Detail Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="selectedJob?.title"
      width="600px"
    >
      <div v-if="selectedJob" class="job-detail">
        <div class="detail-header">
          <div class="detail-company">
            <el-avatar :size="48" :src="selectedJob.logo" />
            <div class="detail-company-info">
              <h4>{{ selectedJob.company }}</h4>
              <span class="detail-location">
                <el-icon><Location /></el-icon>
                {{ selectedJob.city }}
              </span>
            </div>
          </div>
          <div class="detail-salary">{{ selectedJob.salary }}</div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h5>职位描述</h5>
          <p>
            1. 负责公司产品的前端开发工作；<br />
            2. 参与前端架构设计和技术选型；<br />
            3. 优化前端性能，提升用户体验；<br />
            4. 与后端团队紧密配合，实现数据交互。
          </p>
        </div>

        <div class="detail-section">
          <h5>职位要求</h5>
          <p>
            1. 本科及以上学历，计算机相关专业；<br />
            2. 1-3年前端开发经验，熟练掌握Vue或React；<br />
            3. 熟悉TypeScript，熟悉前端工程化；<br />
            4. 良好的沟通能力和团队协作精神。
          </p>
        </div>

        <div class="detail-section">
          <h5>技能要求</h5>
          <div class="detail-tags">
            <el-tag
              v-for="tag in selectedJob.tags"
              :key="tag"
              effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="applyJob">投递简历</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.jobs-page {
  max-width: 1000px;
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

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.filters-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
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
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
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

.job-company {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.company-name {
  font-size: 14px;
  color: #64748b;
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
}

.job-side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 16px;
}

.publish-time {
  font-size: 12px;
  color: #94a3b8;
}

/* Dialog styles */
.job-detail {
  padding: 8px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.detail-company {
  display: flex;
  gap: 12px;
}

.detail-company-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
}

.detail-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.detail-salary {
  font-size: 20px;
  font-weight: 700;
  color: #22c55e;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h5 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.detail-section p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
  margin: 0;
}

.detail-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
