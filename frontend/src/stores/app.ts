import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useUserStore } from './user'

export interface MenuItem {
  title: string
  icon: string
  path: string
  children?: MenuItem[]
}

export interface AppState {
  sidebarCollapsed: boolean
  sidebarMenus: MenuItem[]
}

// Role-based menu configuration
const roleMenus: Record<string, MenuItem[]> = {
  student: [
    { title: '个人首页', icon: 'HomeFilled', path: '/student/dashboard' },
    { title: '档案管理', icon: 'User', path: '/student/profile' },
    { title: '岗位推荐', icon: 'Briefcase', path: '/student/jobs' },
    { title: 'AI就业画像', icon: 'Cpu', path: '/student/ai-profile' },
    { title: 'AI简历优化', icon: 'Document', path: '/student/ai-resume' },
    { title: '考研vs就业', icon: 'ScaleToOriginal', path: '/student/ai-decision' }
  ],
  school: [
    { title: '就业概况', icon: 'DataAnalysis', path: '/school/dashboard' },
    { title: '学生管理', icon: 'User', path: '/school/students' },
    { title: '就业预警', icon: 'Warning', path: '/school/warnings' },
    { title: '数据大屏', icon: 'Monitor', path: '/school/databoard' }
  ],
  admin: [
    { title: '管理首页', icon: 'HomeFilled', path: '/admin/dashboard' },
    { title: '统计分析', icon: 'DataAnalysis', path: '/admin/statistics' },
    { title: '学院就业率', icon: 'OfficeBuilding', path: '/admin/colleges' },
    { title: '稀缺人才', icon: 'Star', path: '/admin/scarce-talents' },
    { title: '数据大屏', icon: 'Monitor', path: '/admin/databoard' }
  ],
  company: [
    { title: '招聘概况', icon: 'DataAnalysis', path: '/company/dashboard' },
    { title: '岗位管理', icon: 'Briefcase', path: '/company/jobs' },
    { title: '发布岗位', icon: 'Plus', path: '/company/post-job' }
  ]
}

export const useAppStore = defineStore('app', () => {
  // State
  const sidebarCollapsed = ref(false)
  const sidebarMenus = ref<MenuItem[]>([])

  // Getters
  const isCollapsed = computed(() => sidebarCollapsed.value)

  const currentRoleMenus = computed(() => {
    const userStore = useUserStore()
    const role = userStore.primaryRole()
    return roleMenus[role] || []
  })

  // Actions
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setSidebarCollapsed = (collapsed: boolean) => {
    sidebarCollapsed.value = collapsed
  }

  const setSidebarMenus = (menus: MenuItem[]) => {
    sidebarMenus.value = menus
  }

  const loadMenusByRole = () => {
    const userStore = useUserStore()
    const role = userStore.primaryRole()
    sidebarMenus.value = roleMenus[role] || []
  }

  return {
    // State
    sidebarCollapsed,
    sidebarMenus,
    // Getters
    isCollapsed,
    currentRoleMenus,
    // Actions
    toggleSidebar,
    setSidebarCollapsed,
    setSidebarMenus,
    loadMenusByRole
  }
})
