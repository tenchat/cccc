<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()

onMounted(() => {
  if (!userStore.isLoggedIn()) {
    userStore.initMockUser()
  }
})

interface MenuItem {
  path: string
  label: string
  icon: string
}

const studentMenus: MenuItem[] = [
  { path: '/student/dashboard', label: '个人首页', icon: 'HomeFilled' },
  { path: '/student/profile', label: '档案管理', icon: 'User' },
  { path: '/student/jobs', label: '岗位推荐', icon: 'Briefcase' },
  { path: '/student/ai-profile', label: 'AI就业画像', icon: 'Cpu' },
  { path: '/student/ai-resume', label: 'AI简历优化', icon: 'Document' },
  { path: '/student/ai-decision', label: '考研vs就业', icon: 'TrendCharts' }
]

const schoolMenus: MenuItem[] = [
  { path: '/school/dashboard', label: '就业概况', icon: 'DataAnalysis' },
  { path: '/school/students', label: '学生管理', icon: 'User' },
  { path: '/school/warnings', label: '就业预警', icon: 'Warning' },
  { path: '/school/databoard', label: '数据大屏', icon: 'Monitor' }
]

const adminMenus: MenuItem[] = [
  { path: '/admin/dashboard', label: '管理首页', icon: 'HomeFilled' },
  { path: '/admin/statistics', label: '统计分析', icon: 'DataAnalysis' },
  { path: '/admin/colleges', label: '学院就业率', icon: 'OfficeBuilding' },
  { path: '/admin/scarce-talents', label: '稀缺人才', icon: 'Star' },
  { path: '/admin/databoard', label: '数据大屏', icon: 'Monitor' }
]

const companyMenus: MenuItem[] = [
  { path: '/company/dashboard', label: '招聘概况', icon: 'DataAnalysis' },
  { path: '/company/jobs', label: '岗位管理', icon: 'Briefcase' },
  { path: '/company/post-job', label: '发布岗位', icon: 'Plus' }
]

const currentMenus = computed(() => {
  const path = route.path
  if (path.startsWith('/student')) return studentMenus
  if (path.startsWith('/school')) return schoolMenus
  if (path.startsWith('/admin')) return adminMenus
  if (path.startsWith('/company')) return companyMenus
  return []
})

const roleTitle = computed(() => {
  const path = route.path
  if (path.startsWith('/student')) return '学生端'
  if (path.startsWith('/school')) return '学校端'
  if (path.startsWith('/admin')) return '管理端'
  if (path.startsWith('/company')) return '企业端'
  return ''
})

const isCollapsed = computed(() => appStore.isCollapsed)

const toggleCollapse = () => {
  appStore.toggleSidebar()
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/')
  } catch {
    // cancelled
  }
}
</script>

<template>
  <aside class="app-sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <el-icon v-if="!isCollapsed" :size="24" color="#667eea">
        <DataAnalysis />
      </el-icon>
      <span v-if="!isCollapsed" class="sidebar-title">{{ roleTitle }}</span>
      <el-icon v-else :size="20" color="#667eea">
        <DataAnalysis />
      </el-icon>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="menu in currentMenus"
        :key="menu.path"
        :to="menu.path"
        class="nav-item"
        :class="{ active: route.path === menu.path }"
      >
        <el-icon :size="20">
          <component :is="menu.icon" />
        </el-icon>
        <span v-if="!isCollapsed" class="nav-label">{{ menu.label }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <el-button
        class="collapse-btn"
        text
        @click="toggleCollapse"
      >
        <el-icon :size="18">
          <Fold v-if="!isCollapsed" />
          <Expand v-else />
        </el-icon>
        <span v-if="!isCollapsed">收起</span>
      </el-button>
      <el-button
        class="logout-btn"
        text
        @click="handleLogout"
      >
        <el-icon :size="18"><SwitchButton /></el-icon>
        <span v-if="!isCollapsed">退出登录</span>
      </el-button>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: 240px;
  height: 100%;
  background: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: sticky;
  top: 0;
  height: 100vh;
}

.app-sidebar.collapsed {
  width: 72px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.sidebar-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.collapse-btn,
.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.collapse-btn:hover {
  color: #667eea;
  background: #f1f5f9;
}

.logout-btn:hover {
  color: #ef4444;
}

.app-sidebar.collapsed .nav-label,
.app-sidebar.collapsed .sidebar-title {
  display: none;
}

.app-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
}
</style>
