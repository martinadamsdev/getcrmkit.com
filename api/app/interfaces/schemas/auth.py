import uuid
from datetime import datetime

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class RegisterResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ProfileResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    timezone: str
    language: str
    role: str
    last_login_at: datetime | None
    created_at: datetime


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    timezone: str | None = None
    language: str | None = None


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
