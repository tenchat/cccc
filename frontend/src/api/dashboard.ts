import { request, DashboardData } from './index'

export const getDashboardData = () => {
  return request.get<DashboardData>('/dashboard/data')
}

export const getStats = () => {
  return request.get('/dashboard/stats')
}

export const getVisitTrend = (params: { days?: number }) => {
  return request.get('/dashboard/visit-trend', { params })
}

export const getRegionDistribution = () => {
  return request.get('/dashboard/region')
}

export const getTrafficSources = () => {
  return request.get('/dashboard/traffic-sources')
}

export const getRealTimeUsers = () => {
  return request.get('/dashboard/realtime')
}
