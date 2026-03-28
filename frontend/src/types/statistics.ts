// Statistics types
export interface StatisticsSummary {
  total: number
  employed: number
  unemployed: number
  further_study: number
  abroad: number
  employment_rate: number
}

export interface CollegeStatistics {
  college: string
  total: number
  employed: number
  employment_rate: number
}

export interface MajorStatistics {
  major: string
  total: number
  employed: number
  employment_rate: number
}

export interface ProvinceStatistics {
  province: string
  total: number
  employed: number
  employment_rate: number
}
