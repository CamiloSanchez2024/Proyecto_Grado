"""Lectura de CSV con detección de codificación y reintentos seguros."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Union

import pandas as pd
from charset_normalizer import from_bytes

# Muestra suficiente para detección sin cargar archivos enormes en memoria.
_MAX_BYTES_MUESTRA = 1_000_000


def _estrategias_read_csv() -> list[dict[str, Any]]:
    """
    Primero detección automática del delimitador (coma, punto y coma, tab, etc.);
    luego motor C con coma; separadores típicos; por último filas irregulares.
    """
    return [
        {"sep": None, "engine": "python"},
        {},
        {"sep": ";"},
        {"sep": "\t"},
        {"sep": "|"},
        {"sep": ";", "engine": "python"},
        {"sep": None, "engine": "python", "on_bad_lines": "skip"},
    ]


def _read_csv_una_codificacion(path: Path, encoding: str) -> pd.DataFrame:
    ultimo_parse: pd.errors.ParserError | None = None
    for extra in _estrategias_read_csv():
        kwargs: dict[str, Any] = {"encoding": encoding, **extra}
        try:
            return pd.read_csv(path, **kwargs)
        except UnicodeDecodeError:
            raise
        except pd.errors.ParserError as exc:
            ultimo_parse = exc
            continue
    if ultimo_parse is not None:
        raise ultimo_parse
    raise RuntimeError("No se pudo analizar el CSV con ninguna estrategia de delimitador.")


def _candidatos_codificacion(muestra: bytes) -> list[str]:
    if not muestra:
        return ["utf-8"]
    resultado = from_bytes(muestra)
    mejor = resultado.best()
    ordenados: list[str] = []
    if mejor is not None and mejor.encoding:
        ordenados.append(mejor.encoding)
    for cod in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        if cod not in ordenados:
            ordenados.append(cod)
    return ordenados


def read_csv_with_detected_encoding(ruta: Union[str, Path]) -> pd.DataFrame:
    """
    Lee un CSV probando primero la codificación inferida del contenido y luego
    valores habituales (UTF-8 con BOM, UTF-8, Windows-1252, Latin-1).
    Latin-1 decodifica cualquier secuencia de bytes y actúa como último recurso.

    Si la codificación es válida pero el delimitador no es coma (p. ej. ``;`` en
    Excel regional), reintenta con detección automática y separadores habituales.
    """
    path = Path(ruta)
    muestra = path.read_bytes()[:_MAX_BYTES_MUESTRA]
    ultimo_error: UnicodeDecodeError | None = None
    for codificacion in _candidatos_codificacion(muestra):
        try:
            return _read_csv_una_codificacion(path, codificacion)
        except UnicodeDecodeError as exc:
            ultimo_error = exc
            continue
    if ultimo_error is not None:
        raise ultimo_error
    raise RuntimeError("No se pudo leer el CSV: no hay codificaciones candidatas.")
