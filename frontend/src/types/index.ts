// Base API types
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

export interface PaginationParams {
  page: number
  pageSize: number
}

export interface PaginatedResponse<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// Auth types
export * from './auth'
export type { LoginParams, LoginResponse, UserInfo } from './auth'

// Student types
export * from './student'
export type { StudentProfile, ImportResult } from './student'

// Job types
export * from './job'
export type { JobDescription, JobApplication } from './job'

// Statistics types
export * from './statistics'
export type { StatisticsSummary, CollegeStatistics, MajorStatistics, ProvinceStatistics } from './statistics'

// AI types
export * from './ai'
export type {
  EmploymentProfileRequest,
  EmploymentProfileResponse,
  JobRecommendationRequest,
  JobRecommendation,
  JobRecommendationResponse,
  SkillPathRequest,
  SkillPathResponse,
  WarningRequest,
  WarningStudent,
  WarningResponse
} from './ai'
