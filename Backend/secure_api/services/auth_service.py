import uuid
from jose import JWTError

from secure_api.models.user import User
from secure_api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    ChangePasswordRequest,
)
from secure_api.services.user_repository import UserRepository
from secure_api.services.password_service import PasswordService
from secure_api.services.rate_limiter import rate_limiter
from secure_api.core.security import TokenService
from secure_api.core.config import get_settings
from secure_api.core.exceptions import (
    CredentialsException,
    UserNotFoundException,
    UserAlreadyExistsException,
    InactiveUserException,
)

settings = get_settings()


class AuthService:
    """
    orquesta todos los casos de uso de autenticación.
    Depende de: UserRepository (DB), PasswordService (crypto),
                TokenService (JWT), RateLimiterService (prevención de abuso).
    """

    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo
        self._pwd = PasswordService()
        self._tokens = TokenService()

    # ── Register ───────────────────────────────────────────────────────────────
    async def register(self, data: RegisterRequest) -> User:
        if await self._repo.exists_username(data.username):
            raise UserAlreadyExistsException("Username")
        if await self._repo.exists_email(data.email):
            raise UserAlreadyExistsException("Email")

        user = User(
            id=str(uuid.uuid4()),
            username=data.username.lower(),
            email=data.email.lower(),
            hashed_password=self._pwd.hash_password(data.password),
            full_name=data.full_name,
        )
        return await self._repo.save(user)

    # ── Login ──────────────────────────────────────────────────────────────────
    async def login(self, data: LoginRequest) -> TokenResponse:
        # 1. Check rate limit BEFORE hitting the DB
        rate_limiter.check_rate_limit(data.username)

        # 2. Fetch user
        user = await self._repo.find_by_username(data.username)

        # 3. Always run bcrypt to prevent timing attacks
        dummy_hash = "$2b$12$KIXbgHCvpkHJfGCMUGW.6OuCjwcZK7UtSDe3VIexE3bX6/LOkWJlC"
        stored_hash = user.hashed_password if user else dummy_hash
        password_ok = self._pwd.verify_password(data.password, stored_hash)

        if not user or not password_ok:
            rate_limiter.record_failed_attempt(data.username)
            raise CredentialsException("credenciales inválidas")

        if not user.is_active:
            raise InactiveUserException()

        # 4. Successful login — reset attempts and update last_login
        rate_limiter.reset(data.username)
        await self._repo.update_last_login(user.id)

        return self._build_token_response(user.username)

    # ── Refresh token ──────────────────────────────────────────────────────────
    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = self._tokens.decode_token(refresh_token)
            if not self._tokens.verify_token_type(payload, "refresh"):
                raise ValueError("Wrong token type")
            username: str = payload.get("sub")
        except (JWTError, ValueError):
            raise CredentialsException("Token de refresco inválido o expirado")

        user = await self._repo.find_by_username(username)
        if not user or not user.is_active:
            raise CredentialsException("usuario no encontrado o inactivo")

        return self._build_token_response(username)

    # ── Validate token → current user ──────────────────────────────────────────
    async def get_current_user(self, token: str) -> User:
        try:
            payload = self._tokens.decode_token(token)
            if not self._tokens.verify_token_type(payload, "access"):
                raise CredentialsException()
            username: str = payload.get("sub")
            if not username:
                raise CredentialsException()
        except JWTError:
            raise CredentialsException()

        user = await self._repo.find_by_username(username)
        if not user or not user.is_active:
            raise CredentialsException()
        return user

    # ── Change password ────────────────────────────────────────────────────────
    async def change_password(
        self, user: User, data: ChangePasswordRequest
    ) -> None:
        if not self._pwd.verify_password(data.current_password, user.hashed_password):
            raise CredentialsException("contraseña incorrecta")
        new_hash = self._pwd.hash_password(data.new_password)
        await self._repo.update_password(user.id, new_hash)

    # ── Private ────────────────────────────────────────────────────────────────
    def _build_token_response(self, username: str) -> TokenResponse:
        return TokenResponse(
            access_token=self._tokens.create_access_token(username),
            refresh_token=self._tokens.create_refresh_token(username),
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
