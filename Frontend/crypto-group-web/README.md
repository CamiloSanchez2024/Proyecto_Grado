# CryptoUGroup — Web (React + TypeScript)

Cliente web que consume la API FastAPI de `Backend/secure_api`. Sustituye el frontend de escritorio en `Frontend/CryptoGroup` (CustomTkinter) manteniendo los mismos flujos y endpoints.

## Requisitos

- Node.js 22+ (recomendado)
- Backend en ejecución (por defecto `http://localhost:8000`)

## Configuración

```bash
cp .env.example .env
# Editar VITE_API_URL si el backend no está en localhost:8000/api/v1
```

## Desarrollo

```bash
npm install
npm run dev
```

Abre `http://localhost:5173`.

## Producción

```bash
npm run build
npm run preview
```

## Tests

```bash
npm test
```

## Docker

```bash
docker build -t cryptougroup-web .
docker run -p 8080:80 cryptougroup-web
```

La app se sirve en el puerto 80 del contenedor; configura `VITE_API_URL` en tiempo de **build** si el API no está en el mismo origen (CORS en el backend).

## Estructura

- `src/modules/*` — pantallas por flujo (auth, dashboard, carga, detección, etc.)
- `src/services/*` — cliente HTTP (Axios + JWT + refresh)
- `src/stores/*` — Zustand (sesión y estado del archivo en curso)
