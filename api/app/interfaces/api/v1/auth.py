from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.auth.exceptions import (
    AuthenticationError,
    DuplicateEmailError,
    UserInactiveError,
    WeakPasswordError,
)
from app.domain.auth.services import AuthService
from app.interfaces.api.deps import get_auth_service, get_current_user, get_db, oauth2_scheme
from app.interfaces.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    ProfileResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UpdateProfileRequest,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(
    body: RegisterRequest,
    auth: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
) -> RegisterResponse:
    try:
        user = await auth.register(body.email, body.password, body.name)
        await session.commit()
        return RegisterResponse(id=user.id, email=user.email.value, name=user.name)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail={"code": e.code, "message": e.message}) from e
    except WeakPasswordError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    auth: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    try:
        pair = await auth.login(body.email, body.password, body.remember_me)
        await session.commit()
        return TokenResponse(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            expires_in=pair.expires_in,
        )
    except (AuthenticationError, UserInactiveError) as e:
        status = 403 if isinstance(e, UserInactiveError) else 401
        raise HTTPException(status_code=status, detail={"code": e.code, "message": e.message}) from e


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        pair = await auth.refresh(body.refresh_token)
        return TokenResponse(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            expires_in=pair.expires_in,
        )
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail={"code": e.code, "message": e.message}) from e


@router.post("/logout", status_code=204)
async def logout(
    body: LogoutRequest,
    access_token: str | None = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    auth: AuthService = Depends(get_auth_service),
) -> None:
    await auth.logout(access_token or "", body.refresh_token)


@router.get("/me", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)) -> ProfileResponse:
    return ProfileResponse(
        id=current_user.id,
        email=current_user.email.value,
        name=current_user.name,
        timezone=current_user.timezone,
        language=current_user.language,
        role=current_user.role,
        last_login_at=current_user.last_login_at,
        created_at=current_user.created_at,
    )


@router.put("/me", response_model=ProfileResponse)
async def update_profile(
    body: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    auth: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
) -> ProfileResponse:
    user = await auth.update_profile(
        user_id=current_user.id,
        name=body.name,
        timezone=body.timezone,
        language=body.language,
    )
    await session.commit()
    return ProfileResponse(
        id=user.id,
        email=user.email.value,
        name=user.name,
        timezone=user.timezone,
        language=user.language,
        role=user.role,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
    )


@router.put("/me/password", status_code=204)
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    auth: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
) -> None:
    try:
        await auth.change_password(current_user.id, body.old_password, body.new_password)
        await session.commit()
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail={"code": e.code, "message": e.message}) from e
    except WeakPasswordError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": e.message}) from e
