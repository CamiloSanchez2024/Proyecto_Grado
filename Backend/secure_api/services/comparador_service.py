from pathlib import Path
from typing import Any

import pandas as pd

from secure_api.utils.csv_encoding import read_csv_with_detected_encoding


def _limpiar_nombre_columna(nombre: Any) -> str:
    """Quita espacios, BOM y unifica para comparar Excel vs CSV."""
    s = str(nombre).strip()
    if s.startswith("\ufeff"):
        s = s[1:].strip()
    return s


def _mapa_columnas_normalizadas(df: pd.DataFrame) -> dict[str, str]:
    """clave normalizada -> nombre real en el DataFrame."""
    m: dict[str, str] = {}
    for c in df.columns:
        m[_limpiar_nombre_columna(c)] = c
    return m


def _valores_equivalentes(a: Any, b: Any) -> bool:
    """Misma celda aunque Excel use float y CSV texto, o 1 vs 1.0."""
    if pd.isna(a) and pd.isna(b):
        return True
    if pd.isna(a) or pd.isna(b):
        return False
    if a == b:
        return True
    sa, sb = str(a).strip(), str(b).strip()
    if sa == sb:
        return True
    try:
        fa = float(sa.replace(",", "."))
        fb = float(sb.replace(",", "."))
        if abs(fa - fb) < 1e-9:
            return True
    except ValueError:
        pass
    return False


class ServicioComparadorArchivos:
    def comparar_archivos(
        self, ruta_original: str, ruta_desencriptado: str
    ) -> dict[str, Any]:
        df_original = self._leer_archivo(ruta_original)
        df_desencriptado = self._leer_archivo(ruta_desencriptado)

        mapa_orig = _mapa_columnas_normalizadas(df_original)
        mapa_dec = _mapa_columnas_normalizadas(df_desencriptado)
        claves_comunes = sorted(set(mapa_orig.keys()) & set(mapa_dec.keys()))

        if not claves_comunes:
            return {
                "coincidencia": 0.0,
                "filas_iguales": 0,
                "filas_diferentes": max(len(df_original), len(df_desencriptado)),
                "columnas_con_error": [],
                "detalle": [
                    {
                        "tipo": "sin_columnas_alineadas",
                        "mensaje": (
                            "No hay columnas coincidentes tras normalizar nombres "
                            "(espacios, BOM). Compare las listas o use el mismo "
                            "orden de columnas que el original."
                        ),
                        "columnas_original": [str(c) for c in df_original.columns],
                        "columnas_desencriptado": [str(c) for c in df_desencriptado.columns],
                        "columnas_normalizadas_origen": list(mapa_orig.keys()),
                        "columnas_normalizadas_desencriptado": list(mapa_dec.keys()),
                    }
                ],
            }

        total_celdas = max(len(df_original), len(df_desencriptado)) * max(
            len(claves_comunes), 1
        )
        celdas_iguales = 0
        detalle_diferencias: list[dict[str, Any]] = []
        columnas_con_error: set[str] = set()

        limite_filas = max(len(df_original), len(df_desencriptado))
        for indice in range(limite_filas):
            for clave in claves_comunes:
                col_o = mapa_orig[clave]
                col_d = mapa_dec[clave]
                vo = (
                    df_original.at[indice, col_o]
                    if indice < len(df_original)
                    else None
                )
                vd = (
                    df_desencriptado.at[indice, col_d]
                    if indice < len(df_desencriptado)
                    else None
                )
                if vo is None or vd is None:
                    columnas_con_error.add(str(col_o))
                    if len(detalle_diferencias) < 200:
                        detalle_diferencias.append(
                            {
                                "fila": indice + 1,
                                "columna": str(col_o),
                                "valor_original": "<sin_fila>" if vo is None else str(vo),
                                "valor_desencriptado": (
                                    "<sin_fila>" if vd is None else str(vd)
                                ),
                            }
                        )
                    continue
                if _valores_equivalentes(vo, vd):
                    celdas_iguales += 1
                else:
                    columnas_con_error.add(str(col_o))
                    if len(detalle_diferencias) < 200:
                        detalle_diferencias.append(
                            {
                                "fila": indice + 1,
                                "columna": str(col_o),
                                "valor_original": str(vo),
                                "valor_desencriptado": str(vd),
                            }
                        )

        coincidencia = (celdas_iguales / total_celdas * 100) if total_celdas else 0.0
        filas_iguales = int(
            sum(
                1
                for i in range(min(len(df_original), len(df_desencriptado)))
                if all(
                    _valores_equivalentes(
                        df_original.at[i, mapa_orig[clave]],
                        df_desencriptado.at[i, mapa_dec[clave]],
                    )
                    for clave in claves_comunes
                )
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
    def _extension_real_por_contenido(ruta: Path) -> str:
        """Si el archivo tiene extensión .csv pero es binario Excel, leer como xlsx/xls."""
        suf = ruta.suffix.lower()
        try:
            cab = ruta.read_bytes()[:8]
        except OSError:
            return suf
        if suf == ".csv" and len(cab) >= 2 and cab[:2] == b"PK":
            return ".xlsx"
        if suf == ".csv" and len(cab) >= 8 and cab[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            return ".xls"
        return suf

    @classmethod
    def _leer_archivo(cls, ruta_archivo: str) -> pd.DataFrame:
        ruta = Path(ruta_archivo)
        extension = cls._extension_real_por_contenido(ruta)
        if extension == ".csv":
            return read_csv_with_detected_encoding(ruta_archivo).fillna("")
        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(ruta_archivo).fillna("")
        raise ValueError("Tipo de archivo no soportado. Use CSV o Excel")
