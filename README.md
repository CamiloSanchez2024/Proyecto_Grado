# CryptoUGroup — Proyecto de grado

Plataforma para **detectar y proteger datos sensibles** en archivos tabulares (CSV / Excel). Incluye **autenticación JWT**, **procesamiento en backend (FastAPI)**, **persistencia en PostgreSQL**, **auditoría** y un **cliente web** (React + TypeScript + Vite) que consume la misma API.

> Documentación alineada con el estado actual del repositorio (abril 2026).

---

## Objetivos del sistema

- **Proteger información sensible por columna** en archivos estructurados (subida → análisis → configuración → procesamiento → descarga).
- **Validar el proceso** mediante desencriptación controlada (clave solicitada en la operación).
- **Verificar integridad** comparando el archivo original con una versión desencriptada.
- **Trazabilidad**: auditoría en base de datos y registro de eventos en el flujo de protección.

---

## Qué hace el sistema hoy (alcance funcional)

| Área | Comportamiento actual |
|------|------------------------|
| Autenticación | Registro, login, refresh de tokens, perfil (`/auth/me`), cambio de contraseña. Contraseñas con **bcrypt** (rounds configurables). |
| Archivos | Subida de `.csv`, `.xlsx`, `.xls`; validación de extensión y contenido no vacío; **sanitización del nombre** de archivo. |
| Detección | Análisis de columnas sensibles (nombres + patrones vía clasificador). |
| Protección | Por columna: `aes-256`, `hashing`, `tokenizacion`, `pseudonimizacion`, `anonimizacion`. |
| Validación | Desencriptación y comparación de integridad entre archivos. |
| Observabilidad | Dashboard de métricas, logs de auditoría; middleware de logging de peticiones. |
| Arranque | Creación automática de tablas al iniciar; **usuario `admin` sembrado** si no existe (ver [Seguridad](#seguridad)). |

Cliente web: flujos de **login/registro**, **carga**, **detección**, **configuración**, **procesamiento**, **desencriptación**, **comparación**, **dashboard** y **auditoría** (`Frontend/crypto-group-web`).

---

## Arquitectura

### Vista general

```text
┌─────────────────────────────────────────────────────────────────┐
│  Cliente web (React + Vite)  ←→  API REST FastAPI (/api/v1)      │
│  Axios + JWT + refresh       │  Routers: auth, users, datos     │
└────────────────────────────────┼────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │  Servicios de dominio    │
                    │  (archivo, cifrado,      │
                    │   auditoría, comparador) │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   PostgreSQL            Almacenamiento local      Logs / auditoría
   (SQLAlchemy async)    (`storage/`: uploads,     (BD + middleware)
                          processed, logs)
```

### Patrones y decisiones

- **Backend**: API REST con **FastAPI**, capas **routers → servicios → modelos**, sesión **async** (SQLAlchemy + asyncpg), configuración con **Pydantic Settings** (`core/config.py`).
- **Frontend**: SPA con **React 19**, **React Router**, **TanStack Query**, **Zustand** para estado; peticiones con **Axios** e interceptores para JWT/refresh (`Frontend/crypto-group-web/src/services/api.ts`).
- **Despliegue**: `docker-compose` orquesta **PostgreSQL 16**, **backend** (imagen Python 3.12) y **frontend** (Nginx sirve estático y hace *reverse proxy* a `/api/` y documentación embebida vía `/docs`, `/openapi.json`, `/redoc`).

### Base URL de la API

- Desarrollo típico: `http://localhost:8000/api/v1`
- Con stack Docker y proxy Nginx del frontend: el navegador puede usar rutas relativas bajo `/api/` (ver variable `VITE_API_URL` en build).

---

## Estructura del repositorio

```text
Proyecto Grado/
├── Backend/
│   ├── Dockerfile                 # Imagen del API (uvicorn)
│   ├── .dockerignore
│   └── secure_api/
│       ├── main.py                # FastAPI, CORS, lifespan, routers
│       ├── core/
│       │   ├── config.py          # Settings (.env), JWT, rate limit, storage
│       │   ├── dependencies.py    # JWT Bearer, get_current_user
│       │   ├── security.py        # Tokens JWT access/refresh
│       │   └── exceptions.py
│       ├── db/
│       │   └── session.py         # Engine async, sesiones
│       ├── middleware/
│       │   └── logging_middleware.py
│       ├── migrations/            # Alembic (env)
│       ├── models/                # User, Archivo, logs, configuración
│       ├── routers/
│       │   ├── auth_router.py
│       │   ├── users_router.py
│       │   └── proteccion_datos_router.py
│       ├── schemas/               # Pydantic (auth, protección)
│       ├── services/
│       │   ├── auth_service.py
│       │   ├── password_service.py
│       │   ├── rate_limiter.py
│       │   ├── data_classifier.py
│       │   ├── encryption_service.py
│       │   ├── decryption_service.py
│       │   ├── file_processor.py
│       │   ├── comparador_service.py
│       │   └── audit_service.py
│       ├── utils/
│       ├── storage/               # uploads, processed, logs (runtime)
│       ├── requirements.txt
│       └── .env.example
├── Frontend/
│   └── crypto-group-web/          # React + TS + Vite + Tailwind
│       ├── src/
│       │   ├── modules/           # Pantallas por flujo
│       │   ├── services/        # API + auth
│       │   ├── stores/          # Zustand
│       │   ├── components/
│       │   └── ...
│       ├── Dockerfile             # Build estático + Nginx
│       ├── nginx.conf             # Proxy a backend en Docker
│       ├── package.json
│       └── .env.example
├── docker-compose.yml             # db + backend + frontend
├── docker.env.example             # Variables para Compose
└── README.md
```

Más detalle del cliente web: [Frontend/crypto-group-web/README.md](Frontend/crypto-group-web/README.md).

---

## Seguridad

| Medida | Descripción |
|--------|-------------|
| **JWT** | Acceso y refresh con `python-jose` (HS256); rutas de datos protegidas con `HTTPBearer` y usuario actual. |
| **Contraseñas** | **bcrypt** vía Passlib; rounds configurables (`BCRYPT_ROUNDS`). |
| **Login** | **Rate limiting** en memoria por usuario (intentos / ventana); mitiga fuerza bruta. Comportamiento documentado para reemplazar por Redis en despliegues multi-instancia (`rate_limiter.py`). |
| **Timing** | En login, verificación de hash incluso si el usuario no existe (reduce filtrado por tiempo). |
| **Archivos** | Solo extensiones permitidas; rechazo de vacíos; **sanitización de nombres** al guardar. |
| **Secretos** | `SECRET_KEY`, credenciales PostgreSQL y `CLAVE_MAESTRA_AES` deben definirse por entorno (`.env` / Compose); no deben versionarse valores reales. |
| **Cifrado de datos** | Clave maestra AES para operaciones de protección; configurable por entorno. |
| **CORS** | En `main.py`, `allow_origins=["*"]` facilita desarrollo; **en producción conviene restringir** al dominio del frontend. |
| **Auditoría** | Eventos de subida, análisis, procesamiento, etc., sin exponer secretos en respuestas públicas. |
| **Usuario admin por defecto** | Al iniciar, si no existe `admin`, se crea con contraseña documentada en logs (**cambiar o deshabilitar en producción**). |

---

## Requisitos previos

- **Python** 3.11+ (el Dockerfile del backend usa 3.12).
- **PostgreSQL** 14+ (local) o contenedor; Compose usa imagen **16-alpine**.
- **Node.js** 22+ para el frontend web (recomendado en su README).

---

## Levantamiento del proyecto

### 1) Variables de entorno del backend

Copiar y editar:

```bash
cd Backend/secure_api
copy .env.example .env
```

Ajustar al menos: `POSTGRES_*`, `SECRET_KEY`, `APP_HOST`, `APP_PORT`. Para operaciones de cifrado, definir también **`CLAVE_MAESTRA_AES`** (longitud adecuada para producción). Los campos adicionales aparecen en `core/config.py` (por ejemplo límites de rate limiting).

### 2) Base de datos PostgreSQL

**Opción A — Solo PostgreSQL (ejemplo):**

```bash
docker run --name CryptoUGroup-db -e POSTGRES_PASSWORD=CryptoUGroup -e POSTGRES_DB=secure_api_db -p 5432:5432 -d postgres:16-alpine
```

Alinear usuario/contraseña/base en `Backend/secure_api/.env`.

**Opción B — Stack completo con Docker Compose** (recomendado para entorno integrado):

```bash
cd "c:\Users\Camilo S\Documents\Estudio\Proyectos\Proyecto Grado"
copy docker.env.example .env
docker compose up --build
```

Variables útiles (ver `docker.env.example`): `POSTGRES_*`, `SECRET_KEY`, `CLAVE_MAESTRA_AES`, `FRONTEND_PORT`, `BACKEND_PORT`, `VITE_API_URL` (en build del frontend, por defecto `/api/v1` para mismo origen vía Nginx).

### 3) Backend (desarrollo local)

Desde la raíz del repo, con el entorno virtual y dependencias:

```bash
cd Backend/secure_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar la API (ajustar `PYTHONPATH` si hace falta; en Docker `PYTHONPATH=/app`):

```bash
cd ..\..
set PYTHONPATH=Backend
python -m uvicorn secure_api.main:app --reload --host 0.0.0.0 --port 8000
```

O desde `Backend` si `secure_api` está en el path:

```bash
cd Backend
set PYTHONPATH=.
python -m uvicorn secure_api.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación interactiva:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

La API expone descripciones por etiqueta, `summary`/`description` por endpoint, esquemas Pydantic con campos documentados, códigos de respuesta habituales (`401`, `403`, `404`, `409`, `429`) y modelos tipados (incluida la respuesta de subida de archivo). La definición central de etiquetas OpenAPI está en `Backend/secure_api/core/openapi.py`.

### 4) Frontend web (desarrollo local)

```bash
cd Frontend/crypto-group-web
copy .env.example .env
npm install
npm run dev
```

Por defecto la app usa `VITE_API_URL=http://localhost:8000/api/v1`. Abrir **http://localhost:5173**.

### 5) Tests del frontend

```bash
cd Frontend/crypto-group-web
npm test
```

---

## Comandos de referencia rápida

| Objetivo | Comando |
|----------|---------|
| Instalar dependencias backend | `pip install -r Backend/secure_api/requirements.txt` |
| Arrancar API (desarrollo) | `uvicorn secure_api.main:app --reload` (con `PYTHONPATH` apuntando al paquete) |
| Instalar dependencias web | `cd Frontend/crypto-group-web && npm install` |
| Servidor Vite | `npm run dev` |
| Build producción web | `npm run build` |
| Lint web | `npm run lint` |
| Levantar todo con Docker | `docker compose up --build` |
| Solo imagen web (manual) | `docker build -t cryptougroup-web Frontend/crypto-group-web` |

---

## Endpoints principales

**Base:** `http://localhost:8000/api/v1` (o `/api/v1` detrás del proxy en Docker).

**Autenticación**

- `POST /auth/register` · `POST /auth/login` · `POST /auth/refresh` · `GET /auth/me` · `POST /auth/change-password`

**Protección y auditoría**

- `POST /proteccion-datos/subir-archivo`
- `POST /proteccion-datos/analizar-archivo`
- `POST /proteccion-datos/procesar-archivo`
- `GET /proteccion-datos/descargar-archivo/{id_archivo}`
- `GET /proteccion-datos/dashboard`
- `GET /proteccion-datos/logs-auditoria`

**Validación**

- `POST /proteccion-datos/desencriptar-archivo`
- `POST /proteccion-datos/comparar-archivos`

**Salud**

- `GET /` → estado de la API

---

## Flujo funcional resumido

1. El usuario inicia sesión (JWT).
2. Sube un archivo CSV/Excel.
3. El backend analiza y sugiere columnas sensibles.
4. El usuario configura método por columna y procesa.
5. Descarga el archivo protegido.
6. Opcional: desencripta con la clave correspondiente y compara integridad con el original.

---

## Notas operativas

- Si el backend no conecta a la BD, revisar `POSTGRES_*` y que PostgreSQL esté accesible.
- El **rate limit** de login es en memoria: en varias réplicas del mismo servicio, valorar un almacén compartido (p. ej. Redis).
- Tras cambios en variables de entorno del frontend embebidas en build (`VITE_*`), reconstruir la imagen o ejecutar `npm run build` de nuevo.

---

## Estado del código

El repositorio concentra el **backend FastAPI** y el **frontend web**. La documentación histórica del cliente de escritorio CustomTkinter no forma parte de este árbol; el flujo oficial documentado en código es el **cliente React** bajo `Frontend/crypto-group-web`.
