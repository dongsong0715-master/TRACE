export interface Profile {
  id: string
  nickname: string
  education: 'college' | 'bachelor' | 'master' | null
  target_category: 'python' | 'frontend' | 'data' | null
  preferred_cities: string[]
  version: number
}

export interface Account {
  id: string
  username: string
  role: 'student' | 'admin'
  is_demo: boolean
  profile: Profile | null
}

export interface ProfileUpdate {
  version: number
  nickname: string
  education: Profile['education']
  target_category: Profile['target_category']
  preferred_cities: string[]
}

export interface ApiEnvelope<T> {
  data: T
  request_id: string
}
