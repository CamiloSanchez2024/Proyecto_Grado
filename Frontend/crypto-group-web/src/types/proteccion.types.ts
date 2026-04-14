export const TIPOS_PROTECCION = [
  'aes-256',
  'hashing',
  'tokenizacion',
  'pseudonimizacion',
  'anonimizacion',
] as const

export type TipoProteccion = (typeof TIPOS_PROTECCION)[number]

export interface ColumnaSensibleItem {
  columna: string
  puntaje?: number
  clasificacion?: string
  evidencia?: string[]
}

export interface AnalisisArchivoResponse {
  id_archivo: string
  columnas: string[]
  columnas_sensibles: ColumnaSensibleItem[]
  total_filas: number
}

export interface ConfiguracionProteccionItem {
  columna: string
  tipo_proteccion: TipoProteccion | string
}

export interface ProcesarArchivoRequest {
  id_archivo: string
  configuraciones: ConfiguracionProteccionItem[]
  clave_usuario?: string | null
}

export interface ProcesarArchivoResponse {
  id_archivo: string
  estado: string
  nombre_archivo_procesado: string
}

export interface SubirArchivoResponse {
  id_archivo: string
  nombre_archivo: string
}

export interface DashboardResponse {
  archivos_procesados: number
  datos_sensibles_detectados: number
  tipos_encriptacion_usados: Record<string, number>
}

export interface LogAuditoriaResponse {
  accion: string
  nivel: string
  detalle: string
  fecha_evento: string
}

export interface DesencriptarArchivoRequest {
  id_archivo: string
  clave_usuario: string
  configuraciones?: ConfiguracionProteccionItem[]
}

export interface CompararArchivosResponse {
  coincidencia: number
  filas_iguales: number
  filas_diferentes: number
  columnas_con_error: string[]
  detalle: Record<string, unknown>[]
}
