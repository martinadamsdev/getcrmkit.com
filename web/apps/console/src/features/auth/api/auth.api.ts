import { client } from "@/shared/api/client"

// --- Request / Response types ---

export interface LoginRequest {
  email: string
  password: string
  remember_me: boolean
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

export interface RegisterResponse {
  id: string
  email: string
  name: string
}

export interface UserProfile {
  id: string
  email: string
  name: string
  timezone: string
  language: string
  role: string
  last_login_at: string | null
  created_at: string
}

// --- API error ---

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

// --- Auth API functions ---

export async function login(data: LoginRequest): Promise<TokenResponse> {
  const response = await client.post({
    url: "/v1/auth/login",
    body: data,
  })
  if (response.error) {
    throw new ApiError(response.response.status, "INVALID_CREDENTIALS", "Login failed")
  }
  return response.data as TokenResponse
}

export async function register(data: RegisterRequest): Promise<RegisterResponse> {
  const response = await client.post({
    url: "/v1/auth/register",
    body: data,
  })
  if (response.error) {
    throw new ApiError(response.response.status, "REGISTER_FAILED", "Registration failed")
  }
  return response.data as RegisterResponse
}

export async function refreshTokens(refreshToken: string): Promise<TokenResponse> {
  const response = await client.post({
    url: "/v1/auth/refresh",
    body: { refresh_token: refreshToken },
  })
  if (response.error) {
    throw new ApiError(response.response.status, "REFRESH_FAILED", "Token refresh failed")
  }
  return response.data as TokenResponse
}

export async function logout(accessToken: string, refreshToken: string): Promise<void> {
  await client.post({
    url: "/v1/auth/logout",
    body: { refresh_token: refreshToken },
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
}

export async function getProfile(accessToken: string): Promise<UserProfile> {
  const response = await client.get({
    url: "/v1/auth/me",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  if (response.error) {
    throw new ApiError(response.response.status, "PROFILE_FAILED", "Failed to fetch profile")
  }
  return response.data as UserProfile
}
