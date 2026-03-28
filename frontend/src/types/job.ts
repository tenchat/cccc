// Job description types
export interface JobDescription {
  jd_no: string
  company_id: string
  jd_title: string
  city: string
  industry?: string
  min_salary?: number
  max_salary?: number
  require_nums?: number
  min_edu_level?: number
  min_years?: string
  job_description?: string
  key_words?: string
  status: number
  apply_count?: number
}

export interface JobApplication {
  jd_no: string
  student_id: string
  apply_time?: string
  status?: number
}
