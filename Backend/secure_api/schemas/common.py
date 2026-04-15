"""Esquemas compartidos para documentación OpenAPI y respuestas uniformes."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Estado del servicio."""

    status: str = Field(examples=["ok"])
    app: str = Field(description="Nombre de la aplicación")
    version: str = Field(description="Versión semántica de la API")


class ErrorPayload(BaseModel):
    """Cuerpo típico de error controlado (4xx/5xx) en esta API."""

    detail: str | list = Field(description="Mensaje o lista de errores de validación")
    success: bool = Field(default=False, description="Indicador de fallo en respuestas JSON propias")
