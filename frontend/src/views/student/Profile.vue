<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()

const activeTab = ref('basic')

const basicInfo = reactive({
  realName: '张三',
  gender: 'male',
  birthday: '2002-01-15',
  phone: '13800138000',
  email: 'zhangsan@example.com',
  province: '浙江省',
  city: '杭州市'
})

const jobIntention = reactive({
 期望城市: '杭州',
  期望薪资: '20K-30K',
  工作类型: '全职',
  行业偏好: '互联网',
  岗位偏好: '前端开发'
})

const resumeFile = ref<File | null>(null)

const basicRules: FormRules = {
  realName: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ]
}

const submitBasicInfo = async () => {
  if (!formRef.value) return

  await formRef.value.validate((valid) => {
    if (valid) {
      ElMessage.success('基本信息保存成功')
    }
  })
}

const submitIntention = () => {
  ElMessage.success('求职意向保存成功')
}
</script>

<template>
  <div class="profile-page">
    <div class="page-header">
      <h2>档案管理</h2>
      <p class="page-desc">完善您的个人信息，提高就业匹配度</p>
    </div>

    <div class="profile-content">
      <el-tabs v-model="activeTab" class="profile-tabs">
        <!-- Basic Info Tab -->
        <el-tab-pane label="基本信息" name="basic">
          <div class="tab-content">
            <el-card shadow="never">
              <template #header>
                <div class="card-header">
                  <span>基本信息</span>
                </div>
              </template>
              <el-form
                ref="formRef"
                :model="basicInfo"
                :rules="basicRules"
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="姓名" prop="realName">
                  <el-input v-model="basicInfo.realName" placeholder="请输入姓名" />
                </el-form-item>

                <el-form-item label="性别" prop="gender">
                  <el-radio-group v-model="basicInfo.gender">
                    <el-radio label="male">男</el-radio>
                    <el-radio label="female">女</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="出生日期" prop="birthday">
                  <el-date-picker
                    v-model="basicInfo.birthday"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                  />
                </el-form-item>

                <el-form-item label="手机号" prop="phone">
                  <el-input v-model="basicInfo.phone" placeholder="请输入手机号" />
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="basicInfo.email" placeholder="请输入邮箱" />
                </el-form-item>

                <el-form-item label="省份" prop="province">
                  <el-input v-model="basicInfo.province" placeholder="请输入省份" />
                </el-form-item>

                <el-form-item label="城市" prop="city">
                  <el-input v-model="basicInfo.city" placeholder="请输入城市" />
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="submitBasicInfo">保存</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
        </el-tab-pane>

        <!-- Job Intention Tab -->
        <el-tab-pane label="求职意向" name="intention">
          <div class="tab-content">
            <el-card shadow="never">
              <template #header>
                <div class="card-header">
                  <span>求职意向</span>
                </div>
              </template>
              <el-form
                :model="jobIntention"
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="期望城市">
                  <el-input v-model="jobIntention.期望城市" placeholder="请输入期望城市" />
                </el-form-item>

                <el-form-item label="期望薪资">
                  <el-select v-model="jobIntention.期望薪资" placeholder="请选择" style="width: 100%">
                    <el-option label="10K-15K" value="10K-15K" />
                    <el-option label="15K-20K" value="15K-20K" />
                    <el-option label="20K-30K" value="20K-30K" />
                    <el-option label="30K-40K" value="30K-40K" />
                    <el-option label="40K以上" value="40K以上" />
                  </el-select>
                </el-form-item>

                <el-form-item label="工作类型">
                  <el-radio-group v-model="jobIntention.工作类型">
                    <el-radio label="全职">全职</el-radio>
                    <el-radio label="实习">实习</el-radio>
                    <el-radio label="兼职">兼职</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="行业偏好">
                  <el-input v-model="jobIntention.行业偏好" placeholder="请输入行业偏好" />
                </el-form-item>

                <el-form-item label="岗位偏好">
                  <el-input v-model="jobIntention.岗位偏好" placeholder="请输入岗位偏好" />
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="submitIntention">保存</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
        </el-tab-pane>

        <!-- Resume Upload Tab -->
        <el-tab-pane label="简历上传" name="resume">
          <div class="tab-content">
            <el-card shadow="never">
              <template #header>
                <div class="card-header">
                  <span>简历上传</span>
                </div>
              </template>
              <div class="upload-area">
                <el-upload
                  class="resume-uploader"
                  drag
                  action="#"
                  :auto-upload="false"
                  :on-change="(file: File) => resumeFile = file"
                  :limit="1"
                >
                  <el-icon class="upload-icon"><UploadFilled /></el-icon>
                  <div class="upload-text">
                    <span class="upload-title">拖拽简历到此处</span>
                    <span class="upload-desc">或点击上传</span>
                  </div>
                  <template #tip>
                    <div class="upload-tip">
                      支持 PDF、Word 格式，文件大小不超过 5MB
                    </div>
                  </template>
                </el-upload>

                <div class="upload-actions">
                  <el-button type="primary" :disabled="!resumeFile">上传简历</el-button>
                  <el-button>使用AI优化简历</el-button>
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
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

.profile-tabs {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.tab-content {
  padding: 20px 0;
}

.card-header {
  font-weight: 600;
  color: #1e293b;
}

.profile-form {
  max-width: 500px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.resume-uploader {
  width: 100%;
  max-width: 500px;
}

:deep(.el-upload-dragger) {
  padding: 40px;
  border-radius: 16px;
}

.upload-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 16px;
}

.upload-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.upload-title {
  font-size: 16px;
  font-weight: 500;
  color: #1e293b;
}

.upload-desc {
  font-size: 14px;
  color: #64748b;
}

.upload-tip {
  margin-top: 12px;
  font-size: 12px;
  color: #64748b;
}

.upload-actions {
  display: flex;
  gap: 12px;
}
</style>
