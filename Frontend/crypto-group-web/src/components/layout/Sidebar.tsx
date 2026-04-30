import { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import { cn } from '@/lib/utils'

const items = [
  { to: '/app/inicio', label: 'Inicio', icon: '📊' },
  { to: '/app/cargar', label: 'Cargar archivo', icon: '📁' },
  { to: '/app/detectar', label: 'Detectar datos', icon: '🔍' },
  { to: '/app/configurar', label: 'Configurar encriptación', icon: '⚙️' },
  { to: '/app/procesar', label: 'Procesar archivo', icon: '▶️' },
  { to: '/app/desencriptar', label: 'Desencriptar', icon: '🔓' },
  { to: '/app/comparar', label: 'Comparar archivos', icon: '📄' },
  { to: '/app/logs', label: 'Logs auditoría', icon: '📋' },
] as const

const SIDEBAR_COLLAPSED_STORAGE_KEY = 'app.sidebar.collapsed'

export function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  const [isCollapsed, setIsCollapsed] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false
    return window.localStorage.getItem(SIDEBAR_COLLAPSED_STORAGE_KEY) === 'true'
  })

  useEffect(() => {
    window.localStorage.setItem(SIDEBAR_COLLAPSED_STORAGE_KEY, String(isCollapsed))
  }, [isCollapsed])

  return (
    <aside className={cn('flex shrink-0 flex-col bg-[#0D1B4B] text-white transition-all', isCollapsed ? 'w-20' : 'w-60')}>
      <div className={cn('flex items-center px-5 py-5', isCollapsed ? 'justify-center' : 'gap-3')}>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/15 text-sm font-bold">
          G
        </div>
        {!isCollapsed ? (
          <div>
            <span className="text-sm font-semibold tracking-tight">CryptoUGroup</span>
            <p className="text-[11px] text-white/60">Protección de datos</p>
          </div>
        ) : null}
      </div>

      <div className={cn('px-3', isCollapsed ? 'pb-2' : 'pb-3')}>
        <button
          type="button"
          onClick={() => setIsCollapsed((current) => !current)}
          className={cn(
            'group w-full rounded-xl border border-white/15 bg-white/10 text-white shadow-sm transition-all hover:border-white/30 hover:bg-white/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60',
            isCollapsed ? 'flex h-10 items-center justify-center' : 'flex items-center justify-between px-3 py-2.5',
          )}
          title={isCollapsed ? 'Expandir menú lateral' : 'Contraer menú lateral'}
          aria-label={isCollapsed ? 'Expandir menú lateral' : 'Contraer menú lateral'}
        >
          {!isCollapsed ? <span className="text-xs font-medium tracking-wide text-white/90">Contraer menú</span> : null}
          <span
            className={cn(
              'inline-flex h-6 w-6 items-center justify-center rounded-full bg-white/15 transition-transform duration-200',
              !isCollapsed && 'rotate-180',
            )}
            aria-hidden="true"
          >
            <svg viewBox="0 0 20 20" fill="none" className="h-3.5 w-3.5 text-white/95">
              <path d="M12.5 4.5 7 10l5.5 5.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
        </button>
      </div>

      <nav className="mt-2 flex flex-1 flex-col gap-0.5 px-3">
        {items.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors',
                isCollapsed && 'justify-center px-2',
                isActive
                  ? 'bg-white/15 font-medium text-white border-l-2 border-white'
                  : 'text-white/70 hover:bg-white/10 hover:text-white',
              )
            }
            title={item.label}
            aria-label={item.label}
          >
            <span className="text-base">{item.icon}</span>
            {!isCollapsed ? item.label : null}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
