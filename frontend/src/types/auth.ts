// Auth types
export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: UserInfo
}

export interface UserInfo {
  account_id: string
  username: string
  real_name: string
  email?: string
  phone?: string
  roles: string[]
  status: number
}
