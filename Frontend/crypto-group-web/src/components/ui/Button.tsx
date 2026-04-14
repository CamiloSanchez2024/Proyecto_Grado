import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

type Variant = 'primary' | 'secondary' | 'danger'

const styles: Record<Variant, string> = {
  primary:
    'bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-white border-transparent',
  secondary:
    'bg-white hover:bg-[var(--color-surface)] text-[var(--color-text-primary)] border-[var(--color-border-default)]',
  danger: 'bg-red-600 hover:bg-red-700 text-white border-transparent',
}

export function Button({
  variant = 'primary',
  type = 'button',
  className,
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      type={type}
      className={cn(
        'inline-flex items-center justify-center rounded-lg border px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed',
        styles[variant],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}
