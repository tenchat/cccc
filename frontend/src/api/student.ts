import { get, post, put } from './request'
import type { StudentProfile, ImportResult, PaginatedResponse, PaginationParams } from '@/types'

export interface StudentListParams extends PaginationParams {
  college?: string
  major?: string
  employment_status?: number
  graduation_year?: number
}

export const getStudentList = (params: StudentListParams) => {
  return get<PaginatedResponse<StudentProfile>>('/students', { params })
}

export const getStudentDetail = (id: string) => {
  return get<StudentProfile>(`/students/${id}`)
}

export const updateStudent = (id: string, data: Partial<StudentProfile>) => {
  return put<StudentProfile>(`/students/${id}`, data)
}

export const importStudents = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return post<ImportResult>('/students/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const exportStudents = (params?: StudentListParams) => {
  return get<Blob>('/students/export', {
    params,
    responseType: 'blob'
  })
}
