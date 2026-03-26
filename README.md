# CryptoUGroup - Proyecto_Grado

CryptoUGroup es una plataforma de proteccion de datos sensibles en archivos
estructurados (Excel/CSV). El sistema permite detectar datos sensibles,
protegerlos con distintos metodos, desencriptar para validacion y comparar
integridad entre versiones.

## Objetivo del proyecto

Construir una solucion empresarial para:

- proteger informacion sensible por columna en archivos tabulares;
- permitir validacion del proceso de proteccion mediante desencriptacion;
- verificar integridad comparando archivo original vs desencriptado;
- ofrecer trazabilidad completa mediante auditoria y logs.

## Arquitectura actual

El proyecto se divide en dos bloques:

- `Backend/secure_api` (FastAPI + PostgreSQL + servicios de seguridad)
- `Frontend/CryptoGroup` (app de escritorio en CustomTkinter)

### Backend (`Backend/secure_api`)

Responsabilidades:

- autenticacion/autorizacion JWT;
- procesamiento y proteccion de archivos;
- desencriptacion controlada por clave de usuario;
- comparacion de integridad entre archivos;
- auditoria en base de datos y archivo de logs.

Estructura principal:

```text
Backend/secure_api/
├── core/                      # config, seguridad, dependencias
├── db/                        # sesion SQLAlchemy
├── models/                    # user, archivo, audit_logs, configuraciones
├── routers/                   # auth, users, proteccion_datos
├── schemas/                   # contratos request/response
├── services/                  # logica de negocio
│   ├── data_classifier.py
│   ├── encryption_service.py
│   ├── decryption_service.py
│   ├── file_processor.py
│   ├── comparador_service.py
│   └── audit_service.py
├── storage/
│   ├── uploads/
│   ├── processed/
│   └── logs/
└── main.py
```

### Frontend (`Frontend/CryptoGroup`)

Responsabilidades:

- login/registro y consumo de API;
- dashboard y navegacion por flujo;
- seleccion de columnas a incluir;
- configuracion de proteccion por columna;
- ejecucion de procesamiento, desencriptacion y comparacion;
- visualizacion de logs y estado del sistema.

Tecnologia UI:

- `customtkinter` (modo oscuro)
- `CTkMessagebox`
- `Pillow`
- `requests`

## Funcionamiento del sistema (flujo)

1. Usuario inicia sesion.
2. Carga archivo (`.csv`, `.xlsx`, `.xls`).
3. Backend analiza columnas sensibles (nombre + patrones).
4. Usuario elige columnas a incluir en proteccion.
5. Configura metodo por columna:
   - `aes-256`
   - `hashing`
   - `tokenizacion`
   - `pseudonimizacion`
   - `anonimizacion`
6. Procesa archivo y descarga archivo protegido.
7. (Opcional) Desencripta archivo protegido con clave de usuario.
8. (Opcional) Compara original vs desencriptado y obtiene reporte de
   coincidencia/diferencias.

## Endpoints principales

Base URL: `http://localhost:8000/api/v1`

### Autenticacion

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`
- `POST /auth/change-password`

### Proteccion / Auditoria

- `POST /proteccion-datos/subir-archivo`
- `POST /proteccion-datos/analizar-archivo`
- `POST /proteccion-datos/procesar-archivo`
- `GET /proteccion-datos/descargar-archivo/{id_archivo}`
- `GET /proteccion-datos/dashboard`
- `GET /proteccion-datos/logs-auditoria`

### Validacion de desencriptacion e integridad

- `POST /proteccion-datos/desencriptar-archivo`
- `POST /proteccion-datos/comparar-archivos`

## Seguridad implementada

- JWT en rutas protegidas.
- Sanitizacion de nombres de archivo.
- Validacion estricta de tipos permitidos.
- Claves fuera de codigo hardcodeado operativo (`.env`).
- Clave de desencriptacion solicitada al usuario en tiempo de operacion.
- No se exponen secretos ni claves en logs.
- Auditoria de eventos de carga, analisis, procesamiento, desencriptacion y
  comparacion.

## Levantamiento del proyecto

## 1) Requisitos

- Python 3.11+ recomendado
- PostgreSQL 14+ recomendado

## 2) Configurar backend

```bash
cd Backend/secure_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Crear/ajustar archivo `Backend/secure_api/.env` con al menos:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=secure_api_db
SECRET_KEY=tu_secret_jwt_seguro
APP_HOST=0.0.0.0
APP_PORT=8000
CLAVE_MAESTRA_AES=CAMBIAR_EN_PRODUCCION_CON_32_BYTES_MINIMO_1234
```

Levantar backend:

```bash
uvicorn secure_api.main:app --reload
```

Swagger:

- `http://127.0.0.1:8000/docs`

