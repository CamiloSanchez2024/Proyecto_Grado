import type { SelectHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export function Select({
  label,
  className,
  children,
  ...props
}: SelectHTMLAttributes<HTMLSelectElement> & { label?: string }) {
  return (
    <label className="flex flex-col gap-1.5">
      {label ? (
        <span className="text-sm font-medium text-[var(--color-text-secondary)]">{label}</span>
      ) : null}
      <select
        className={cn(
          'rounded-lg border border-[var(--color-border-default)] bg-white px-3 py-2 text-sm text-[var(--color-text-primary)] outline-none focus:border-[var(--color-accent)] focus:ring-1 ring-[var(--color-accent)]',
          className,
        )}
        {...props}
      >
        {children}
      </select>
    </label>
  )
}
