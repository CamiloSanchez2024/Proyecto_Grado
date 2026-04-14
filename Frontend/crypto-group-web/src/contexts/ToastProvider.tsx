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
      <div className="pointer-events-none fixed bottom-4 right-4 z-[100] flex max-w-sm flex-col gap-2">
        {items.map((t) => (
          <ToastItem key={t.id} message={t.message} kind={t.kind} />
        ))}
      </div>
    </ToastContext.Provider>
  )
}

function ToastItem({ message, kind }: { message: string; kind: ToastKind }) {
  const cls =
    kind === 'success'
      ? 'border-emerald-700 bg-emerald-950/95 text-emerald-100'
      : kind === 'error'
        ? 'border-red-700 bg-red-950/95 text-red-100'
        : kind === 'warning'
          ? 'border-amber-700 bg-amber-950/95 text-amber-100'
          : 'border-[var(--color-border-subtle)] bg-[var(--color-panel)] text-[var(--color-text-primary)]'

  return (
    <div className={`pointer-events-auto rounded-lg border px-4 py-3 text-sm shadow-lg ${cls}`}>{message}</div>
  )
}
