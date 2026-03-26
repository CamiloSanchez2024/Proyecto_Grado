import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from secure_api.db.session import Base


class ConfiguracionEncriptacion(Base):
    __tablename__ = "configuraciones_encriptacion"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    id_archivo: Mapped[str] = mapped_column(
        String(36), ForeignKey("archivos.id"), nullable=False, index=True
    )
    nombre_columna: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_proteccion: Mapped[str] = mapped_column(String(50), nullable=False)
    algoritmo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
