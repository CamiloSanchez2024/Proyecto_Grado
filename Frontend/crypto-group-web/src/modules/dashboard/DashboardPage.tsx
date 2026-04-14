import { useQuery } from '@tanstack/react-query'
import { MetricCard } from '@/components/common/MetricCard'
import * as proteccionService from '@/services/proteccionService'

export function DashboardPage() {
  const q = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => proteccionService.obtenerDashboard(),
  })

  const d = q.data ?? {
    archivos_procesados: 0,
    datos_sensibles_detectados: 0,
    tipos_encriptacion_usados: {} as Record<string, number>,
  }

  const tipos = Object.entries(d.tipos_encriptacion_usados)
    .map(([k, v]) => `${k}: ${v}`)
    .join(', ')

  return (
    <div className="space-y-6">
      {q.isError ? (
        <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
          <p className="text-sm text-amber-700">No se pudo cargar el dashboard. Mostrando valores en cero.</p>
        </div>
      ) : null}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <MetricCard label="Archivos procesados" value={d.archivos_procesados} accent="blue" />
        <MetricCard label="Datos sensibles detectados" value={d.datos_sensibles_detectados} accent="emerald" />
        <MetricCard
          label="Tipos de encriptación (total)"
          value={Object.values(d.tipos_encriptacion_usados).reduce((a, b) => a + b, 0)}
          accent="violet"
        />
      </div>

      {tipos ? (
        <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
          <p className="text-sm font-medium text-[var(--color-text-secondary)]">Desglose por tipo</p>
          <p className="mt-2 font-mono text-sm text-[var(--color-text-primary)]">{tipos || '—'}</p>
        </div>
      ) : null}
    </div>
  )
}