## 3) Configurar frontend

```bash
cd Frontend/CryptoGroup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Notas de uso

- Si el backend no conecta a BD, revisar variables `POSTGRES_*`.
- Si cambias `requirements.txt` y falla parseo en `uv`, validar codificacion
  UTF-8 del archivo.
- Al cambiar codigo de UI, reiniciar `python app.py` para reflejar cambios.

## Estado actual

El proyecto esta funcional en:

- autenticacion y control de acceso;
- flujo completo de proteger archivo;
- desencriptar archivo procesado;
- comparar integridad de archivos;
- dashboard y logs de auditoria en interfaz moderna.
# CryptoUGroup - Proyecto_Grado

Plataforma de proteccion de datos sensibles para archivos estructurados (CSV/Excel),
con backend en FastAPI + PostgreSQL y frontend de escritorio en Python (Tkinter).

## 1) Resultado construido

Se implemento un flujo funcional completo:

1. Autenticacion JWT (registro/login/refresh/me) existente y mantenida.
2. Subida segura de archivos CSV/XLSX.
3. Analisis automatico de columnas sensibles por:
   - Nombre de columna objetivo.
   - Patrones por regex (cedula, numero tarjeta, edad).
4. Configuracion de proteccion por columna:
   - `aes-256`
   - `hashing`
   - `tokenizacion`
   - `pseudonimizacion`
   - `anonimizacion`
5. Procesamiento de archivo y generacion de salida protegida.
6. Descarga del archivo procesado.
7. Dashboard de metricas.
8. Logs de auditoria (archivo + base de datos).

## 2) Estructura principal

```text
Proyecto Grado/
├── Backend/secure_api/
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   │   ├── user.py
│   │   ├── archivo.py
│   │   ├── log_auditoria.py
│   │   └── configuracion_encriptacion.py
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── users_router.py
│   │   └── proteccion_datos_router.py
│   ├── schemas/
│   │   └── proteccion_datos.py
│   ├── services/
│   │   ├── data_classifier.py
│   │   ├── encryption_service.py
│   │   ├── file_processor.py
│   │   └── audit_service.py
│   ├── storage/
│   │   ├── uploads/
│   │   ├── processed/
│   │   └── logs/
│   └── main.py
└── Frontend/CryptoGroup/
    ├── app.py
    └── requirements.txt
```


## 3) Endpoints principales

Base URL: `http://localhost:8000/api/v1`

Autenticacion (existentes):
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`
- `POST /auth/change-password`

Proteccion de datos (nuevos):
- `POST /proteccion-datos/subir-archivo`
- `POST /proteccion-datos/analizar-archivo`
- `POST /proteccion-datos/procesar-archivo`
- `GET /proteccion-datos/descargar-archivo/{id_archivo}`
- `GET /proteccion-datos/logs-auditoria`
- `GET /proteccion-datos/dashboard`

## 4) Seguridad aplicada

- JWT para endpoints protegidos.
- Sanitizacion de nombre de archivos.
- Validacion estricta de tipo de archivo (CSV/XLS/XLSX).
- Sin hardcode de claves operativas por endpoint.
- Clave maestra configurable por `.env` (`CLAVE_MAESTRA_AES`).
- Sin exposicion directa de valores sensibles en logs de auditoria.
- Manejo de errores controlado en backend y frontend.

## 5) Instalacion

## 5.1 Requisitos

- Python 3.11+ recomendado
- PostgreSQL 14+ recomendado

## 5.2 Backend

```bash
cd Backend/secure_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Crear `.env` tomando como base `.env.example` y agregar:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=secure_api_db
SECRET_KEY=tu_secret_jwt_seguro
APP_HOST=0.0.0.0
APP_PORT=8000
CLAVE_MAESTRA_AES=CAMBIAR_EN_PRODUCCION_CON_32_BYTES_MINIMO_1234
```

Ejecutar backend:

```bash
uvicorn secure_api.main:app --reload
```

## 6.3 Frontend

```bash
cd Frontend/CryptoGroup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 7) Testing sugerido

Pruebas minimas recomendadas:
- Unitarias: `data_classifier`, `encryption_service`, `file_processor`.
- Integracion: flujo completo `subir -> analizar -> procesar -> descargar`.
- Seguridad: archivo invalido, archivo vacio, token invalido.
- Performance basica: CSV con volumen alto de filas.

## 8) Notas finales

- La logica de procesamiento se ejecuta en backend.
- El frontend solo consume endpoints.
- La base esta lista para crecer con migraciones Alembic y mas pruebas automatizadas.
