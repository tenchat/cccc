<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { request } from '@/api/index'

const router = useRouter()

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'student' as 'student' | 'school_admin' | 'company_admin'
})

const loading = ref(false)

const roleOptions = [
  { value: 'student', label: '学生' },
  { value: 'school_admin', label: '学校' },
  { value: 'company_admin', label: '企业' }
]

const handleRegister = async () => {
  if (!registerForm.value.username) {
    ElMessage.warning('请输入用户名')
    return
  }

  if (!registerForm.value.password) {
    ElMessage.warning('请输入密码')
    return
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  if (registerForm.value.password.length < 6) {
    ElMessage.warning('密码长度至少为6位')
    return
  }

  loading.value = true
  try {
    await request.post('/auth/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      role: registerForm.value.role
    })

    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch {
    // error handled by interceptor
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h1 class="register-title">创建账号</h1>
          <p class="register-subtitle">加入就业分析平台</p>
        </div>

        <el-form
          :model="registerForm"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item label="选择角色">
            <el-radio-group v-model="registerForm.role" class="role-group">
              <el-radio-button
                v-for="option in roleOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="registerForm.username"
              size="large"
              placeholder="请输入用户名"
              prefix-icon="User"
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="registerForm.password"
              type="password"
              size="large"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              size="large"
              placeholder="请确认密码"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="register-button"
              native-type="submit"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <span class="login-link">
            已有账号?
            <a @click="goToLogin">立即登录</a>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
}

.register-container {
  width: 100%;
  max-width: 480px;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: 14px;
  color: #64748b;
}

.register-form {
  margin-bottom: 24px;
}

.role-group {
  width: 100%;
  display: flex;
}

.role-group :deep(.el-radio-button__inner) {
  flex: 1;
  text-align: center;
}

.register-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
}

.register-footer {
  text-align: center;
}

.login-link {
  color: #64748b;
  font-size: 14px;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
}

.login-link a:hover {
  text-decoration: underline;
}

:deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 12px 16px;
}

:deep(.el-input__inner) {
  font-size: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #1e293b;
}
</style>
