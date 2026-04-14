import os
import json
from pathlib import Path
from typing import Any

import pandas as pd

from secure_api.core.config import get_settings
from secure_api.utils.csv_encoding import read_csv_with_detected_encoding
from secure_api.services.data_classifier import ClasificadorDatos
from secure_api.services.encryption_service import ServicioEncriptacion

settings = get_settings()


class ProcesadorArchivos:
    def __init__(self) -> None:
        self._clasificador = ClasificadorDatos()
        self._encriptador = ServicioEncriptacion()
        self._ruta_base = Path(__file__).resolve().parent.parent / settings.RUTA_STORAGE
        self._ruta_subidos = self._ruta_base / "uploads"
        self._ruta_procesados = self._ruta_base / "processed"
        self._ruta_subidos.mkdir(parents=True, exist_ok=True)
        self._ruta_procesados.mkdir(parents=True, exist_ok=True)

    def sanitizar_nombre_archivo(self, nombre_archivo: str) -> str:
        nombre = os.path.basename(nombre_archivo)
        permitido = "".join(
            caracter
            for caracter in nombre
            if caracter.isalnum() or caracter in {"_", "-", ".", " "}
        ).strip()
        return permitido.replace(" ", "_")

    def guardar_archivo_subido(self, contenido: bytes, nombre_archivo: str) -> Path:
        nombre_seguro = self.sanitizar_nombre_archivo(nombre_archivo)
        ruta_destino = self._ruta_subidos / nombre_seguro
        with ruta_destino.open("wb") as descriptor:
            descriptor.write(contenido)
        return ruta_destino

    def leer_archivo_a_dataframe(self, ruta_archivo: str) -> pd.DataFrame:
        extension = Path(ruta_archivo).suffix.lower()
        if extension == ".csv":
            return read_csv_with_detected_encoding(ruta_archivo)
        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(ruta_archivo)
        raise ValueError("Tipo de archivo no soportado. Use CSV o Excel")

    def analizar_archivo(self, ruta_archivo: str) -> dict[str, Any]:
        dataframe = self.leer_archivo_a_dataframe(ruta_archivo)
        columnas = list(dataframe.columns)
        columnas_sensibles = self._clasificador.detectar_columnas_sensibles(dataframe)
        return {
            "columnas": columnas,
            "columnas_sensibles": columnas_sensibles,
            "total_filas": int(len(dataframe)),
        }

    def procesar_archivo(
        self,
        ruta_archivo: str,
        configuraciones: list[dict[str, str]],
        nombre_salida: str,
        clave_usuario: str | None = None,
    ) -> Path:
        dataframe = self.leer_archivo_a_dataframe(ruta_archivo)
        configuracion_por_columna = {
            item["columna"]: item["tipo_proteccion"] for item in configuraciones
        }
        for columna, tipo_proteccion in configuracion_por_columna.items():
            if columna in dataframe.columns:
                dataframe[columna] = dataframe[columna].apply(
                    lambda valor: self._encriptador.aplicar_proteccion(
                        valor, tipo_proteccion, clave_usuario=clave_usuario
                    )
                )

        ruta_salida = self._ruta_procesados / self.sanitizar_nombre_archivo(nombre_salida)
        extension = ruta_salida.suffix.lower()
        if extension == ".csv":
            dataframe.to_csv(ruta_salida, index=False)
        elif extension in {".xlsx", ".xls"}:
            dataframe.to_excel(ruta_salida, index=False)
        else:
            ruta_salida = ruta_salida.with_suffix(".csv")
            dataframe.to_csv(ruta_salida, index=False)

        self._guardar_metadata_proceso(
            ruta_archivo_procesado=ruta_salida,
            ruta_archivo_original=Path(ruta_archivo),
            configuraciones=configuraciones,
            clave_usuario_utilizada=bool(clave_usuario),
            mapas=self._encriptador.exportar_mapas(),
        )
        return ruta_salida

    def _guardar_metadata_proceso(
        self,
        ruta_archivo_procesado: Path,
        ruta_archivo_original: Path,
        configuraciones: list[dict[str, str]],
        clave_usuario_utilizada: bool,
        mapas: dict[str, dict[str, str]],
    ) -> None:
        metadata = {
            "ruta_original": str(ruta_archivo_original),
            "configuraciones": configuraciones,
            "clave_usuario_utilizada": clave_usuario_utilizada,
            "mapas": mapas,
        }
        ruta_metadata = self.obtener_ruta_metadata(ruta_archivo_procesado)
        ruta_metadata.write_text(
            json.dumps(metadata, ensure_ascii=True, indent=2), encoding="utf-8"
        )

    @staticmethod
    def obtener_ruta_metadata(ruta_archivo: str | Path) -> Path:
        ruta = Path(ruta_archivo)
        return ruta.with_suffix(f"{ruta.suffix}.meta.json")
