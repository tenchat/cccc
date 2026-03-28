import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios'
import { ElMessage } from 'element-plus'

const BASE_URL = '/api/v1'
const TIMEOUT = 10000

// Token keys in localStorage
const TOKEN_KEY = 'token'
const TOKEN_TYPE = 'Bearer'

// Create axios instance
const request: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT
})

// Get token from localStorage
const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY)
}

// Set token to localStorage
const setToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token)
}

// Remove token from localStorage
const removeToken = (): void => {
  localStorage.removeItem(TOKEN_KEY)
}

// Request interceptor
request.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `${TOKEN_TYPE} ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response) => {
    const res = response.data

    // Handle API response format
    if (res.code !== undefined) {
      if (res.code === 200 || res.code === 0) {
        return res.data !== undefined ? res.data : res
      }
      // Handle error code
      ElMessage.error(res.message || 'Request failed')
      return Promise.reject(new Error(res.message || 'Request failed'))
    }

    // If no standard response format, return directly
    return res
  },
  (error: AxiosError) => {
    const status = error.response?.status
    let message = error.message

    if (error.response?.data) {
      const data = error.response.data as any
      message = data.message || data.msg || message
    }

    switch (status) {
      case 401:
        ElMessage.error('Authentication expired, please login again')
        removeToken()
        window.location.href = '/login'
        break
      case 403:
        ElMessage.error('Access denied')
        break
      case 404:
        ElMessage.error('Resource not found')
        break
      case 500:
        ElMessage.error('Server error')
        break
      default:
        if (message) {
          ElMessage.error(message)
        }
    }

    return Promise.reject(error)
  }
)

// Export request methods with type safety
export interface RequestConfig<T = any> extends AxiosRequestConfig {
  params?: T
  data?: T
}

export const get = <T = any>(url: string, config?: RequestConfig): Promise<T> => {
  return request.get(url, config)
}

export const post = <T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> => {
  return request.post(url, data, config)
}

export const put = <T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> => {
  return request.put(url, data, config)
}

export const del = <T = any>(url: string, config?: RequestConfig): Promise<T> => {
  return request.delete(url, config)
}

export const patch = <T = any>(url: string, data?: any, config?: RequestConfig): Promise<T> => {
  return request.patch(url, data, config)
}

// Export utility functions
export const setAuthToken = setToken
export const clearAuthToken = removeToken

export default request
