from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubirArchivoResponse(BaseModel):
    """Respuesta tras subir un archivo tabular."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id_archivo": "550e8400-e29b-41d4-a716-446655440000",
                    "nombre_archivo": "datos_clientes.csv",
                }
            ]
        }
    )

    id_archivo: str = Field(description="Identificador único del archivo en el sistema")
    nombre_archivo: str = Field(description="Nombre sanitizado guardado en servidor")


class AnalisisArchivoResponse(BaseModel):
    """Resultado del análisis automático de columnas y sensibilidad."""

    id_archivo: str
    columnas: list[str] = Field(description="Todas las columnas detectadas")
    columnas_sensibles: list[dict] = Field(
        description="Columnas marcadas como sensibles (heurísticas + patrones)"
    )
    total_filas: int = Field(ge=0, description="Número de filas de datos (excl. encabezado según lógica interna)")


class ConfiguracionProteccionItem(BaseModel):
    """Selección de técnica de protección aplicada a una columna."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"columna": "documento", "tipo_proteccion": "aes-256"},
                {"columna": "email", "tipo_proteccion": "tokenizacion"},
            ]
        }
    )

    columna: str = Field(min_length=1, max_length=100, description="Nombre de columna en el archivo fuente")
    tipo_proteccion: str = Field(
        description=(
            "Técnica aplicada. Valores admitidos: `aes-256`, `hashing`, `tokenizacion`, "
            "`pseudonimizacion`, `anonimizacion`."
        )
    )


class ProcesarArchivoRequest(BaseModel):
    """Parámetros para generar el archivo protegido."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id_archivo": "550e8400-e29b-41d4-a716-446655440000",
                    "configuraciones": [
                        {"columna": "cedula", "tipo_proteccion": "aes-256"},
                    ],
                    "clave_usuario": "opcional-segun-metodo",
                }
            ]
        }
    )

    id_archivo: str = Field(description="ID devuelto por `subir-archivo`")
    configuraciones: list[ConfiguracionProteccionItem] = Field(
        min_length=1,
        description="Al menos una columna con su método de protección",
    )
    clave_usuario: str | None = Field(
        default=None,
        description="Clave opcional requerida por algunos métodos (p. ej. AES)",
    )


class ProcesarArchivoResponse(BaseModel):
    id_archivo: str
    estado: str = Field(description="Estado del recurso, p. ej. `procesado`")
    nombre_archivo_procesado: str = Field(description="Nombre del fichero generado en almacenamiento")


class LogAuditoriaResponse(BaseModel):
    accion: str = Field(description="Tipo de evento registrado")
    nivel: str
    detalle: str = Field(description="JSON serializado; campos sensibles pueden estar enmascarados")
    fecha_evento: datetime


class DashboardResponse(BaseModel):
    archivos_procesados: int = Field(description="Archivos en estado procesado del usuario")
    datos_sensibles_detectados: int = Field(
        description="Suma de columnas sensibles detectadas en archivos del usuario"
    )
    tipos_encriptacion_usados: dict[str, int] = Field(
        description="Conteo por tipo de protección aplicada (histórico del usuario)"
    )


class DesencriptarArchivoRequest(BaseModel):
    id_archivo: str = Field(description="Archivo procesado a revertir parcialmente según configuración")
    clave_usuario: str = Field(
        min_length=4,
        max_length=256,
        description="Clave que el usuario suministró al proteger (no se registra en logs en claro)",
    )
    configuraciones: list[ConfiguracionProteccionItem] | None = Field(
        default=None,
        description="Si se omite, se usan las configuraciones persistidas para ese `id_archivo`",
    )


class DesencriptarArchivoResponse(BaseModel):
    id_archivo: str
    estado: str
    nombre_archivo_desencriptado: str


class CompararArchivosResponse(BaseModel):
    coincidencia: float = Field(ge=0, le=100, description="Porcentaje de coincidencia global")
    filas_iguales: int
    filas_diferentes: int
    columnas_con_error: list[str]
    detalle: list[dict] = Field(description="Detalle por fila/columna según el comparador")
