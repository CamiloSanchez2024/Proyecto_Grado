import base64
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd
from Crypto.Cipher import AES

from secure_api.core.config import get_settings
from secure_api.services.file_processor import ProcesadorArchivos

settings = get_settings()


class ServicioDesencriptacion:
    def __init__(self) -> None:
        self._procesador = ProcesadorArchivos()
        self._clave_maestra = hashlib.sha256(
            settings.CLAVE_MAESTRA_AES.encode("utf-8")
        ).digest()

    def desencriptar_archivo(
        self,
        ruta_archivo: str,
        clave_usuario: str,
        configuracion: list[dict[str, str]] | None = None,
    ) -> Path:
        dataframe = self._procesador.leer_archivo_a_dataframe(ruta_archivo)
        metadata = self._leer_metadata(ruta_archivo)
        configuraciones = configuracion or metadata.get("configuraciones", [])
        mapas = metadata.get("mapas", {})

        for item in configuraciones:
            columna = item.get("columna")
            tipo_proteccion = str(item.get("tipo_proteccion", "")).lower()
            if columna not in dataframe.columns:
                continue
            if tipo_proteccion == "aes-256":
                dataframe[columna] = dataframe[columna].apply(
                    lambda valor: self._desencriptar_aes(
                        str(valor), clave_usuario=clave_usuario
                    )
                )
            elif tipo_proteccion == "tokenizacion":
                mapa_tokens = mapas.get("tokenizacion", {})
                dataframe[columna] = dataframe[columna].apply(
                    lambda valor: mapa_tokens.get(str(valor), str(valor))
                )
            elif tipo_proteccion == "pseudonimizacion":
                mapa_pseudonimos = mapas.get("pseudonimizacion", {})
                dataframe[columna] = dataframe[columna].apply(
                    lambda valor: mapa_pseudonimos.get(str(valor), str(valor))
                )

        ruta_salida = self._generar_ruta_desencriptado(ruta_archivo)
        extension = ruta_salida.suffix.lower()
        if extension == ".csv":
            dataframe.to_csv(ruta_salida, index=False)
        else:
            dataframe.to_excel(ruta_salida, index=False)
        return ruta_salida

    def _desencriptar_aes(self, valor_cifrado: str, clave_usuario: str) -> str:
        paquete = base64.b64decode(valor_cifrado.encode("utf-8"))
        nonce, tag, cifrado = paquete[:12], paquete[12:28], paquete[28:]

        clave_derivada_usuario = hashlib.sha256(clave_usuario.encode("utf-8")).digest()
        try:
            descifrador_usuario = AES.new(clave_derivada_usuario, AES.MODE_GCM, nonce=nonce)
            texto = descifrador_usuario.decrypt_and_verify(cifrado, tag)
            return texto.decode("utf-8")
        except Exception:
            # Compatibilidad con archivos anteriores encriptados con clave maestra.
            descifrador_maestro = AES.new(self._clave_maestra, AES.MODE_GCM, nonce=nonce)
            texto = descifrador_maestro.decrypt_and_verify(cifrado, tag)
            return texto.decode("utf-8")

    @staticmethod
    def _generar_ruta_desencriptado(ruta_archivo: str) -> Path:
        ruta = Path(ruta_archivo)
        return ruta.with_name(f"desencriptado_{ruta.name}")

    def _leer_metadata(self, ruta_archivo: str) -> dict[str, Any]:
        ruta_metadata = self._procesador.obtener_ruta_metadata(ruta_archivo)
        if not ruta_metadata.exists():
            return {}
        return json.loads(ruta_metadata.read_text(encoding="utf-8"))
