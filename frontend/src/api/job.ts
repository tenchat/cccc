import { get, post, put, del } from './request'
import type { JobDescription, PaginatedResponse, PaginationParams } from '@/types'

export interface JobListParams extends PaginationParams {
  city?: string
  industry?: string
  min_salary?: number
  max_salary?: number
  min_edu_level?: number
  status?: number
  keyword?: string
}

export interface ApplyJobData {
  jd_no: string
  resume_url?: string
  cover_letter?: string
}

export const getJobList = (params: JobListParams) => {
  return get<PaginatedResponse<JobDescription>>('/jobs', { params })
}

export const getJobDetail = (jdNo: string) => {
  return get<JobDescription>(`/jobs/${jdNo}`)
}

export const createJob = (data: Partial<JobDescription>) => {
  return post<JobDescription>('/jobs', data)
}

export const updateJob = (jdNo: string, data: Partial<JobDescription>) => {
  return put<JobDescription>(`/jobs/${jdNo}`, data)
}

export const deleteJob = (jdNo: string) => {
  return del<void>(`/jobs/${jdNo}`)
}

export const applyJob = (data: ApplyJobData) => {
  return post<void>('/jobs/apply', data)
}

export const getMyApplications = (params: PaginationParams) => {
  return get<PaginatedResponse<JobDescription>>('/jobs/my-applications', { params })
}
