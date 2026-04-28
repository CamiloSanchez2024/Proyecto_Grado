import { useCallback, useEffect, useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { MetricCard } from '@/components/common/MetricCard'
import { Button } from '@/components/ui/Button'
import * as proteccionService from '@/services/proteccionService'

const quickActions = [
  {
    title: 'Cargar archivo',
    description: 'Sube nuevos documentos para su analisis y proteccion.',
    to: '/app/cargar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M7 16.5a4.5 4.5 0 0 1 .85-8.92A5.5 5.5 0 0 1 18.5 9a4 4 0 1 1 .5 8h-3.5" />
        <path strokeLinecap="round" strokeLinejoin="round" d="m12 18 0-8m0 0-3 3m3-3 3 3" />
      </svg>
    ),
    iconClass: 'bg-blue-50 text-blue-600',
  },
  {
    title: 'Detectar datos',
    description: 'Identifica informacion sensible automaticamente.',
    to: '/app/detectar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-4.35-4.35" />
        <circle cx="11" cy="11" r="6.25" />
      </svg>
    ),
    iconClass: 'bg-emerald-50 text-emerald-600',
  },
  {
    title: 'Configurar encriptacion',
    description: 'Define algoritmos y politicas de seguridad.',
    to: '/app/configurar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 3.5h3l.7 2.2a7 7 0 0 1 2.14 1.24l2.2-.68 1.5 2.6-1.8 1.45a7.45 7.45 0 0 1 0 2.48l1.8 1.45-1.5 2.6-2.2-.68a7 7 0 0 1-2.14 1.24l-.7 2.2h-3l-.7-2.2a7 7 0 0 1-2.14-1.24l-2.2.68-1.5-2.6 1.8-1.45a7.45 7.45 0 0 1 0-2.48l-1.8-1.45 1.5-2.6 2.2.68A7 7 0 0 1 9.8 5.7l.7-2.2Z" />
        <circle cx="12" cy="12" r="2.5" />
      </svg>
    ),
    iconClass: 'bg-violet-50 text-violet-600',
  },
  {
    title: 'Procesar archivo',
    description: 'Ejecuta las tareas de proteccion programadas.',
    to: '/app/procesar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <circle cx="12" cy="12" r="8" />
        <path strokeLinecap="round" strokeLinejoin="round" d="m10 9 5 3-5 3V9Z" />
      </svg>
    ),
    iconClass: 'bg-slate-100 text-slate-600',
  },
  {
    title: 'Desencriptar',
    description: 'Recupera la informacion original con tus llaves.',
    to: '/app/desencriptar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <rect x="4.25" y="10" width="15.5" height="10" rx="2.25" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M8 10V7.75a4 4 0 1 1 8 0" />
      </svg>
    ),
    iconClass: 'bg-amber-50 text-amber-600',
  },
  {
    title: 'Comparar archivos',
    description: 'Analiza diferencias entre versiones de archivos.',
    to: '/app/comparar',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 4.75h10.5v14.5H6.75z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9h4.5M9.75 12h4.5M9.75 15h3" />
      </svg>
    ),
    iconClass: 'bg-pink-50 text-pink-600',
  },
  {
    title: 'Logs auditoria',
    description: 'Registro detallado de las operaciones realizadas.',
    to: '/app/logs',
    icon: (
      <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <circle cx="12" cy="12" r="7.5" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8.5v4l2.75 1.75" />
      </svg>
    ),
    iconClass: 'bg-indigo-50 text-indigo-600',
  },
] as const

const DASHBOARD_ACTIONS_STORAGE_KEY = 'dashboard.quick-actions.v1'
const allActionIds: string[] = quickActions.map((action) => action.to)

