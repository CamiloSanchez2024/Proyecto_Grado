from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re


# ── Request Schemas ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    """Credenciales para obtener tokens JWT."""

    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(description="Nombre de usuario registrado")
    password: str = Field(description="Contraseña en texto plano (HTTPS en producción)")


class RegisterRequest(BaseModel):
    """Datos para crear una cuenta de usuario."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "analista01",
                    "email": "analista@empresa.com",
                    "password": "ClaveSegura1",
                    "full_name": "Ana Lísta",
                }
            ]
        },
    )

    username: str = Field(description="3–50 caracteres: letras, números y guión bajo")
    email: EmailStr
    password: str = Field(description="Mínimo 8 caracteres, una mayúscula y un dígito")
    full_name: Optional[str] = Field(default=None, description="Nombre para mostrar")

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
            raise ValueError("Nombre de usuario: 3-50 caracteres, letras, números o guiones bajos únicamente")
        return v.lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        errors = []
        if len(v) < 8:
            errors.append("al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            errors.append("una letra mayúscula")
        if not re.search(r"\d", v):
            errors.append("un dígito")
        if errors:
            raise ValueError(f"Contraseña requerida: {', '.join(errors)}")
        return v


class RefreshTokenRequest(BaseModel):
    """Cuerpo para renovar el access token sin volver a iniciar sesión."""

    refresh_token: str = Field(description="Token de refresco emitido en login")


class ChangePasswordRequest(BaseModel):
    """Cambio de contraseña para el usuario autenticado."""

    current_password: str = Field(description="Contraseña actual")
    new_password: str = Field(description="Nueva contraseña (mismas reglas que en registro)")

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, v: str) -> str:
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"\d", v):
            raise ValueError("nueva contraseña: mínimo 8 caracteres, una mayúscula y un dígito")
        return v


# ── Response Schemas ───────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    """Tokens OAuth2-style (Bearer) para autorización en cabecera."""

    access_token: str = Field(description="JWT de acceso (corta duración)")
    refresh_token: str = Field(description="JWT de refresco (larga duración)")
    token_type: str = Field(default="bearer", description="Siempre `bearer` para el header Authorization")
    expires_in: int = Field(description="Segundos hasta expiración del access token")


class UserResponse(BaseModel):
    """Perfil público del usuario (sin hash de contraseña)."""

    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime]
    last_login_at: Optional[datetime]


class MessageResponse(BaseModel):
    message: str
    success: bool = Field(default=True, description="Indicador de éxito en operaciones simples")
