import axios from 'axios'
import type { ApiErrorBody } from '@/types/common.types'

export function cn(...parts: (string | false | undefined | null)[]): string {
  return parts.filter(Boolean).join(' ')
}

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as ApiErrorBody | undefined
    const detail = data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      return detail.map((d) => (typeof d === 'object' && d && 'msg' in d ? String(d.msg) : JSON.stringify(d))).join(
        '; ',
      )
    }
    return error.message
  }
  if (error instanceof Error) return error.message
  return String(error)
}

/** Parse filename from Content-Disposition header */
export function parseFilenameFromContentDisposition(header: string | null): string | null {
  if (!header) return null
  const utf8 = /filename\*=UTF-8''([^;]+)/i.exec(header)
  if (utf8?.[1]) {
    try {
      return decodeURIComponent(utf8[1].replace(/"/g, '').trim())
    } catch {
      return utf8[1]
    }
  }
  const simple = /filename="?([^";\n]+)"?/i.exec(header)
  return simple?.[1]?.trim() ?? null
}

/**
 * Nombre de archivo al descargar un blob cuando el header Content-Disposition
 * no está disponible (p. ej. CORS antes de expose_headers): evita guardar un
 * .xlsx como .csv (firma ZIP "PK").
 */
export async function resolveDownloadFilename(
  blob: Blob,
  headerFilename: string | null,
  baseName = 'desencriptado',
): Promise<string> {
  const fromHeader = headerFilename?.trim()
  if (fromHeader) return fromHeader
  const head = new Uint8Array(await blob.slice(0, 8).arrayBuffer())
  if (head.length >= 2 && head[0] === 0x50 && head[1] === 0x4b) {
    return `${baseName}.xlsx`
  }
  if (
    head.length >= 8 &&
    head[0] === 0xd0 &&
    head[1] === 0xcf &&
    head[2] === 0x11 &&
    head[3] === 0xe0
  ) {
    return `${baseName}.xls`
  }
  return `${baseName}.csv`
}
