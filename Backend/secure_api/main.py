import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from secure_api.core.config import get_settings
from secure_api.core.openapi import OPENAPI_TAGS
from secure_api.db.session import engine, Base, AsyncSessionLocal
from secure_api.middleware.logging_middleware import RequestLoggingMiddleware
from secure_api.routers.auth_router import router as auth_router
from secure_api.routers.users_router import router as users_router
from secure_api.routers.proteccion_datos_router import router as proteccion_datos_router
from secure_api.schemas.common import HealthResponse
# from secure_api.routers.resources_router import router as resources_router

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("api")


# ── Lifespan: startup / shutdown ───────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Api Iniciada — Creando tablas si no existen...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed a default admin user
    await _seed_admin()

    logger.info("Tablas listas y admin creado (si no existía)")
    yield

    logger.info("Servicio abajo — cerrando DB connections...")
    await engine.dispose()


#---- Función para agregar un usuario admin por defecto si no existe ----
async def _seed_admin() -> None:
    from secure_api.models.user import User
    from secure_api.services.password_service import PasswordService
    from secure_api.services.user_repository import UserRepository
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        if result.scalar_one_or_none() is None:
            admin = User(
                id="0000",
                username="admin",
                email="admin@example.com",
                hashed_password=PasswordService.hash_password("Admin1234"),
                full_name="Administrator",
                is_superuser=True,
            )
            db.add(admin)
            await db.commit()
            logger.info("👤 admin agregado por defecto → username: admin | password: Admin1234")


# ── App factory ────────────────────────────────────────────────────────────────
_API_DESCRIPTION = """
## CryptoUGroup — API de protección de datos

REST API construida con **FastAPI**, persistencia **PostgreSQL** (SQLAlchemy async) y autenticación **JWT**
(access + refresh). Las rutas bajo `/api/v1/proteccion-datos/*` gestionan archivos CSV/Excel: detección de
columnas sensibles, aplicación de técnicas de protección por columna, auditoría y métricas.

### Autenticación

1. `POST /api/v1/auth/register` — alta de usuario (opcional según despliegue).
2. `POST /api/v1/auth/login` — obtiene `access_token` y `refresh_token`.
3. Enviar cabecera `Authorization: Bearer <access_token>` en rutas protegidas.
4. `POST /api/v1/auth/refresh` — renovar access token con el refresh token.
5. `POST /api/v1/auth/change-password` — cambio de contraseña (requiere access token).

### Documentación interactiva

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **OpenAPI JSON:** `/openapi.json`

### Convenciones de error

Las respuestas de error suelen incluir `detail` (mensaje o lista de validación). Códigos habituales: `401`
no autenticado, `403` prohibido, `404` no encontrado, `409` conflicto (p. ej. usuario duplicado), `429`
demasiados intentos de login.
"""

app = FastAPI(
    title="CryptoUGroup API",
    description=_API_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=OPENAPI_TAGS,
    terms_of_service=None,
    contact={"name": "CryptoUGroup"},
    license_info={
        "name": "Proyecto académico — consultar al autor",
    },
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# ── Global error handler ───────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "success": False},
    )

# ── Routers ────────────────────────────────────────────────────────────────────
PREFIX = "/api/v1"
app.include_router(auth_router, prefix=PREFIX)
app.include_router(users_router, prefix=PREFIX)
app.include_router(proteccion_datos_router, prefix=PREFIX)
#app.include_router(resources_router, prefix=PREFIX)


@app.get(
    "/",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Estado del servicio",
    description="Comprueba que la API responde y devuelve nombre y versión configurados.",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.APP_NAME, version=settings.APP_VERSION)