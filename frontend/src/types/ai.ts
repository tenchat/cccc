// AI service types
export interface EmploymentProfileRequest {
  major: string
  gpa: number
  skills: string[]
  target_city: string
  internship?: string
}

export interface EmploymentProfileResponse {
  score: number
  professional_match: number
  skill_match: number
  location_demand: number
  salary_expectation: number
  strengths: string
  weaknesses: string
  suggestions: string
}

export interface JobRecommendationRequest {
  student_id: string
  top_n?: number
}

export interface JobRecommendation {
  jd_no: string
  jd_title: string
  company_id: string
  company_name?: string
  city: string
  min_salary?: number
  max_salary?: number
  match_score: number
}

export interface JobRecommendationResponse {
  recommendations: JobRecommendation[]
  total: number
}

export interface SkillPathRequest {
  target_position: string
  current_skills: string[]
}

export interface SkillPathResponse {
  skill_path: string[]
  learning_resources: {
    skill: string
    resource: string
  }[]
  estimated_time: string
}

export interface WarningRequest {
  student_id?: string
  college?: string
  threshold?: number
}

export interface WarningStudent {
  student_id: string
  student_name: string
  college: string
  major: string
  warning_type: string
  warning_level: 'high' | 'medium' | 'low'
  suggestion: string
}

export interface WarningResponse {
  warnings: WarningStudent[]
  total: number
}
