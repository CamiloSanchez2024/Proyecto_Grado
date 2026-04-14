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

export function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <aside className="flex w-60 shrink-0 flex-col bg-[#0D1B4B] text-white">
      <div className="flex items-center gap-3 px-5 py-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/15 text-sm font-bold">
          G
        </div>
        <div>
          <span className="text-sm font-semibold tracking-tight">CryptoUGroup</span>
          <p className="text-[11px] text-white/60">Protección de datos</p>
        </div>
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
                isActive
                  ? 'bg-white/15 font-medium text-white border-l-2 border-white'
                  : 'text-white/70 hover:bg-white/10 hover:text-white',
              )
            }
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
