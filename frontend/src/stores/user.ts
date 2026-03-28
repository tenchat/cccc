import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface UserState {
  accountId: string
  username: string
  realName: string
  avatar: string
  roles: string[]
  token: string | null
}

export const useUserStore = defineStore('user', () => {
  // State
  const accountId = ref('')
  const username = ref('')
  const realName = ref('')
  const avatar = ref('')
  const roles = ref<string[]>([])
  const token = ref<string | null>(null)

  // Getters
  const isLoggedIn = () => !!token.value

  const isStudent = () => roles.value.includes('student')
  const isSchool = () => roles.value.includes('school')
  const isAdmin = () => roles.value.includes('admin')
  const isCompany = () => roles.value.includes('company')

  const primaryRole = () => roles.value[0] || ''

  // Actions
  const setUser = (user: Partial<UserState>) => {
    if (user.accountId !== undefined) accountId.value = user.accountId
    if (user.username !== undefined) username.value = user.username
    if (user.realName !== undefined) realName.value = user.realName
    if (user.avatar !== undefined) avatar.value = user.avatar
    if (user.roles !== undefined) roles.value = user.roles
    if (user.token !== undefined) token.value = user.token
  }

  const setToken = (newToken: string) => {
    token.value = newToken
  }

  const setRoles = (newRoles: string[]) => {
    roles.value = newRoles
  }

  const logout = () => {
    accountId.value = ''
    username.value = ''
    realName.value = ''
    avatar.value = ''
    roles.value = []
    token.value = null
  }

  // Initialize with mock data for development
  const initMockUser = () => {
    accountId.value = '1'
    username.value = 'student01'
    realName.value = '张三'
    avatar.value = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
    roles.value = ['student']
    token.value = 'mock-token-12345'
  }

  return {
    // State
    accountId,
    username,
    realName,
    avatar,
    roles,
    token,
    // Getters
    isLoggedIn,
    isStudent,
    isSchool,
    isAdmin,
    isCompany,
    primaryRole,
    // Actions
    setUser,
    setToken,
    setRoles,
    logout,
    initMockUser
  }
})
