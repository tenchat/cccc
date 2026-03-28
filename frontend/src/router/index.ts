import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { RoleLayout } from '@/layout'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomePage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },

  // Student Routes
  {
    path: '/student',
    component: RoleLayout,
    meta: { roles: ['student'] },
    children: [
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/Dashboard.vue')
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/student/Profile.vue')
      },
      {
        path: 'jobs',
        name: 'StudentJobs',
        component: () => import('@/views/student/Jobs.vue')
      },
      {
        path: 'ai-profile',
        name: 'StudentAIProfile',
        component: () => import('@/views/student/AIProfile.vue')
      },
      {
        path: 'ai-resume',
        name: 'StudentAIResume',
        component: () => import('@/views/student/AIResume.vue')
      },
      {
        path: 'ai-decision',
        name: 'StudentAIDecision',
        component: () => import('@/views/student/AIDecision.vue')
      }
    ]
  },

  // School Routes
  {
    path: '/school',
    component: RoleLayout,
    meta: { roles: ['school_admin', 'school_viewer'] },
    children: [
      {
        path: 'dashboard',
        name: 'SchoolDashboard',
        component: () => import('@/views/school/Dashboard.vue')
      },
      {
        path: 'students',
        name: 'SchoolStudents',
        component: () => import('@/views/school/Students.vue')
      },
      {
        path: 'warnings',
        name: 'SchoolWarnings',
        component: () => import('@/views/school/Warnings.vue')
      },
      {
        path: 'databoard',
        name: 'SchoolDataBoard',
        component: () => import('@/views/school/DataBoard.vue')
      }
    ]
  },

  // Admin Routes
  {
    path: '/admin',
    component: RoleLayout,
    meta: { roles: ['admin'] },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue')
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue')
      },
      {
        path: 'colleges',
        name: 'AdminColleges',
        component: () => import('@/views/admin/Colleges.vue')
      },
      {
        path: 'scarce-talents',
        name: 'AdminScarceTalents',
        component: () => import('@/views/admin/ScarceTalents.vue')
      },
      {
        path: 'databoard',
        name: 'AdminDataBoard',
        component: () => import('@/views/admin/DataBoard.vue')
      }
    ]
  },

  // Company Routes
  {
    path: '/company',
    component: RoleLayout,
    meta: { roles: ['company_admin', 'company_recruiter'] },
    children: [
      {
        path: 'dashboard',
        name: 'CompanyDashboard',
        component: () => import('@/views/company/Dashboard.vue')
      },
      {
        path: 'jobs',
        name: 'CompanyJobs',
        component: () => import('@/views/company/Jobs.vue')
      },
      {
        path: 'post-job',
        name: 'CompanyPostJob',
        component: () => import('@/views/company/PostJob.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
