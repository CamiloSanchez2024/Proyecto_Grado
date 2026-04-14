import type { InputHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export function Input({
  className,
  label,
  error,
  id,
  ...props
}: InputHTMLAttributes<HTMLInputElement> & { label?: string; error?: string }) {
  const nid = id ?? props.name
  return (
    <label className="flex flex-col gap-1.5">
      {label ? (
        <span className="text-sm font-medium text-[var(--color-text-secondary)]">{label}</span>
      ) : null}
      <input
        id={nid}
        className={cn(
          'rounded-lg border border-[var(--color-border-default)] bg-white px-3 py-2 text-sm text-[var(--color-text-primary)] outline-none ring-[var(--color-accent)] placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-accent)] focus:ring-1',
          error && 'border-red-500',
          className,
        )}
        {...props}
      />
      {error ? <span className="text-xs text-red-500">{error}</span> : null}
    </label>
  )
}
