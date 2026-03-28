<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

const router = useRouter()

const loginForm = ref({
  username: '',
  password: '',
  remember: false
})

const loading = ref(false)

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res = await login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })

    localStorage.setItem('token', res.access_token)
    localStorage.setItem('user', JSON.stringify(res.user))

    ElMessage.success('登录成功')

    // 根据用户角色跳转
    const roles = res.user.roles
    if (roles.includes('admin')) {
      router.push('/admin/dashboard')
    } else if (roles.includes('school_admin') || roles.includes('school_viewer')) {
      router.push('/school/dashboard')
    } else if (roles.includes('company_admin') || roles.includes('company_recruiter')) {
      router.push('/company/dashboard')
    } else {
      router.push('/student/dashboard')
    }
  } catch {
    // error handled by interceptor
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1 class="login-title">欢迎回来</h1>
          <p class="login-subtitle">登录到就业分析平台</p>
        </div>

        <el-form
          :model="loginForm"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item>
            <el-input
              v-model="loginForm.username"
              size="large"
              placeholder="请输入用户名"
              prefix-icon="User"
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="loginForm.password"
              type="password"
              size="large"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <div class="form-options">
              <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-button"
              native-type="submit"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <span class="register-link">
            还没有账号?
            <a @click="goToRegister">立即注册</a>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
}

.login-container {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 14px;
  color: #64748b;
}

.login-form {
  margin-bottom: 24px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
}

.login-footer {
  text-align: center;
}

.register-link {
  color: #64748b;
  font-size: 14px;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
}

.register-link a:hover {
  text-decoration: underline;
}

:deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 12px 16px;
}

:deep(.el-input__inner) {
  font-size: 16px;
}
</style>
