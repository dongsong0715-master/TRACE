import type { ApiEnvelope } from './types'

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
    readonly requestId?: string,
  ) {
    super(message)
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object'
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response
  try {
    response = await fetch(`/api/v1${path}`, {
      ...options,
      credentials: 'include',
      headers: {
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
      signal: options.signal ?? AbortSignal.timeout(15_000),
    })
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR', '暂时连接不上服务，请确认服务已启动后重试。')
  }
  const body: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    const error = isRecord(body) && isRecord(body.error) ? body.error : null
    throw new ApiError(
      response.status,
      error && typeof error.code === 'string' ? error.code : 'HTTP_ERROR',
      error && typeof error.message === 'string' ? error.message : '服务暂不可用，请稍后重试。',
      isRecord(body) && typeof body.request_id === 'string' ? body.request_id : undefined,
    )
  }
  if (!isRecord(body) || !('data' in body)) {
    throw new ApiError(response.status, 'INVALID_RESPONSE', '服务响应格式不正确。')
  }
  return (body as unknown as ApiEnvelope<T>).data
}
