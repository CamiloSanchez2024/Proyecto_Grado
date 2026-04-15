from fastapi import APIRouter, Depends, status

from secure_api.core.openapi import responses_auth
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

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description=(
        "Crea una cuenta nueva. Las contraseñas se almacenan con **bcrypt**. "
        "Puede responder `409` si el usuario o correo ya existen."
    ),
    responses={
        201: {"description": "Usuario creado."},
        409: {"description": "Usuario o email ya registrado."},
        422: {"description": "Cuerpo inválido (validación Pydantic)."},
    },
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
    summary="Iniciar sesión",
    description=(
        "Devuelve **access_token** y **refresh_token**. Tras varios intentos fallidos por usuario "
        "se aplica **rate limiting** (`429`). Las contraseñas incorrectas responden `401` sin distinguir "
        "si el usuario existe (mitigación de enumeración)."
    ),
    responses={
        200: {"description": "Tokens emitidos."},
        401: {"description": "Credenciales inválidas o usuario inactivo."},
        429: {"description": "Demasiados intentos fallidos; esperar ventana configurada."},
        422: {"description": "Cuerpo inválido."},
    },
)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.login(data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Renovar access token",
    description="Intercambia un **refresh_token** válido por un nuevo par de tokens.",
    responses={
        200: {"description": "Nuevo access y refresh token."},
        401: {"description": "Refresh token inválido o expirado."},
        422: {"description": "Cuerpo inválido."},
    },
)
async def refresh_token(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.refresh(data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Perfil del usuario actual",
    description="Requiere cabecera `Authorization: Bearer <access_token>`.",
    responses=responses_auth(),
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(**current_user.to_dict())


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Cambiar contraseña",
    description="Requiere access token y la contraseña actual. La nueva debe cumplir las reglas de fortaleza.",
    responses={
        **responses_auth(),
        200: {"description": "Contraseña actualizada."},
        401: {
            "description": "Token ausente/inválido o contraseña actual incorrecta.",
        },
    },
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    await auth_service.change_password(current_user, data)
    return MessageResponse(message="contraseña actualizada exitosamente")
