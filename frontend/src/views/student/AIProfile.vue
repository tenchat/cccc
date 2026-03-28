<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent])

const formRef = ref()
const loading = ref(false)
const hasResult = ref(false)

const formData = reactive({
  专业: '',
  GPA: '',
  技能: '',
  目标城市: '',
  实习经历: ''
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
          value: [0, 0, 0, 0, 0, 0],
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

const profileResult = ref({
  综合评分: 0,
  优势: [] as string[],
  劣势: [] as string[],
  建议: [] as string[]
})

const handleAnalyze = async () => {
  if (!formData.专业 || !formData.技能) {
    ElMessage.warning('请至少填写专业和技能信息')
    return
  }

  loading.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2000))

  // Mock result
  const mockScores = [85, 78, 88, 75, 82, 70]
  radarOptions.value.series[0].data[0].value = mockScores

  profileResult.value = {
    综合评分: Math.round(mockScores.reduce((a, b) => a + b, 0) / mockScores.length),
    优势: [
      '技术能力扎实，掌握主流前端框架',
      '有多个项目实战经验',
      '学习能力强，适应快速变化的技术环境'
    ],
    劣势: [
      '缺乏大厂实习经验',
      '沟通表达能力有待提升',
      '算法和数据结构基础较弱'
    ],
    建议: [
      '建议积极投递中大型互联网公司',
      '加强系统设计能力的培养',
      '考虑报考相关专业的研究生提升竞争力'
    ]
  }

  hasResult.value = true
  loading.value = false
  ElMessage.success('分析完成')
}

const resetForm = () => {
  Object.keys(formData).forEach(key => {
    formData[key as keyof typeof formData] = ''
  })
  hasResult.value = false
}
</script>

<template>
  <div class="ai-profile-page">
    <div class="page-header">
      <h2>AI就业画像</h2>
      <p class="page-desc">基于您的信息，AI将为您生成个性化的就业竞争力分析报告</p>
    </div>

    <div class="profile-content">
      <div class="form-section">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          <el-form
            ref="formRef"
            :model="formData"
            label-width="100px"
            class="profile-form"
          >
            <el-form-item label="专业">
              <el-input v-model="formData.专业" placeholder="如：计算机科学与技术" />
            </el-form-item>

            <el-form-item label="GPA">
              <el-input v-model="formData.GPA" placeholder="如：3.5/4.0" />
            </el-form-item>

            <el-form-item label="技能">
              <el-input
                v-model="formData.技能"
                type="textarea"
                :rows="3"
                placeholder="请输入您掌握的技能，如：Vue, React, TypeScript, Node.js"
              />
            </el-form-item>

            <el-form-item label="目标城市">
              <el-input v-model="formData.目标城市" placeholder="如：杭州" />
            </el-form-item>

            <el-form-item label="实习经历">
              <el-input
                v-model="formData.实习经历"
                type="textarea"
                :rows="3"
                placeholder="请描述您的实习经历"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" :loading="loading" @click="handleAnalyze">
                开始分析
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>

      <div class="result-section" v-if="hasResult">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>分析结果</span>
            </div>
          </template>

          <div class="result-content">
            <!-- Score Display -->
            <div class="score-display">
              <el-progress
                type="dashboard"
                :percentage="profileResult.综合评分"
                :width="160"
                :stroke-width="14"
                color="#667eea"
              >
                <template #default>
                  <span class="score-value">{{ profileResult.综合评分 }}</span>
                  <span class="score-label">综合评分</span>
                </template>
              </el-progress>
            </div>

            <!-- Radar Chart -->
            <div class="chart-container">
              <VChart class="radar-chart" :option="radarOptions" autoresize />
            </div>

            <!-- Strengths -->
            <div class="result-item">
              <div class="result-title">
                <el-icon color="#22c55e"><CircleCheckFilled /></el-icon>
                <span>优势</span>
              </div>
              <ul class="result-list">
                <li v-for="(item, index) in profileResult.优势" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>

            <!-- Weaknesses -->
            <div class="result-item">
              <div class="result-title">
                <el-icon color="#ef4444"><WarningFilled /></el-icon>
                <span>劣势</span>
              </div>
              <ul class="result-list">
                <li v-for="(item, index) in profileResult.劣势" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>

            <!-- Suggestions -->
            <div class="result-item">
              <div class="result-title">
                <el-icon color="#667eea"><LightbulbFilled /></el-icon>
                <span>建议</span>
              </div>
              <ul class="result-list">
                <li v-for="(item, index) in profileResult.建议" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty description="请填写上方表单，点击开始分析获取您的就业画像">
          <template #image>
            <el-icon :size="80" color="#d1d5db"><Cpu /></el-icon>
          </template>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-profile-page {
  max-width: 900px;
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

.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-section,
.result-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.card-header {
  font-weight: 600;
  color: #1e293b;
}

.profile-form {
  margin-top: 16px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.score-display {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.score-value {
  font-size: 56px;
  font-weight: 700;
  color: #667eea;
}

.score-label {
  display: block;
  font-size: 14px;
  color: #64748b;
}

.chart-container {
  width: 100%;
  height: 300px;
}

.radar-chart {
  width: 100%;
  height: 100%;
}

.result-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.result-list {
  margin: 0;
  padding-left: 24px;
}

.result-list li {
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
}

.empty-state {
  grid-column: 1 / -1;
  background: white;
  border-radius: 16px;
  padding: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

@media (max-width: 900px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}
</style>
