import base64
import hashlib
import os
from typing import Any

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from secure_api.core.config import get_settings

settings = get_settings()


class ServicioEncriptacion:
    def __init__(self) -> None:
        self._clave_maestra = hashlib.sha256(
            settings.CLAVE_MAESTRA_AES.encode("utf-8")
        ).digest()
        self._mapa_tokens: dict[str, str] = {}
        self._mapa_pseudonimos: dict[str, str] = {}

    def aplicar_proteccion(
        self, valor: Any, tipo_proteccion: str, clave_usuario: str | None = None
    ) -> str:
        valor_texto = "" if valor is None else str(valor)
        tipo = tipo_proteccion.strip().lower()

        if tipo == "aes-256":
            return self.encriptar_aes(valor_texto, clave_usuario=clave_usuario)
        if tipo == "hashing":
            return self.aplicar_hash(valor_texto)
        if tipo == "tokenizacion":
            return self.tokenizar(valor_texto)
        if tipo == "pseudonimizacion":
            return self.pseudonimizar(valor_texto)
        if tipo == "anonimizacion":
            return self.anonimizar()
        return valor_texto

    def encriptar_aes(self, valor: str, clave_usuario: str | None = None) -> str:
        clave_derivada = (
            hashlib.sha256(clave_usuario.encode("utf-8")).digest()
            if clave_usuario
            else self._clave_maestra
        )
        nonce = get_random_bytes(12)
        cifrador = AES.new(clave_derivada, AES.MODE_GCM, nonce=nonce)
        texto_cifrado, tag = cifrador.encrypt_and_digest(valor.encode("utf-8"))
        paquete = nonce + tag + texto_cifrado
        return base64.b64encode(paquete).decode("utf-8")

    @staticmethod
    def aplicar_hash(valor: str) -> str:
        return hashlib.sha256(valor.encode("utf-8")).hexdigest()

    def tokenizar(self, valor: str) -> str:
        token = f"TKN-{hashlib.sha1(valor.encode('utf-8')).hexdigest()[:12].upper()}"
        self._mapa_tokens[token] = valor
        return token

    def pseudonimizar(self, valor: str) -> str:
        token = f"PSN-{os.urandom(8).hex().upper()}"
        self._mapa_pseudonimos[token] = valor
        return token

    @staticmethod
    def anonimizar() -> str:
        return "ANONIMIZADO"

    def exportar_mapas(self) -> dict[str, dict[str, str]]:
        return {
            "tokenizacion": dict(self._mapa_tokens),
            "pseudonimizacion": dict(self._mapa_pseudonimos),
        }
