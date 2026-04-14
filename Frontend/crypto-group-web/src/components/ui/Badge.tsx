import { cn } from '@/lib/utils'

type Tone = 'alto' | 'bajo' | 'info' | 'warning' | 'error'

const map: Record<Tone, string> = {
  alto: 'bg-amber-50 text-amber-700 border-amber-200',
  bajo: 'bg-slate-50 text-slate-600 border-slate-200',
  info: 'bg-blue-50 text-blue-700 border-blue-200',
  warning: 'bg-amber-50 text-amber-700 border-amber-200',
  error: 'bg-red-50 text-red-700 border-red-200',
}

export function Badge({ children, tone }: { children: string; tone: Tone }) {
  return (
    <span
      className={cn(
        'inline-flex rounded-md border px-2 py-0.5 text-xs font-semibold uppercase tracking-wide',
        map[tone],
      )}
    >
      {children}
    </span>
  )
}
