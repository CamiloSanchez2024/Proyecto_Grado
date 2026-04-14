import json
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from secure_api.core.dependencies import get_current_user
from secure_api.db.session import get_db
from secure_api.models.archivo import Archivo
from secure_api.models.configuracion_encriptacion import ConfiguracionEncriptacion
from secure_api.models.log_auditoria import LogAuditoria
from secure_api.models.user import User
from secure_api.schemas.proteccion_datos import (
    AnalisisArchivoResponse,
    CompararArchivosResponse,
    DashboardResponse,
    DesencriptarArchivoRequest,
    LogAuditoriaResponse,
    ProcesarArchivoRequest,
    ProcesarArchivoResponse,
)
from secure_api.services.audit_service import ServicioAuditoria
from secure_api.services.comparador_service import ServicioComparadorArchivos
from secure_api.services.decryption_service import ServicioDesencriptacion
from secure_api.services.file_processor import ProcesadorArchivos

router = APIRouter(prefix="/proteccion-datos", tags=["Proteccion Datos"])


def _media_type_por_extension(ruta: Path) -> str:
    ext = ruta.suffix.lower()
    if ext == ".xlsx":
        return (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    if ext == ".xls":
        return "application/vnd.ms-excel"
    if ext == ".csv":
        return "text/csv; charset=utf-8"
    return "application/octet-stream"


@router.post("/subir-archivo", status_code=status.HTTP_201_CREATED)
async def subir_archivo(
    archivo: UploadFile = File(...),
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    if not archivo.filename:
        raise HTTPException(status_code=400, detail="Archivo invalido")

    extension = Path(archivo.filename).suffix.lower()
    if extension not in {".csv", ".xlsx", ".xls"}:
        raise HTTPException(status_code=400, detail="Solo se permiten CSV y Excel")

    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="Archivo vacio")

    procesador = ProcesadorArchivos()
    ruta_guardada = procesador.guardar_archivo_subido(contenido, archivo.filename)

    archivo_db = Archivo(
        id_usuario=usuario_actual.id,
        nombre_original=procesador.sanitizar_nombre_archivo(archivo.filename),
        ruta_archivo_original=str(ruta_guardada),
        estado="subido",
    )
    db.add(archivo_db)
    await db.flush()

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="subir_archivo",
        id_usuario=usuario_actual.id,
        detalle={"id_archivo": archivo_db.id, "nombre": archivo_db.nombre_original},
    )
    return {"id_archivo": archivo_db.id, "nombre_archivo": archivo_db.nombre_original}


@router.post("/analizar-archivo", response_model=AnalisisArchivoResponse)
async def analizar_archivo(
    id_archivo: str,
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AnalisisArchivoResponse:
    consulta = await db.execute(
        select(Archivo).where(
            Archivo.id == id_archivo, Archivo.id_usuario == usuario_actual.id
        )
    )
    archivo_db = consulta.scalar_one_or_none()
    if not archivo_db:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    procesador = ProcesadorArchivos()
    resultado = procesador.analizar_archivo(archivo_db.ruta_archivo_original)
    archivo_db.total_columnas_sensibles = len(resultado["columnas_sensibles"])
    archivo_db.estado = "analizado"

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="analizar_archivo",
        id_usuario=usuario_actual.id,
        detalle={
            "id_archivo": archivo_db.id,
            "total_columnas_sensibles": archivo_db.total_columnas_sensibles,
        },
    )
    return AnalisisArchivoResponse(id_archivo=archivo_db.id, **resultado)


