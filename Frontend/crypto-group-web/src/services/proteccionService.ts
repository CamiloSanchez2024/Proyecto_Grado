import { api } from '@/services/api'
import type {
  AnalisisArchivoResponse,
  CompararArchivosResponse,
  DashboardResponse,
  DesencriptarArchivoRequest,
  LogAuditoriaResponse,
  ProcesarArchivoRequest,
  ProcesarArchivoResponse,
  SubirArchivoResponse,
} from '@/types/proteccion.types'
import { parseFilenameFromContentDisposition } from '@/lib/utils'

export async function subirArchivo(file: File): Promise<SubirArchivoResponse> {
  const form = new FormData()
  form.append('archivo', file)
  const { data } = await api.post<SubirArchivoResponse>('/proteccion-datos/subir-archivo', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function analizarArchivo(idArchivo: string): Promise<AnalisisArchivoResponse> {
  const { data } = await api.post<AnalisisArchivoResponse>(
    `/proteccion-datos/analizar-archivo?id_archivo=${encodeURIComponent(idArchivo)}`,
  )
  return data
}

export async function obtenerDashboard(): Promise<DashboardResponse> {
  const { data } = await api.get<DashboardResponse>('/proteccion-datos/dashboard')
  return data
}

export async function procesarArchivo(body: ProcesarArchivoRequest): Promise<ProcesarArchivoResponse> {
  const { data } = await api.post<ProcesarArchivoResponse>('/proteccion-datos/procesar-archivo', body)
  return data
}

export async function descargarArchivo(idArchivo: string): Promise<{ blob: Blob; filename: string | null }> {
  const res = await api.get<Blob>(`/proteccion-datos/descargar-archivo/${encodeURIComponent(idArchivo)}`, {
    responseType: 'blob',
  })
  const cd = res.headers['content-disposition'] ?? res.headers['Content-Disposition']
  const filename = parseFilenameFromContentDisposition(
    typeof cd === 'string' ? cd : Array.isArray(cd) ? cd[0] ?? null : null,
  )
  return { blob: res.data, filename }
}

export async function desencriptarArchivo(
  body: DesencriptarArchivoRequest,
): Promise<{ blob: Blob; filename: string | null }> {
  const res = await api.post<Blob>('/proteccion-datos/desencriptar-archivo', body, {
    responseType: 'blob',
  })
  const contentType = res.headers['content-type'] ?? ''
  if (typeof contentType === 'string' && contentType.includes('application/json')) {
    const text = await res.data.text()
    const err = JSON.parse(text) as { detail?: string }
    throw new Error(err.detail ?? 'Error al desencriptar')
  }
  const cd = res.headers['content-disposition'] ?? res.headers['Content-Disposition']
  const filename = parseFilenameFromContentDisposition(
    typeof cd === 'string' ? cd : Array.isArray(cd) ? cd[0] ?? null : null,
  )
  return { blob: res.data, filename }
}

export async function compararArchivos(original: File, desencriptado: File): Promise<CompararArchivosResponse> {
  const form = new FormData()
  form.append('archivo_original', original)
  form.append('archivo_desencriptado', desencriptado)
  const { data } = await api.post<CompararArchivosResponse>('/proteccion-datos/comparar-archivos', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function logsAuditoria(): Promise<LogAuditoriaResponse[]> {
  const { data } = await api.get<LogAuditoriaResponse[]>('/proteccion-datos/logs-auditoria')
  return data
}

export function triggerDownload(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
