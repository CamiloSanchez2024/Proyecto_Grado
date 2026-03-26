from datetime import datetime

from pydantic import BaseModel, Field


class AnalisisArchivoResponse(BaseModel):
    id_archivo: str
    columnas: list[str]
    columnas_sensibles: list[dict]
    total_filas: int


class ConfiguracionProteccionItem(BaseModel):
    columna: str = Field(min_length=1, max_length=100)
    tipo_proteccion: str = Field(
        description="Opciones: aes-256, hashing, tokenizacion, pseudonimizacion, anonimizacion"
    )


class ProcesarArchivoRequest(BaseModel):
    id_archivo: str
    configuraciones: list[ConfiguracionProteccionItem]
    clave_usuario: str | None = None


class ProcesarArchivoResponse(BaseModel):
    id_archivo: str
    estado: str
    nombre_archivo_procesado: str


class LogAuditoriaResponse(BaseModel):
    accion: str
    nivel: str
    detalle: str
    fecha_evento: datetime


class DashboardResponse(BaseModel):
    archivos_procesados: int
    datos_sensibles_detectados: int
    tipos_encriptacion_usados: dict[str, int]


class DesencriptarArchivoRequest(BaseModel):
    id_archivo: str
    clave_usuario: str = Field(min_length=4, max_length=256)
    configuraciones: list[ConfiguracionProteccionItem] | None = None


class DesencriptarArchivoResponse(BaseModel):
    id_archivo: str
    estado: str
    nombre_archivo_desencriptado: str


class CompararArchivosResponse(BaseModel):
    coincidencia: float
    filas_iguales: int
    filas_diferentes: int
    columnas_con_error: list[str]
    detalle: list[dict]
