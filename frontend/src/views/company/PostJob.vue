<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()
const loading = ref(false)
const editMode = ref(false)

const formData = reactive({
  title: '',
  city: '',
  district: '',
  salaryMin: 0,
  salaryMax: 0,
  experience: '',
  education: '',
  jobType: 'fulltime',
  industry: '',
  description: '',
  requirements: '',
  skills: [] as string[],
  benefits: ''
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
  city: [{ required: true, message: '请选择城市', trigger: 'change' }],
  salaryMin: [{ required: true, message: '请输入最低薪资', trigger: 'blur' }],
  salaryMax: [{ required: true, message: '请输入最高薪资', trigger: 'blur' }],
  experience: [{ required: true, message: '请选择经验要求', trigger: 'change' }],
  education: [{ required: true, message: '请选择学历要求', trigger: 'change' }],
  description: [{ required: true, message: '请输入职位描述', trigger: 'blur' }]
}

const experienceOptions = [
  { value: '不限', label: '经验不限' },
  { value: '1年以下', label: '1年以下' },
  { value: '1-3年', label: '1-3年' },
  { value: '3-5年', label: '3-5年' },
  { value: '5-10年', label: '5-10年' },
  { value: '10年以上', label: '10年以上' }
]

const educationOptions = [
  { value: '不限', label: '学历不限' },
  { value: '高中/中专', label: '高中/中专' },
  { value: '大专', label: '大专' },
  { value: '本科', label: '本科' },
  { value: '硕士', label: '硕士' },
  { value: '博士', label: '博士' }
]

const jobTypeOptions = [
  { value: 'fulltime', label: '全职' },
  { value: 'parttime', label: '兼职' },
  { value: 'intern', label: '实习' }
]

const industryOptions = [
  { value: '互联网', label: '互联网' },
  { value: '金融', label: '金融' },
  { value: '教育', label: '教育' },
  { value: '医疗', label: '医疗' },
  { value: '房地产', label: '房地产' },
  { value: '其他', label: '其他' }
]

const skillOptions = ['Vue', 'React', 'Angular', 'Node.js', 'Java', 'Python', 'Go', 'TypeScript', 'JavaScript', 'CSS', 'HTML5']

const handleSkillChange = (val: string[]) => {
  formData.skills = val
}

const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        ElMessage.success(editMode.value ? '岗位信息已更新' : '岗位发布成功')
        loading.value = false
      }, 1000)
    }
  })
}

const saveDraft = () => {
  ElMessage.info('草稿保存成功')
}
</script>

<template>
  <div class="post-job-page">
    <div class="page-header">
      <h2>{{ editMode ? '编辑岗位' : '发布岗位' }}</h2>
      <p class="page-desc">填写岗位信息，发布招聘信息</p>
    </div>

    <div class="form-card">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
        class="job-form"
      >
        <!-- Basic Info -->
        <div class="form-section">
          <h3>基本信息</h3>

          <el-form-item label="职位名称" prop="title">
            <el-input v-model="formData.title" placeholder="如：前端开发工程师" />
          </el-form-item>

          <el-form-item label="工作城市" prop="city">
            <div class="city-select">
              <el-select v-model="formData.city" placeholder="选择城市" style="width: 48%">
                <el-option label="北京" value="北京" />
                <el-option label="上海" value="上海" />
                <el-option label="广州" value="广州" />
                <el-option label="深圳" value="深圳" />
                <el-option label="杭州" value="杭州" />
                <el-option label="南京" value="南京" />
                <el-option label="成都" value="成都" />
                <el-option label="武汉" value="武汉" />
              </el-select>
              <el-select v-model="formData.district" placeholder="选择区/县" style="width: 48%">
                <el-option label="朝阳区" value="朝阳区" />
                <el-option label="海淀区" value="海淀区" />
                <el-option label="浦东新区" value="浦东新区" />
              </el-select>
            </div>
          </el-form-item>

          <el-form-item label="薪资范围" prop="salaryMin">
            <div class="salary-input">
              <el-input-number v-model="formData.salaryMin" :min="0" :step="1000" />
              <span class="separator">-</span>
              <el-input-number v-model="formData.salaryMax" :min="0" :step="1000" />
              <span class="unit">元/月</span>
            </div>
          </el-form-item>

          <el-form-item label="经验要求" prop="experience">
            <el-select v-model="formData.experience" placeholder="请选择" style="width: 100%">
              <el-option
                v-for="opt in experienceOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="学历要求" prop="education">
            <el-select v-model="formData.education" placeholder="请选择" style="width: 100%">
              <el-option
                v-for="opt in educationOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="工作类型" prop="jobType">
            <el-radio-group v-model="formData.jobType">
              <el-radio
                v-for="opt in jobTypeOptions"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.label }}
              </el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="所属行业" prop="industry">
            <el-select v-model="formData.industry" placeholder="请选择" style="width: 100%">
              <el-option
                v-for="opt in industryOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
          </el-form-item>
        </div>

        <!-- Job Description -->
        <div class="form-section">
          <h3>职位描述</h3>

          <el-form-item label="职位描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="5"
              placeholder="请详细描述岗位职责和工作内容"
            />
          </el-form-item>

          <el-form-item label="任职要求" prop="requirements">
            <el-input
              v-model="formData.requirements"
              type="textarea"
              :rows="5"
              placeholder="请详细描述任职要求"
            />
          </el-form-item>
        </div>

        <!-- Skills -->
        <div class="form-section">
          <h3>技能要求</h3>

          <el-form-item label="技能标签">
            <el-checkbox-group
              :value="formData.skills"
              @change="handleSkillChange"
            >
              <el-checkbox
                v-for="skill in skillOptions"
                :key="skill"
                :label="skill"
              >
                {{ skill }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>

        <!-- Benefits -->
        <div class="form-section">
          <h3>福利待遇</h3>

          <el-form-item label="福利待遇">
            <el-input
              v-model="formData.benefits"
              type="textarea"
              :rows="3"
              placeholder="请描述公司福利，如：五险一金、带薪年假、弹性工作等"
            />
          </el-form-item>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <el-button @click="saveDraft">保存草稿</el-button>
          <el-button type="primary" :loading="loading" @click="submitForm">
            {{ editMode ? '更新岗位' : '发布岗位' }}
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.post-job-page {
  max-width: 800px;
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

.form-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.job-form {
  max-width: 600px;
}

.form-section {
  margin-bottom: 40px;
}

.form-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.city-select {
  display: flex;
  gap: 4%;
}

.salary-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.separator {
  color: #64748b;
}

.unit {
  color: #64748b;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

:deep(.el-input-number) {
  width: 130px;
}

:deep(.el-checkbox) {
  margin-right: 16px;
  margin-bottom: 8px;
}
</style>
