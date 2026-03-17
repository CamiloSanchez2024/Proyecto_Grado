# CryptoUGroup

## Descripción

CryptoUGroup es una solución integral para el envío seguro de archivos encriptados. El sistema está compuesto por un Frontend y un Backend, ambos con capacidades de encriptación y desencriptación. El flujo principal consiste en que el usuario envía un archivo encriptado desde el Frontend, el Backend lo recibe y realiza procesos de anonimización o pseudonimización, y posteriormente lo vuelve a encriptar para el intercambio seguro de información adicional.

## Objetivos

- Permitir el envío seguro de archivos encriptados.
- Anonimizar o pseudonimizar archivos en el Backend.
- Re-encriptar archivos para el intercambio de información adicional.
- Proveer funcionalidades de encriptación y desencriptación tanto en el Frontend como en el Backend.

## Estructura del Proyecto

```
Proyecto Grado/
│
├── Backend/
│   └── secure_api/
│       ├── core/
│       ├── db/
│       ├── middleware/
│       ├── migrations/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       └── services/
│
└── Frontend/
    └── CryptoGroup/
        ├── app.py
        ├── requirements.txt
        └── Imagenes/
```

## Funcionalidades

### Frontend

- Encriptación y desencriptación de archivos.
- Interfaz para enviar archivos encriptados al Backend.
- Implementado en Python (ver `CryptoGroup/app.py`).

### Backend

- Recepción de archivos encriptados.
- Procesos de anonimización/pseudonimización.
- Re-encriptación de archivos.
- API segura para el intercambio de archivos.
- Autenticación de usuarios utilizando base de datos PostgreSQL.
- Implementado en Python con FastAPI.

## Instalación y Configuración

### Clonar el repositorio

```bash
git clone https://github.com/CamiloSanchez2024/Proyecto_Grado.git
cd Proyecto_Grado
```

### Crear y activar entorno virtual (recomendado)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependencias

#### Backend

```bash
cd Backend/secure_api
pip install -r requirements.txt
```

#### Frontend

```bash
cd Frontend/CryptoGroup
pip install -r requirements.txt
```

### Configurar la base de datos PostgreSQL

- Crea una base de datos PostgreSQL.
- Configura las variables de entorno en el archivo `.env` dentro de `Backend/secure_api`.

### Levantar los entornos

#### Backend

Desde la carpeta `Backend`, ejecuta:

```bash
uvicorn secure_api.main:app --reload
```

#### Frontend

Desde la carpeta `Frontend/CryptoGroup`, ejecuta:

```bash
python app.py
```

## Uso

1. Encripta un archivo desde el Frontend.
2. Envía el archivo encriptado al Backend.
3. El Backend anonimiza/pseudonimiza el archivo y lo re-encripta.
4. Descarga o consulta el archivo procesado.

## Contribución

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva`).
3. Realiza tus cambios y haz commit.
4. Envía un pull request.


