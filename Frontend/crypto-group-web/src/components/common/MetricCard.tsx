export function MetricCard({
  label,
  value,
  accent = 'blue',
}: {
  label: string
  value: string | number
  accent?: 'blue' | 'emerald' | 'violet'
}) {
  const bar =
    accent === 'blue'
      ? 'bg-blue-500'
      : accent === 'emerald'
        ? 'bg-emerald-500'
        : 'bg-violet-500'

  const iconBg =
    accent === 'blue'
      ? 'bg-blue-50 text-blue-600'
      : accent === 'emerald'
        ? 'bg-emerald-50 text-emerald-600'
        : 'bg-violet-50 text-violet-600'

  return (
    <div className="relative overflow-hidden rounded-xl border border-[var(--color-border-default)] bg-white p-5">
      <div className={`absolute left-0 top-0 h-full w-1 ${bar}`} />
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-[var(--color-text-secondary)]">{label}</p>
          <p className="mt-2 text-3xl font-semibold tabular-nums text-[var(--color-text-primary)]">{value}</p>
        </div>
        <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${iconBg}`}>
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
          </svg>
        </div>
      </div>
    </div>
  )
}
