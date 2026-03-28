import { get } from './request'
import type { StatisticsSummary, CollegeStatistics, MajorStatistics, ProvinceStatistics } from '@/types'

export interface StatisticsParams {
  graduation_year?: number
  college?: string
}

export const getSummary = (params?: StatisticsParams) => {
  return get<StatisticsSummary>('/statistics/summary', { params })
}

export const getByCollege = (params?: StatisticsParams) => {
  return get<CollegeStatistics[]>('/statistics/by-college', { params })
}

export const getByMajor = (params?: StatisticsParams) => {
  return get<MajorStatistics[]>('/statistics/by-major', { params })
}

export const getByProvince = (params?: StatisticsParams) => {
  return get<ProvinceStatistics[]>('/statistics/by-province', { params })
}

export const getTrendData = (params?: StatisticsParams & { years?: number }) => {
  return get<{ year: number; employment_rate: number; total: number }[]>('/statistics/trend', { params })
}

export const getIndustrySalary = (params?: StatisticsParams) => {
  return get<{ industry: string; avg_salary: number }[]>('/statistics/industry-salary', { params })
}
