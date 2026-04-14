import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useLogin } from '@/hooks/useAuth'
import { getErrorMessage } from '@/lib/utils'
import { useToast } from '@/contexts/useToast'

export function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [show, setShow] = useState(false)
  const login = useLogin()
  const toast = useToast()

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      await login.mutateAsync({ username: username.trim(), password })
      toast.show('Sesión iniciada', 'success')
    } catch (err) {
      toast.show(getErrorMessage(err), 'error')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-surface)] px-4">
      <div className="w-full max-w-[480px] rounded-xl border border-[var(--color-border-default)] bg-white p-8 shadow-[var(--shadow-lg)]">
        <div className="flex flex-col items-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#0D1B4B] text-lg font-bold text-white">
            G
          </div>
          <h1 className="mt-4 text-center text-2xl font-semibold text-[var(--color-text-primary)]">
            Bienvenido de nuevo
          </h1>
          <p className="mt-1 text-center text-sm text-[var(--color-text-secondary)]">
            Inicia sesión en tu espacio CryptoUGroup
          </p>
        </div>

        <form className="mt-8 flex flex-col gap-4" onSubmit={onSubmit}>
          <Input
            label="Usuario"
            name="username"
            autoComplete="username"
            placeholder="Tu nombre de usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <div>
            <Input
              label="Contraseña"
              name="password"
              type={show ? 'text' : 'password'}
              autoComplete="current-password"
              placeholder="Tu contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="mt-1.5 text-xs font-medium text-[var(--color-accent)] hover:underline"
              onClick={() => setShow((s) => !s)}
            >
              {show ? 'Ocultar contraseña' : 'Mostrar contraseña'}
            </button>
          </div>

          <Button type="submit" className="mt-2 w-full py-2.5" disabled={login.isPending}>
            {login.isPending ? 'Entrando…' : 'Iniciar sesión'}
          </Button>
        </form>

        <div className="mt-6 border-t border-[var(--color-border-default)] pt-4 text-center">
          <p className="text-sm text-[var(--color-text-muted)]">
            ¿No tienes cuenta?{' '}
            <Link className="font-medium text-[var(--color-accent)] hover:underline" to="/register">
              Registrarse
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
