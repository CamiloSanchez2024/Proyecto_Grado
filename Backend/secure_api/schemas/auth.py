from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


# ── Request Schemas ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str
    model_config = {"str_strip_whitespace": True}


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

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

    model_config = {"str_strip_whitespace": True}


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, v: str) -> str:
        if len(v) < 8 or not re.search(r"[A-Z]", v) or not re.search(r"\d", v):
            raise ValueError("nueva contraseña: mínimo 8 caracteres, una mayúscula y un dígito")
        return v


# ── Response Schemas ───────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
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
    success: bool = True
