// Student profile types
export interface StudentProfile {
  profile_id: number
  account_id: string
  student_id?: string
  university_id?: string
  college?: string
  major?: string
  degree?: string
  graduation_year?: number
  live_city?: string
  desire_city?: string
  desire_industry?: string
  desire_jd_type?: string
  desire_salary_id?: number
  cur_industry?: string
  cur_salary?: number
  experience?: string
  resume_url?: string
}

export interface ImportResult {
  total: number
  success: number
  failed: number
  errors?: string[]
}
