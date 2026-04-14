import { cn } from '@/lib/utils'

export function ProgressBar({ value }: { value: number }) {
  const v = Math.min(1, Math.max(0, value))
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-[var(--color-surface)]">
      <div
        className={cn('h-full rounded-full bg-[var(--color-accent)] transition-[width] duration-150')}
        style={{ width: `${v * 100}%` }}
      />
    </div>
  )
}