export function DashboardPage() {
  const [isCustomizeOpen, setIsCustomizeOpen] = useState(false)
  const [visibleActionIds, setVisibleActionIds] = useState<string[]>(() => {
    if (typeof window === 'undefined') {
      return allActionIds
    }

    try {
      const storedValue = window.localStorage.getItem(DASHBOARD_ACTIONS_STORAGE_KEY)
      if (!storedValue) return allActionIds

      const parsed = JSON.parse(storedValue) as unknown
      if (!Array.isArray(parsed)) return allActionIds

      const validIds = parsed.filter(
        (value): value is string => typeof value === 'string' && allActionIds.includes(value),
      )

      return validIds.length > 0 ? validIds : allActionIds
    } catch {
      return allActionIds
    }
  })

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

  const visibleQuickActions = useMemo(
    () => quickActions.filter((action) => visibleActionIds.includes(action.to)),
    [visibleActionIds],
  )

  const toggleActionVisibility = useCallback((actionId: string) => {
    setVisibleActionIds((current) => {
      if (current.includes(actionId)) {
        if (current.length === 1) return current
        return current.filter((id) => id !== actionId)
      }

      return [...current, actionId]
    })
  }, [])

  const showAllActions = useCallback(() => {
    setVisibleActionIds(allActionIds)
  }, [])

  useEffect(() => {
    window.localStorage.setItem(DASHBOARD_ACTIONS_STORAGE_KEY, JSON.stringify(visibleActionIds))
  }, [visibleActionIds])

  return (
    <div className="space-y-7">
      <section>
        <h2 className="text-3xl font-semibold tracking-tight text-[var(--color-text-primary)]">Bienvenido al Panel de Control</h2>
        <p className="mt-1 text-[15px] text-[var(--color-text-secondary)]">
          Gestione la seguridad y procesamiento de sus datos desde una vista centralizada.
        </p>
      </section>

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
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)]">Desglose por tipo</p>
          <p className="mt-2 font-mono text-sm text-[var(--color-text-primary)]">{tipos || '—'}</p>
        </div>
      ) : null}

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {visibleQuickActions.map((action) => (
          <Link
            key={action.to}
            to={action.to}
            className="group rounded-2xl border border-[var(--color-border-default)] bg-white p-6 shadow-sm transition-all hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
          >
            <div className={`mb-6 inline-flex h-14 w-14 items-center justify-center rounded-full ${action.iconClass}`}>
              {action.icon}
            </div>
            <h3 className="text-[28px]/8 font-semibold tracking-tight text-[var(--color-text-primary)] sm:text-2xl">
              {action.title}
            </h3>
            <p className="mt-2 text-sm text-[var(--color-text-secondary)]">{action.description}</p>
          </Link>
        ))}

        <button
          type="button"
          onClick={() => setIsCustomizeOpen((current) => !current)}
          className="rounded-2xl border border-dashed border-[var(--color-border-default)] bg-white p-6 text-center text-[var(--color-text-muted)] transition-colors hover:border-slate-300 hover:text-[var(--color-text-secondary)]"
        >
          <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-3xl leading-none">+</div>
          <p className="text-xs font-semibold uppercase tracking-wider">
            {isCustomizeOpen ? 'Cerrar personalizacion' : 'Personalizar panel'}
          </p>
        </button>
      </section>

      {isCustomizeOpen ? (
        <section className="rounded-2xl border border-[var(--color-border-default)] bg-white p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">Personalizar panel</h3>
              <p className="text-sm text-[var(--color-text-secondary)]">
                Seleccione los accesos rapidos que desea ver en su dashboard.
              </p>
            </div>

            <Button type="button" variant="secondary" onClick={showAllActions}>
              Mostrar todos
            </Button>
          </div>

          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {quickActions.map((action) => (
              <label
                key={`visibility-${action.to}`}
                className="flex cursor-pointer items-start gap-3 rounded-xl border border-[var(--color-border-default)] p-3 transition-colors hover:border-slate-300"
              >
                <input
                  type="checkbox"
                  className="mt-1 h-4 w-4 accent-blue-600"
                  checked={visibleActionIds.includes(action.to)}
                  onChange={() => toggleActionVisibility(action.to)}
                />
                <span>
                  <span className="block text-sm font-semibold text-[var(--color-text-primary)]">{action.title}</span>
                  <span className="block text-xs text-[var(--color-text-secondary)]">{action.description}</span>
                </span>
              </label>
            ))}
          </div>
          <p className="mt-4 text-xs text-[var(--color-text-muted)]">
            Debe mantener al menos un acceso rapido visible.
          </p>
        </section>
      ) : null}

      <div className="flex justify-end">
        <Link to="/app/cargar">
          <Button type="button">Siguiente: Cargar archivo</Button>
        </Link>
      </div>
    </div>
  )
}
