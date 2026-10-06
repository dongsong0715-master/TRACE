import { request } from './client'
import type { Account, Profile, ProfileUpdate } from './types'

export const accountApi = {
  me: () => request<Account>('/me'),
  register: (username: string, password: string, nickname: string) =>
    request<Account>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password, nickname }),
    }),
  login: (username: string, password: string) =>
    request<Account>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  logout: () => request<{ logged_out: boolean }>('/auth/logout', { method: 'POST' }),
  saveProfile: (payload: ProfileUpdate) =>
    request<Profile>('/me/profile', { method: 'PATCH', body: JSON.stringify(payload) }),
}
