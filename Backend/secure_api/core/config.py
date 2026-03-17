from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Ruta absoluta al .env
# __file__ = .../secure_api/core/config.py
# .parent   = .../secure_api/core/
# .parent   = .../secure_api/          ← aquí está el .env
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    # ── App ────────────────────────────────────────────────
    APP_NAME: str = "Secure API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── PostgreSQL — vienen del .env, sin defaults ─────────
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # ── Server ─────────────────────────────────────────────────
    APP_HOST: str 
    APP_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ── JWT — vienen del .env, sin defaults ───────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Security ───────────────────────────────────────────
    BCRYPT_ROUNDS: int = 12
    RATE_LIMIT_ATTEMPTS: int = 5
    RATE_LIMIT_WINDOW_SECONDS: int = 300

    class Config:
        env_file = str(ENV_FILE)   # ← ruta absoluta, siempre funciona
        case_sensitive = True

    

@lru_cache()
def get_settings() -> Settings:
    return Settings()