import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import * as proteccionService from '@/services/proteccionService'
import type { LogAuditoriaResponse } from '@/types/proteccion.types'

function nivelTone(n: string): 'info' | 'warning' | 'error' {
  const u = n.toUpperCase()
  if (u.includes('ERROR')) return 'error'
  if (u.includes('WARN')) return 'warning'
  return 'info'
}

export function AuditLogsPage() {
  const [buscar, setBuscar] = useState('')
  const [nivel, setNivel] = useState<string>('TODOS')

  const q = useQuery({
    queryKey: ['logs-auditoria'],
    queryFn: () => proteccionService.logsAuditoria(),
  })

  const filtrados = useMemo(() => {
    let rows: LogAuditoriaResponse[] = q.data ?? []
    const t = buscar.trim().toLowerCase()
    if (t) {
      rows = rows.filter(
        (r) =>
          r.accion.toLowerCase().includes(t) ||
          r.detalle.toLowerCase().includes(t) ||
          r.nivel.toLowerCase().includes(t),
      )
    }
    if (nivel !== 'TODOS') {
      rows = rows.filter((r) => r.nivel.toUpperCase().includes(nivel))
    }
    return rows
  }, [q.data, buscar, nivel])

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-3">
        <Input label="Buscar…" value={buscar} onChange={(e) => setBuscar(e.target.value)} className="min-w-[200px]" />
        <label className="flex flex-col gap-1.5">
          <span className="text-sm font-medium text-[var(--color-text-secondary)]">Nivel</span>
          <select
            className="rounded-lg border border-[var(--color-border-default)] bg-white px-3 py-2 text-sm text-[var(--color-text-primary)] outline-none focus:border-[var(--color-accent)] focus:ring-1 ring-[var(--color-accent)]"
            value={nivel}
            onChange={(e) => setNivel(e.target.value)}
          >
            {['TODOS', 'INFO', 'WARNING', 'ERROR'].map((x) => (
              <option key={x} value={x}>
                {x}
              </option>
            ))}
          </select>
        </label>
        <Button type="button" onClick={() => void q.refetch()}>
          Aplicar filtros
        </Button>
      </div>

      <p className="text-sm text-[var(--color-text-muted)]">
        Mostrando {filtrados.length} eventos
        {q.isFetching ? ' (actualizando…)' : ''}
      </p>

      <div className="overflow-hidden rounded-xl border border-[var(--color-border-default)] bg-white">
        <div className="max-h-[480px] overflow-auto">
          {q.isError ? (
            <p className="p-4 text-sm text-red-600">Error al cargar logs</p>
          ) : filtrados.length === 0 ? (
            <p className="p-4 text-sm text-[var(--color-text-muted)]">Sin resultados</p>
          ) : (
            <table className="w-full table-fixed border-collapse text-left">
              <thead className="sticky top-0 z-[1] border-b border-[var(--color-border-default)] bg-[var(--color-surface)]">
                <tr>
                  <th className="w-[18%] min-w-0 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
                    Fecha
                  </th>
                  <th className="w-[12%] min-w-0 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
                    Nivel
                  </th>
                  <th className="w-[22%] min-w-0 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
                    Acción
                  </th>
                  <th className="min-w-0 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
                    Detalle
                  </th>
                </tr>
              </thead>
              <tbody>
                {filtrados.map((r, i) => (
                  <tr
                    key={`${r.fecha_evento}-${i}`}
                    className="border-b border-[var(--color-border-subtle)] transition-colors hover:bg-[var(--color-surface)]"
                  >
                    <td className="min-w-0 align-top px-4 py-3 text-sm text-[var(--color-text-secondary)]">
                      <span className="block break-words">{r.fecha_evento}</span>
                    </td>
                    <td className="min-w-0 align-top px-4 py-3">
                      <Badge tone={nivelTone(r.nivel)}>{r.nivel}</Badge>
                    </td>
                    <td className="min-w-0 align-top px-4 py-3 text-sm font-medium text-[var(--color-text-primary)]">
                      <span className="block break-words">{r.accion}</span>
                    </td>
                    <td className="min-w-0 align-top px-4 py-3 font-mono text-xs text-[var(--color-text-secondary)]">
                      <span className="block break-all [overflow-wrap:anywhere]">{r.detalle}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
