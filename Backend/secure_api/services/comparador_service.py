from pathlib import Path
from typing import Any

import pandas as pd


class ServicioComparadorArchivos:
    def comparar_archivos(
        self, ruta_original: str, ruta_desencriptado: str
    ) -> dict[str, Any]:
        df_original = self._leer_archivo(ruta_original)
        df_desencriptado = self._leer_archivo(ruta_desencriptado)

        columnas_original = list(df_original.columns)
        columnas_desencriptado = list(df_desencriptado.columns)
        columnas_comunes = [c for c in columnas_original if c in columnas_desencriptado]

        total_celdas = max(len(df_original), len(df_desencriptado)) * max(
            len(columnas_comunes), 1
        )
        celdas_iguales = 0
        detalle_diferencias: list[dict[str, Any]] = []
        columnas_con_error: set[str] = set()

        limite_filas = max(len(df_original), len(df_desencriptado))
        for indice in range(limite_filas):
            for columna in columnas_comunes:
                valor_original = (
                    str(df_original.at[indice, columna])
                    if indice < len(df_original)
                    else "<sin_fila>"
                )
                valor_desencriptado = (
                    str(df_desencriptado.at[indice, columna])
                    if indice < len(df_desencriptado)
                    else "<sin_fila>"
                )
                if valor_original == valor_desencriptado:
                    celdas_iguales += 1
                else:
                    columnas_con_error.add(columna)
                    if len(detalle_diferencias) < 200:
                        detalle_diferencias.append(
                            {
                                "fila": indice + 1,
                                "columna": columna,
                                "valor_original": valor_original,
                                "valor_desencriptado": valor_desencriptado,
                            }
                        )

        coincidencia = (celdas_iguales / total_celdas * 100) if total_celdas else 0.0
        filas_iguales = int(
            sum(
                1
                for i in range(min(len(df_original), len(df_desencriptado)))
                if list(df_original.iloc[i].astype(str))
                == list(df_desencriptado.iloc[i].astype(str))
            )
        )
        filas_diferentes = abs(len(df_original) - len(df_desencriptado)) + max(
            0, min(len(df_original), len(df_desencriptado)) - filas_iguales
        )

        return {
            "coincidencia": round(coincidencia, 2),
            "filas_iguales": filas_iguales,
            "filas_diferentes": filas_diferentes,
            "columnas_con_error": sorted(columnas_con_error),
            "detalle": detalle_diferencias,
        }

    @staticmethod
    def _leer_archivo(ruta_archivo: str) -> pd.DataFrame:
        ruta = Path(ruta_archivo)
        extension = ruta.suffix.lower()
        if extension == ".csv":
            return pd.read_csv(ruta_archivo).fillna("")
        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(ruta_archivo).fillna("")
        raise ValueError("Tipo de archivo no soportado. Use CSV o Excel")
