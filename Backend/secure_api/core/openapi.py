"""
Metadatos centralizados para OpenAPI (Swagger UI / ReDoc).

Mantiene etiquetas, descripciones y respuestas reutilizables para documentación consistente.
"""

from typing import Any

# ── Etiquetas (orden = orden en Swagger UI) ───────────────────────────────────
OPENAPI_TAGS: list[dict[str, str]] = [
    {
        "name": "Health",
        "description": "Comprobación de disponibilidad del servicio.",
    },
    {
        "name": "Autenticación",
        "description": (
            "Registro, sesión JWT (access + refresh), perfil y cambio de contraseña. "
            "Las rutas protegidas requieren `Authorization: Bearer <access_token>`."
        ),
    },
    {
        "name": "Usuarios",
        "description": (
            "Administración de usuarios. **Solo superusuarios** (`is_superuser=true`)."
        ),
    },
    {
        "name": "Protección de datos",
        "description": (
            "Flujo de archivos tabulares (CSV/Excel): subida, análisis de columnas sensibles, "
            "procesamiento con técnicas de protección por columna, descarga, desencriptación, "
            "comparación de integridad, auditoría y métricas."
        ),
    },
]


def responses_auth() -> dict[int | str, dict[str, Any]]:
    """Respuestas típicas en rutas que exigen JWT válido."""
    return {
        401: {
            "description": "Token ausente, inválido o expirado.",
        },
    }


def responses_superuser() -> dict[int | str, dict[str, Any]]:
    """Respuestas para rutas que exigen superusuario."""
    base = responses_auth()
    base[403] = {"description": "El usuario no es superusuario."}
    return base


def responses_file_binary() -> dict[int | str, dict[str, Any]]:
    """Respuesta 200 para descarga de archivo binario."""
    return {
        200: {
            "description": "Cuerpo del archivo (binario). El nombre sugerido puede ir en `Content-Disposition`.",
            "content": {
                "application/octet-stream": {},
                "text/csv": {},
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {},
                "application/vnd.ms-excel": {},
            },
        },
        **responses_auth(),
    }
