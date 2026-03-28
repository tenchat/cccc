import { post } from './request'
import type {
  EmploymentProfileRequest,
  EmploymentProfileResponse,
  JobRecommendationRequest,
  JobRecommendationResponse,
  SkillPathRequest,
  SkillPathResponse,
  WarningRequest,
  WarningResponse
} from '@/types'

export const getEmploymentProfile = (data: EmploymentProfileRequest) => {
  return post<EmploymentProfileResponse>('/ai/employment-profile', data)
}

export const getJobRecommendation = (data: JobRecommendationRequest) => {
  return post<JobRecommendationResponse>('/ai/job-recommendation', data)
}

export const getSkillPath = (data: SkillPathRequest) => {
  return post<SkillPathResponse>('/ai/skill-path', data)
}

export const generateWarning = (data?: WarningRequest) => {
  return post<WarningResponse>('/ai/warning', data || {})
}

export const analyzeResume = (resumeUrl: string) => {
  return post<{
    skills: string[]
    experience: string[]
    education: string[]
    summary: string
  }>('/ai/analyze-resume', { resume_url: resumeUrl })
}

export const compareOptions = (data: {
  option_a: string
  option_b: string
  context: string
}) => {
  return post<{
    analysis: string
    recommendation: string
    pros_cons: {
      option_a: string[]
      option_b: string[]
    }
  }>('/ai/compare-options', data)
}
