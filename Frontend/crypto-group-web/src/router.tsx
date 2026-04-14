import { lazy, Suspense, type ReactNode } from 'react'
import { createBrowserRouter, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { AppLayout } from '@/components/layout/AppLayout'

const LoginPage = lazy(() =>
  import('@/modules/auth/LoginPage').then((m) => ({ default: m.LoginPage })),
)
const RegisterPage = lazy(() =>
  import('@/modules/auth/RegisterPage').then((m) => ({ default: m.RegisterPage })),
)
const DashboardPage = lazy(() =>
  import('@/modules/dashboard/DashboardPage').then((m) => ({ default: m.DashboardPage })),
)
const UploadPage = lazy(() =>
  import('@/modules/upload/UploadPage').then((m) => ({ default: m.UploadPage })),
)
const DetectionPage = lazy(() =>
  import('@/modules/detection/DetectionPage').then((m) => ({ default: m.DetectionPage })),
)
const ConfigurationPage = lazy(() =>
  import('@/modules/configuration/ConfigurationPage').then((m) => ({ default: m.ConfigurationPage })),
)
const ProcessingPage = lazy(() =>
  import('@/modules/processing/ProcessingPage').then((m) => ({ default: m.ProcessingPage })),
)
const DecryptionPage = lazy(() =>
  import('@/modules/decryption/DecryptionPage').then((m) => ({ default: m.DecryptionPage })),
)
const ComparisonPage = lazy(() =>
  import('@/modules/comparison/ComparisonPage').then((m) => ({ default: m.ComparisonPage })),
)
const AuditLogsPage = lazy(() =>
  import('@/modules/audit/AuditLogsPage').then((m) => ({ default: m.AuditLogsPage })),
)

function RootRedirect() {
  const token = useAuthStore((s) => s.accessToken)
  return <Navigate to={token ? '/app/inicio' : '/login'} replace />
}

function lazyWrap(node: ReactNode) {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-[40vh] items-center justify-center text-[var(--color-text-muted)]">
          Cargando…
        </div>
      }
    >
      {node}
    </Suspense>
  )
}

function RequireAuth({ children }: { children: ReactNode }) {
  const token = useAuthStore((s) => s.accessToken)
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

export const router = createBrowserRouter([
  { path: '/', element: <RootRedirect /> },
  {
    path: '/login',
    element: lazyWrap(<LoginPage />),
  },
  {
    path: '/register',
    element: lazyWrap(<RegisterPage />),
  },
  {
    path: '/app',
    element: (
      <RequireAuth>
        <AppLayout />
      </RequireAuth>
    ),
    children: [
      { index: true, element: <Navigate to="/app/inicio" replace /> },
      { path: 'inicio', element: lazyWrap(<DashboardPage />) },
      { path: 'cargar', element: lazyWrap(<UploadPage />) },
      { path: 'detectar', element: lazyWrap(<DetectionPage />) },
      { path: 'configurar', element: lazyWrap(<ConfigurationPage />) },
      { path: 'procesar', element: lazyWrap(<ProcessingPage />) },
      { path: 'desencriptar', element: lazyWrap(<DecryptionPage />) },
      { path: 'comparar', element: lazyWrap(<ComparisonPage />) },
      { path: 'logs', element: lazyWrap(<AuditLogsPage />) },
    ],
  },
  { path: '*', element: <Navigate to="/app/inicio" replace /> },
])
