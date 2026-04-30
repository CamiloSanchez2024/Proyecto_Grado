import { useCallback, useMemo, useState, type ReactNode } from 'react'
import { ToastContext, type ToastKind } from '@/contexts/toast-context'

interface Toast {
  id: number
  message: string
  kind: ToastKind
}

let idSeq = 0

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<Toast[]>([])

  const show = useCallback((message: string, kind: ToastKind = 'info') => {
    const id = ++idSeq
    setItems((prev) => [...prev, { id, message, kind }])
    window.setTimeout(() => {
      setItems((prev) => prev.filter((t) => t.id !== id))
    }, 4500)
  }, [])

  const value = useMemo(() => ({ show }), [show])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed inset-x-0 top-5 z-[100] flex items-center justify-center px-4">
        <div className="flex w-full max-w-xl flex-col gap-2">
        {items.map((t) => (
          <ToastItem key={t.id} message={t.message} kind={t.kind} />
        ))}
        </div>
      </div>
    </ToastContext.Provider>
  )
}

function ToastItem({ message, kind }: { message: string; kind: ToastKind }) {
  const styleByKind =
    kind === 'success'
      ? {
          container: 'border-emerald-300/60 bg-emerald-50/95 text-emerald-900',
          iconBg: 'bg-emerald-100 text-emerald-700',
          icon: '✓',
        }
      : kind === 'error'
        ? {
            container: 'border-red-300/60 bg-red-50/95 text-red-900',
            iconBg: 'bg-red-100 text-red-700',
            icon: '!',
          }
        : kind === 'warning'
          ? {
              container: 'border-amber-300/60 bg-amber-50/95 text-amber-900',
              iconBg: 'bg-amber-100 text-amber-700',
              icon: '!',
            }
          : {
              container: 'border-sky-300/60 bg-sky-50/95 text-sky-900',
              iconBg: 'bg-sky-100 text-sky-700',
              icon: 'i',
            }

  return (
    <div
      className={`pointer-events-auto flex items-start gap-3 rounded-xl border px-4 py-3 text-sm shadow-[0_10px_35px_rgba(2,6,23,0.15)] backdrop-blur-sm ${styleByKind.container}`}
      role="status"
      aria-live="polite"
    >
      <span
        className={`mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${styleByKind.iconBg}`}
        aria-hidden="true"
      >
        {styleByKind.icon}
      </span>
      <p className="font-medium leading-5">{message}</p>
    </div>
  )
}
