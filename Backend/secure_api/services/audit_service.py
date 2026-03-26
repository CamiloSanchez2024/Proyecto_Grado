import json
import logging
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from secure_api.core.config import get_settings
from secure_api.models.log_auditoria import LogAuditoria

settings = get_settings()
logger = logging.getLogger("audit")


class ServicioAuditoria:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        ruta_base = Path(__file__).resolve().parent.parent
        self._ruta_logs = ruta_base / settings.RUTA_STORAGE / "logs"
        self._ruta_logs.mkdir(parents=True, exist_ok=True)
        self._archivo_log = self._ruta_logs / "auditoria.log"

    async def registrar_evento(
        self,
        accion: str,
        detalle: dict,
        id_usuario: str | None = None,
        nivel: str = "INFO",
    ) -> None:
        contenido = {
            "accion": accion,
            "id_usuario": id_usuario,
            "nivel": nivel,
            "detalle": detalle,
        }
        self._escribir_log_archivo(contenido)

        log_db = LogAuditoria(
            id_usuario=id_usuario,
            accion=accion,
            detalle=json.dumps(detalle, ensure_ascii=True),
            nivel=nivel,
        )
        self._db.add(log_db)
        await self._db.flush()

    def _escribir_log_archivo(self, contenido: dict) -> None:
        linea = json.dumps(contenido, ensure_ascii=True)
        logger.info("AUDIT %s", linea)
        with self._archivo_log.open("a", encoding="utf-8") as descriptor:
            descriptor.write(f"{linea}\n")
