import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from secure_api.core.config import get_settings
from secure_api.db.session import engine, Base, AsyncSessionLocal
from secure_api.middleware.logging_middleware import RequestLoggingMiddleware
from secure_api.routers.auth_router import router as auth_router
from secure_api.routers.users_router import router as users_router
from secure_api.routers.proteccion_datos_router import router as proteccion_datos_router
#from secure_api.routers.resources_router import router as resources_router

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
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "## API protegida por JWT con respaldo de PostgreSQL\n\n"
        "### Flujo de autenticación\n"
        "1. `POST /api/v1/auth/register` — crear Usuario\n"
        "2. `POST /api/v1/auth/login` — obtener acceso y actualizar tokens\n"
        "3. Enviar `Authorization: Bearer <access_token>` en rutas protegidas\n"
        "4. `POST /api/v1/auth/refresh` — renovar token de acceso silenciosamente\n"
        "5. `POST /api/v1/auth/change-password` — actualizar contraseña\n"
    ),
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


@app.get("/", tags=["Health"])
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}