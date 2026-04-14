import { createContext } from 'react'

export type ToastKind = 'success' | 'error' | 'warning' | 'info'

export const ToastContext = createContext<{
  show: (message: string, kind?: ToastKind) => void
} | null>(null)
