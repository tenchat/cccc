import { get, post, setAuthToken, clearAuthToken } from './request'
import type { LoginParams, LoginResponse, UserInfo } from '@/types'

export const login = (data: LoginParams) => {
  return post<LoginResponse>('/auth/login', data).then((res) => {
    // Store token after successful login
    if (res.access_token) {
      setAuthToken(res.access_token)
    }
    return res
  })
}

export const logout = () => {
  return post<void>('/auth/logout').finally(() => {
    clearAuthToken()
  })
}

export const getCurrentUser = () => {
  return get<UserInfo>('/auth/user')
}

export const refreshToken = () => {
  return post<{ access_token: string }>('/auth/refresh')
}