@router.post("/procesar-archivo", response_model=ProcesarArchivoResponse)
async def procesar_archivo(
    payload: ProcesarArchivoRequest,
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProcesarArchivoResponse:
    consulta = await db.execute(
        select(Archivo).where(
            Archivo.id == payload.id_archivo, Archivo.id_usuario == usuario_actual.id
        )
    )
    archivo_db = consulta.scalar_one_or_none()
    if not archivo_db:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    if not payload.configuraciones:
        raise HTTPException(status_code=400, detail="Debe enviar configuraciones")

    procesador = ProcesadorArchivos()
    nombre_salida = f"procesado_{archivo_db.nombre_original}"
    ruta_salida = procesador.procesar_archivo(
        archivo_db.ruta_archivo_original,
        [item.model_dump() for item in payload.configuraciones],
        nombre_salida,
        clave_usuario=payload.clave_usuario,
    )

    meta_lateral = ProcesadorArchivos.obtener_ruta_metadata(ruta_salida)
    if meta_lateral.exists():
        respaldo = meta_lateral.parent / f"{archivo_db.id}.meta.json"
        shutil.copy2(meta_lateral, respaldo)

    archivo_db.ruta_archivo_procesado = str(ruta_salida)
    archivo_db.estado = "procesado"

    for item in payload.configuraciones:
        db.add(
            ConfiguracionEncriptacion(
                id_archivo=archivo_db.id,
                nombre_columna=item.columna,
                tipo_proteccion=item.tipo_proteccion,
                algoritmo=item.tipo_proteccion,
            )
        )

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="procesar_archivo",
        id_usuario=usuario_actual.id,
        detalle={
            "id_archivo": archivo_db.id,
            "configuraciones": [item.model_dump() for item in payload.configuraciones],
        },
    )

    return ProcesarArchivoResponse(
        id_archivo=archivo_db.id,
        estado=archivo_db.estado,
        nombre_archivo_procesado=Path(ruta_salida).name,
    )


@router.get("/descargar-archivo/{id_archivo}")
async def descargar_archivo(
    id_archivo: str,
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    consulta = await db.execute(
        select(Archivo).where(
            Archivo.id == id_archivo, Archivo.id_usuario == usuario_actual.id
        )
    )
    archivo_db = consulta.scalar_one_or_none()
    if not archivo_db or not archivo_db.ruta_archivo_procesado:
        raise HTTPException(status_code=404, detail="Archivo procesado no encontrado")

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="descargar_archivo",
        id_usuario=usuario_actual.id,
        detalle={"id_archivo": id_archivo},
    )

    return FileResponse(
        path=archivo_db.ruta_archivo_procesado,
        filename=Path(archivo_db.ruta_archivo_procesado).name,
        media_type="application/octet-stream",
    )


@router.post("/desencriptar-archivo")
async def desencriptar_archivo(
    payload: DesencriptarArchivoRequest,
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    consulta = await db.execute(
        select(Archivo).where(
            Archivo.id == payload.id_archivo, Archivo.id_usuario == usuario_actual.id
        )
    )
    archivo_db = consulta.scalar_one_or_none()
    if not archivo_db or not archivo_db.ruta_archivo_procesado:
        raise HTTPException(status_code=404, detail="Archivo procesado no encontrado")

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="desencriptar_archivo_inicio",
        id_usuario=usuario_actual.id,
        detalle={"id_archivo": payload.id_archivo},
    )

    if payload.configuraciones:
        configuracion_desencriptar = [item.model_dump() for item in payload.configuraciones]
    else:
        consulta_conf = await db.execute(
            select(ConfiguracionEncriptacion).where(
                ConfiguracionEncriptacion.id_archivo == payload.id_archivo
            )
        )
        filas_conf = consulta_conf.scalars().all()
        por_columna: dict[str, dict[str, str]] = {}
        for fila in filas_conf:
            por_columna[fila.nombre_columna] = {
                "columna": fila.nombre_columna,
                "tipo_proteccion": fila.tipo_proteccion,
            }
        configuracion_desencriptar = list(por_columna.values()) if por_columna else None

    try:
        servicio_desencriptacion = ServicioDesencriptacion()
        ruta_desencriptada = servicio_desencriptacion.desencriptar_archivo(
            ruta_archivo=archivo_db.ruta_archivo_procesado,
            clave_usuario=payload.clave_usuario,
            configuracion=configuracion_desencriptar,
            id_archivo=payload.id_archivo,
        )
    finally:
        # Manejo seguro de memoria: eliminar referencia de clave.
        payload.clave_usuario = ""

    await auditoria.registrar_evento(
        accion="desencriptar_archivo_fin",
        id_usuario=usuario_actual.id,
        detalle={
            "id_archivo": payload.id_archivo,
            "columnas_procesadas": len(payload.configuraciones or []),
        },
    )
    ruta_path = Path(ruta_desencriptada)
    return FileResponse(
        path=str(ruta_desencriptada),
        filename=ruta_path.name,
        media_type=_media_type_por_extension(ruta_path),
    )


