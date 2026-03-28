<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const formRef = ref()
const loading = ref(false)
const hasResult = ref(false)

const formData = reactive({
  GPA: '',
  目标院校: '',
  专业: '',
  学费预算: '',
  就业方向: ''
})

const barOptions = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['考研', '就业'] },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: {
    type: 'category',
    data: ['起薪', '发展潜力', '时间成本', '难度系数', '总体收益']
  },
  yAxis: { type: 'value', max: 100 },
  series: [
    {
      name: '考研',
      type: 'bar',
      data: resultData.value?.考研分析 || [65, 85, 75, 80, 78],
      itemStyle: { color: '#667eea' }
    },
    {
      name: '就业',
      type: 'bar',
      data: resultData.value?.就业分析 || [80, 70, 90, 60, 82],
      itemStyle: { color: '#22c55e' }
    }
  ]
}))

const pieOptions = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', left: 'left' },
  series: [
    {
      name: '建议比例',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' }
      },
      data: resultData.value?.建议比例 || [
        { value: 60, name: '建议就业', itemStyle: { color: '#22c55e' } },
        { value: 40, name: '建议考研', itemStyle: { color: '#667eea' } }
      ]
    }
  ]
}))

const resultData = ref<{
  综合建议: string
  考研分析: number[]
  就业分析: number[]
  建议比例: { value: number; name: string; itemStyle: { color: string } }[]
  详细分析: {
    考研: string[]
    就业: string[]
  }
} | null>(null)

const handleAnalyze = async () => {
  if (!formData.GPA || !formData.目标院校) {
    ElMessage.warning('请填写GPA和目标院校信息')
    return
  }

  loading.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2000))

  // Mock result
  resultData.value = {
    综合建议: '根据您的情况（ GPA 3.5，目标院校为211/985高校），建议您优先考虑考研。考研可以提升您的学历背景，在长期职业发展中具有明显优势。但如果能够获得知名企业的实习机会，也可以考虑先就业积累经验。',
    考研分析: [60, 88, 70, 85, 76],
    就业分析: [85, 72, 95, 55, 80],
    建议比例: [
      { value: 65, name: '建议考研', itemStyle: { color: '#667eea' } },
      { value: 35, name: '建议就业', itemStyle: { color: '#22c55e' } }
    ],
    详细分析: {
      考研: [
        '您的GPA较高（3.5+），考研上岸概率较大',
        '目标院校为211/985，毕业后竞争力显著提升',
        '研究生起薪平均比本科生高30-50%',
        '适合对学术研究有兴趣的同学'
      ],
      就业: [
        '当前就业市场对技术人才需求旺盛',
        '您有相关项目经验，可快速适应工作',
        '3年工作经验可能比普通研究生更有价值',
        '适合希望尽早积累实战经验的同学'
      ]
    }
  }

  hasResult.value = true
  loading.value = false
  ElMessage.success('分析完成')
}
</script>

<template>
  <div class="ai-decision-page">
    <div class="page-header">
      <h2>考研 vs 就业</h2>
      <p class="page-desc">AI将根据您的情况，分析考研与就业的优劣，为您做出合理建议</p>
    </div>

    <div class="decision-content">
      <div class="form-section">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <el-form
            ref="formRef"
            :model="formData"
            label-width="100px"
            class="decision-form"
          >
            <el-form-item label="GPA">
              <el-input v-model="formData.GPA" placeholder="如：3.5/4.0" />
            </el-form-item>

            <el-form-item label="目标院校">
              <el-input v-model="formData.目标院校" placeholder="如：浙江大学" />
            </el-form-item>

            <el-form-item label="专业">
              <el-input v-model="formData.专业" placeholder="如：计算机科学与技术" />
            </el-form-item>

            <el-form-item label="学费预算">
              <el-select v-model="formData.学费预算" placeholder="请选择" style="width: 100%">
                <el-option label="10万以下" value="10万以下" />
                <el-option label="10-20万" value="10-20万" />
                <el-option label="20-30万" value="20-30万" />
                <el-option label="30万以上" value="30万以上" />
              </el-select>
            </el-form-item>

            <el-form-item label="就业方向">
              <el-input v-model="formData.就业方向" placeholder="如：互联网技术岗位" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" :loading="loading" @click="handleAnalyze">
                开始分析
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>

      <div class="result-section" v-if="hasResult && resultData">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>分析结果</span>
            </div>
          </template>

          <div class="result-content">
            <!-- Recommendation Banner -->
            <div class="recommendation-banner">
              <el-icon :size="32" color="#667eea"><TrendCharts /></el-icon>
              <div class="recommendation-text">
                <h4>综合建议</h4>
                <p>{{ resultData.综合建议 }}</p>
              </div>
            </div>

            <!-- Charts -->
            <div class="charts-row">
              <div class="chart-item">
                <h5>多维度对比</h5>
                <VChart class="bar-chart" :option="barOptions" autoresize />
              </div>
              <div class="chart-item">
                <h5>建议比例</h5>
                <VChart class="pie-chart" :option="pieOptions" autoresize />
              </div>
            </div>

            <!-- Detailed Analysis -->
            <div class="analysis-row">
              <div class="analysis-card考研">
                <div class="analysis-header">
                  <el-icon :size="20" color="#667eea"><School /></el-icon>
                  <span>考研分析</span>
                </div>
                <ul class="analysis-list">
                  <li v-for="(item, index) in resultData.详细分析.考研" :key="index">
                    {{ item }}
                  </li>
                </ul>
              </div>

              <div class="analysis-card就业">
                <div class="analysis-header">
                  <el-icon :size="20" color="#22c55e"><Briefcase /></el-icon>
                  <span>就业分析</span>
                </div>
                <ul class="analysis-list">
                  <li v-for="(item, index) in resultData.详细分析.就业" :key="index">
                    {{ item }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty description="请填写上方表单，点击开始分析获取决策建议">
          <template #image>
            <el-icon :size="80" color="#d1d5db"><ScaleToOriginal /></el-icon>
          </template>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-decision-page {
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

.decision-content {
  display: grid;
  grid-template-columns: 350px 1fr;
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

.decision-form {
  margin-top: 16px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.recommendation-banner {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-radius: 12px;
}

.recommendation-text h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.recommendation-text p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-item {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
}

.chart-item h5 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.bar-chart {
  height: 250px;
}

.pie-chart {
  height: 250px;
}

.analysis-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.analysis-card考研,
.analysis-card就业 {
  padding: 16px;
  border-radius: 12px;
}

.analysis-card考研 {
  background: rgba(102, 126, 234, 0.08);
}

.analysis-card就业 {
  background: rgba(34, 197, 94, 0.08);
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.analysis-list {
  margin: 0;
  padding-left: 20px;
}

.analysis-list li {
  font-size: 13px;
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
  .decision-content {
    grid-template-columns: 1fr;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .analysis-row {
    grid-template-columns: 1fr;
  }
}
</style>
