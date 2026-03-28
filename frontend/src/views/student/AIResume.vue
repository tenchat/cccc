<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const resumeContent = ref(`张三
计算机科学与技术专业 本科
邮箱：zhangsan@example.com | 手机：13800138000

教育经历
2020 - 2024  XXX大学  计算机科学与技术  GPA 3.5/4.0

技能特长
- 熟练掌握 Vue、React 前端框架
- 熟悉 TypeScript、JavaScript 开发
- 了解 Node.js 后端开发
- 熟悉 Git 版本控制

项目经验
校园社交APP
- 使用 Vue + Node.js 开发
- 实现即时通讯、动态发布等功能

实习经历
2023.06 - 2023.09  前端开发实习生  XX科技公司
- 参与公司官网前端开发
- 使用 Vue 完成多个页面组件`)

const optimizedResume = ref('')
const loading = ref(false)
const hasOptimized = ref(false)

const optimizationOptions = reactive({
  语气风格: 'professional',
  重点突出: '技术能力',
  长度: '适中'
})

const toneOptions = [
  { value: 'professional', label: '专业正式' },
  { value: 'creative', label: '创新活泼' },
  { value: 'concise', label: '简洁有力' }
]

const highlightOptions = [
  { value: '技术能力', label: '技术能力' },
  { value: '项目经验', label: '项目经验' },
  { value: '实习经历', label: '实习经历' },
  { value: '学术成绩', label: '学术成绩' }
]

const lengthOptions = [
  { value: '简短', label: '简短' },
  { value: '适中', label: '适中' },
  { value: '详细', label: '详细' }
]

const optimizeResume = async () => {
  if (!resumeContent.value.trim()) {
    ElMessage.warning('请先输入简历内容')
    return
  }

  loading.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2500))

  // Mock optimized result
  optimizedResume.value = `【优化版简历】

张三
计算机科学与技术专业  |  本科  |  GPA 3.8/4.0 (专业前10%)
联系方式：13800138000 | zhangsan@example.com

━━━━━━━━━━━━━━━━━━━━━━━━

【专业技能】
✦ 前端开发：精通 Vue3、React，掌握 TypeScript，具备完整项目开发经验
✦ 后端技术：熟悉 Node.js、Express，了解 MongoDB 数据库操作
✦ 工程能力：熟练使用 Git、Webpack，了解 CI/CD 流程

【项目经验】

▸ 校园社交APP (2023.09 - 2024.01)
  技术栈：Vue3 + Node.js + MongoDB
  ▪ 从0到1独立开发，累计用户2000+
  ▪ 实现实时聊天、动态发布等功能，前端性能优化首屏加载<1s
  ▪ 负责前端架构设计及团队协作，推动项目如期上线

▸ 电商后台管理系统 (2023.06 - 2023.09)
  技术栈：Vue2 + Element UI + Axios
  ▪ 独立完成20+页面组件开发
  ▪ 封装通用请求模块，代码复用率提升40%

【实习经历】

XX科技公司 | 前端开发实习生 | 2023.06 - 2023.09
▪ 参与公司官网重构，使用 Vue 实现响应式页面开发
▪ 优化页面加载性能，Google PageSpeed 评分提升至95+
▪ 与产品、设计团队紧密协作，独立交付3个功能模块

【荣誉奖项】
▪ 2022-2023学年校级一等奖学金
▪ ACM 程序设计竞赛省级银奖
▪ 校级优秀学生干部`

  hasOptimized.value = true
  loading.value = false
  ElMessage.success('简历优化完成')
}

const downloadResume = () => {
  ElMessage.info('简历下载功能开发中')
}

const copyResume = () => {
  ElMessage.success('简历内容已复制到剪贴板')
}
</script>

<template>
  <div class="ai-resume-page">
    <div class="page-header">
      <h2>AI简历优化</h2>
      <p class="page-desc">上传您的简历，AI将为您提供专业的优化建议和改进版本</p>
    </div>

    <div class="resume-content">
      <div class="editor-section">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>原始简历</span>
              <el-button size="small" @click="resumeContent = ''">清空</el-button>
            </div>
          </template>
          <el-input
            v-model="resumeContent"
            type="textarea"
            :rows="20"
            placeholder="请粘贴您的简历内容..."
            class="resume-textarea"
          />
          <div class="editor-actions">
            <el-button type="primary" :loading="loading" @click="optimizeResume">
              AI 优化简历
            </el-button>
          </div>
        </el-card>
      </div>

      <div class="options-section">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>优化选项</span>
            </div>
          </template>
          <el-form label-width="80px" class="options-form">
            <el-form-item label="语气风格">
              <el-select v-model="optimizationOptions.语气风格" style="width: 100%">
                <el-option
                  v-for="opt in toneOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="重点突出">
              <el-select v-model="optimizationOptions.重点突出" style="width: 100%">
                <el-option
                  v-for="opt in highlightOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="简历长度">
              <el-select v-model="optimizationOptions.长度" style="width: 100%">
                <el-option
                  v-for="opt in lengthOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
          </el-form>

          <el-divider />

          <div class="tips-section">
            <h4>优化建议</h4>
            <ul class="tips-list">
              <li>使用强动词开头（如：独立完成、负责开发）</li>
              <li>量化成果数据（如：用户量2000+）</li>
              <li>突出技术栈和关键技能</li>
              <li>保持简洁，控制在1-2页</li>
            </ul>
          </div>
        </el-card>
      </div>

      <div class="result-section" v-if="hasOptimized">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>优化后简历</span>
              <div class="header-actions">
                <el-button size="small" @click="copyResume">
                  <el-icon><DocumentCopy /></el-icon>
                  复制
                </el-button>
                <el-button size="small" type="primary" @click="downloadResume">
                  <el-icon><Download /></el-icon>
                  下载
                </el-button>
              </div>
            </div>
          </template>
          <div class="optimized-resume">
            <pre>{{ optimizedResume }}</pre>
          </div>
        </el-card>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty description="优化后的简历将显示在这里">
          <template #image>
            <el-icon :size="80" color="#d1d5db"><Document /></el-icon>
          </template>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-resume-page {
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

.resume-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  grid-template-rows: auto auto;
  gap: 24px;
}

.editor-section {
  grid-row: 1;
}

.options-section {
  grid-row: 1;
}

.result-section {
  grid-column: 1 / -1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1e293b;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.resume-textarea :deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.editor-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.options-form {
  margin-bottom: 16px;
}

.tips-section {
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.tips-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.tips-list {
  margin: 0;
  padding-left: 20px;
}

.tips-list li {
  font-size: 13px;
  color: #64748b;
  line-height: 1.8;
}

.optimized-resume {
  background: #f8fafc;
  border-radius: 8px;
  padding: 24px;
  max-height: 500px;
  overflow-y: auto;
}

.optimized-resume pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
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
  .resume-content {
    grid-template-columns: 1fr;
  }

  .options-section {
    grid-row: 2;
  }

  .result-section {
    grid-row: 3;
  }
}
</style>
