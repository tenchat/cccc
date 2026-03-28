// Re-export request utilities
export { default as request, get, post, put, del, patch, setAuthToken, clearAuthToken } from './request'
export type { RequestConfig } from './request'

// Re-export all types
export * from '@/types'

// ============ Dashboard API Types (local to frontend) ============
export interface DashboardStats {
  totalVisits: number
  activeUsers: number
  avgDuration: string
  conversionRate: number
  trends: {
    visitsTrend: string
    usersTrend: string
    durationTrend: string
    conversionTrend: string
  }
}

export interface VisitData {
  date: string
  value: number
}

export interface RegionData {
  region: string
  value: number
}

export interface TrafficSource {
  name: string
  value: number
}

export interface DashboardData {
  stats: DashboardStats
  visitTrend: VisitData[]
  regionDistribution: RegionData[]
  trafficSources: TrafficSource[]
  realTimeUsers: VisitData[]
}
