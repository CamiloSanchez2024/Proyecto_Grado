import re
from typing import Any

import pandas as pd


class ClasificadorDatos:
    columnas_objetivo = {
        "nombres",
        "apellidos",
        "cedula",
        "numero_tarjeta",
        "nombre_cuenta",
        "banco",
        "ciudad",
        "cupo_tarjeta",
        "edad",
        "tipo_cliente",
    }

    patrones = {
        "cedula": re.compile(r"\b\d{6,12}\b"),
        "numero_tarjeta": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        "edad": re.compile(r"\b(?:1[89]|[2-9]\d)\b"),
    }

    def detectar_columnas_sensibles(
        self, dataframe: pd.DataFrame
    ) -> list[dict[str, Any]]:
        columnas_sensibles: list[dict[str, Any]] = []
        for columna in dataframe.columns:
            nombre_normalizado = self._normalizar_columna(columna)
            puntaje = 0
            evidencia: list[str] = []

            if nombre_normalizado in self.columnas_objetivo:
                puntaje += 70
                evidencia.append("coincidencia_nombre_columna")

            serie = dataframe[columna].astype(str).fillna("")
            for nombre_patron, patron in self.patrones.items():
                muestras = serie.head(50).tolist()
                coincidencias = sum(1 for valor in muestras if patron.search(valor))
                if coincidencias > 0:
                    puntaje += 10 + min(coincidencias, 20)
                    evidencia.append(f"patron_{nombre_patron}:{coincidencias}")

            es_sensible = puntaje >= 70
            if es_sensible:
                columnas_sensibles.append(
                    {
                        "columna": columna,
                        "puntaje": min(puntaje, 100),
                        "clasificacion": "sensible",
                        "evidencia": evidencia,
                    }
                )
        return columnas_sensibles

    @staticmethod
    def _normalizar_columna(nombre_columna: str) -> str:
        nombre = nombre_columna.strip().lower()
        nombre = nombre.replace(" ", "_")
        return nombre