@router.post("/comparar-archivos", response_model=CompararArchivosResponse)
async def comparar_archivos(
    archivo_original: UploadFile = File(...),
    archivo_desencriptado: UploadFile = File(...),
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CompararArchivosResponse:
    procesador = ProcesadorArchivos()
    extension_1 = Path(archivo_original.filename or "").suffix.lower()
    extension_2 = Path(archivo_desencriptado.filename or "").suffix.lower()
    permitidas = {".csv", ".xlsx", ".xls"}
    if extension_1 not in permitidas or extension_2 not in permitidas:
        raise HTTPException(status_code=400, detail="Solo se permiten CSV y Excel")

    contenido_original = await archivo_original.read()
    contenido_desencriptado = await archivo_desencriptado.read()
    ruta_original = procesador.guardar_archivo_subido(
        contenido_original, f"comparacion_original_{archivo_original.filename}"
    )
    ruta_desencriptado = procesador.guardar_archivo_subido(
        contenido_desencriptado,
        f"comparacion_desencriptado_{archivo_desencriptado.filename}",
    )

    auditoria = ServicioAuditoria(db)
    await auditoria.registrar_evento(
        accion="comparar_archivos_inicio",
        id_usuario=usuario_actual.id,
        detalle={"archivo_original": archivo_original.filename or "sin_nombre"},
    )
    comparador = ServicioComparadorArchivos()
    resultado = comparador.comparar_archivos(str(ruta_original), str(ruta_desencriptado))
    await auditoria.registrar_evento(
        accion="comparar_archivos_fin",
        id_usuario=usuario_actual.id,
        detalle={
            "coincidencia": resultado["coincidencia"],
            "filas_diferentes": resultado["filas_diferentes"],
        },
    )
    return CompararArchivosResponse(**resultado)


@router.get("/logs-auditoria", response_model=list[LogAuditoriaResponse])
async def logs_auditoria(
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[LogAuditoriaResponse]:
    consulta = await db.execute(
        select(LogAuditoria)
        .where(LogAuditoria.id_usuario == usuario_actual.id)
        .order_by(LogAuditoria.fecha_evento.desc())
        .limit(100)
    )
    logs = consulta.scalars().all()
    return [
        LogAuditoriaResponse(
            accion=log.accion,
            nivel=log.nivel,
            detalle=_sanitizar_detalle(log.detalle),
            fecha_evento=log.fecha_evento,
        )
        for log in logs
    ]


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(
    usuario_actual: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardResponse:
    total_archivos = await db.scalar(
        select(func.count(Archivo.id)).where(
            Archivo.id_usuario == usuario_actual.id, Archivo.estado == "procesado"
        )
    )
    total_sensibles = await db.scalar(
        select(func.coalesce(func.sum(Archivo.total_columnas_sensibles), 0)).where(
            Archivo.id_usuario == usuario_actual.id
        )
    )
    consulta_tipos = await db.execute(
        select(
            ConfiguracionEncriptacion.tipo_proteccion,
            func.count(ConfiguracionEncriptacion.id),
        )
        .join(Archivo, ConfiguracionEncriptacion.id_archivo == Archivo.id)
        .where(Archivo.id_usuario == usuario_actual.id)
        .group_by(ConfiguracionEncriptacion.tipo_proteccion)
    )
    tipos = {fila[0]: int(fila[1]) for fila in consulta_tipos.all()}
    return DashboardResponse(
        archivos_procesados=int(total_archivos or 0),
        datos_sensibles_detectados=int(total_sensibles or 0),
        tipos_encriptacion_usados=tipos,
    )


def _sanitizar_detalle(detalle: str) -> str:
    try:
        contenido = json.loads(detalle)
    except Exception:
        return detalle
    for campo in ("clave", "token", "password", "secret"):
        if campo in contenido:
            contenido[campo] = "***"
    return json.dumps(contenido, ensure_ascii=True)
