import { Outlet, useLocation } from 'react-router-dom'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { useLogout } from '@/hooks/useAuth'
import { useAuthStore } from '@/stores/authStore'

const titles: Record<string, { title: string; subtitle?: string }> = {
  '/app/inicio': { title: 'Inicio', subtitle: 'Métricas del sistema' },
  '/app/cargar': { title: 'Cargar archivo', subtitle: 'Sube CSV o Excel' },
  '/app/detectar': { title: 'Detectar datos', subtitle: 'Revisión y columnas sensibles' },
  '/app/configurar': { title: 'Configurar encriptación', subtitle: 'Protección por columna' },
  '/app/procesar': { title: 'Procesar archivo', subtitle: 'Aplicar protecciones' },
  '/app/desencriptar': { title: 'Desencriptar archivo', subtitle: 'Revertir AES / token / pseudónimo' },
  '/app/comparar': { title: 'Comparar archivos', subtitle: 'Integridad original vs desencriptado' },
  '/app/logs': { title: 'Logs de auditoría', subtitle: 'Trazabilidad' },
}

export function AppLayout() {
  const loc = useLocation()
  const meta = titles[loc.pathname] ?? { title: 'CryptoUGroup' }
  const username = useAuthStore((s) => s.username)
  const logout = useLogout()

  return (
    <div className="flex min-h-screen bg-[var(--color-surface)]">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header title={meta.title} subtitle={meta.subtitle} username={username} onLogout={logout} />
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
