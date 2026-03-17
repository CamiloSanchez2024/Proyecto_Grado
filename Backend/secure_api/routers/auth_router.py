from fastapi import APIRouter, Depends, status

from secure_api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    TokenResponse,
    UserResponse,
    MessageResponse,
)
from secure_api.services.auth_service import AuthService
from secure_api.models.user import User
from secure_api.core.dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro Nuevo",
)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    user = await auth_service.register(data)
    return MessageResponse(message=f"User '{user.username}' registro exitoso")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="login y obtención de tokens de acceso y refresco",
)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.login(data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="genera un nuevo token de acceso usando un token de refresco válido",
)
async def refresh_token(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.refresh(data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="lista los datos del usuario autenticado, requiere el token de acceso en el header",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(**current_user.to_dict())


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="cambia la contraseña del usuario autenticado, requiere el token de acceso en el header",
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    await auth_service.change_password(current_user, data)
    return MessageResponse(message="contraseña actualizada exitosamente")
