import { Button } from '@/components/ui/Button'

export function Header({
  title,
  subtitle,
  username,
  onLogout,
}: {
  title: string
  subtitle?: string
  username: string | null
  onLogout: () => void
}) {
  return (
    <header className="flex items-start justify-between border-b border-[var(--color-border-default)] bg-white px-6 py-4">
      <div>
        <h1 className="text-xl font-semibold text-[var(--color-text-primary)]">{title}</h1>
        {subtitle ? (
          <p className="mt-0.5 text-sm text-[var(--color-text-secondary)]">{subtitle}</p>
        ) : null}
      </div>
      <div className="flex items-center gap-3">
        {username ? (
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--color-accent)] text-xs font-medium text-white">
              {username.charAt(0).toUpperCase()}
            </div>
            <span className="text-sm text-[var(--color-text-secondary)]">{username}</span>
          </div>
        ) : null}
        <Button variant="secondary" onClick={onLogout}>
          Cerrar sesión
        </Button>
      </div>
    </header>
  )
}
