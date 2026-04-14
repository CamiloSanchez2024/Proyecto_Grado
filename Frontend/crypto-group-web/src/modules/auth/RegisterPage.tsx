import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useRegister } from '@/hooks/useAuth'
import { getErrorMessage } from '@/lib/utils'
import { validateEmail, validatePassword, validateUsername } from '@/lib/validation'
import { useToast } from '@/contexts/useToast'

export function RegisterPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const register = useRegister()
  const toast = useToast()

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    const eu = validateUsername(username)
    const ee = validateEmail(email)
    const ep = validatePassword(password)
    if (eu) {
      toast.show(eu, 'warning')
      return
    }
    if (ee) {
      toast.show(ee, 'warning')
      return
    }
    if (ep) {
      toast.show(ep, 'warning')
      return
    }
    try {
      await register.mutateAsync({
        username: username.trim().toLowerCase(),
        email: email.trim(),
        password,
        full_name: fullName.trim() || undefined,
      })
      toast.show('Cuenta creada. Inicia sesión.', 'success')
    } catch (err) {
      toast.show(getErrorMessage(err), 'error')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-surface)] px-4 py-10">
      <div className="w-full max-w-[480px] rounded-xl border border-[var(--color-border-default)] bg-white p-8 shadow-[var(--shadow-lg)]">
        <Link
          to="/login"
          className="inline-flex items-center gap-1 text-sm font-medium text-[var(--color-accent)] hover:underline"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>
          Volver al inicio de sesión
        </Link>

        <h1 className="mt-5 text-2xl font-semibold text-[var(--color-text-primary)]">Crear tu cuenta</h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">Completa los datos para registrarte en CryptoUGroup</p>

        <form className="mt-6 flex flex-col gap-3" onSubmit={onSubmit}>
          <Input
            label="Nombre completo (opcional)"
            placeholder="Juan Pérez"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
          <Input
            label="Usuario"
            placeholder="nombre_usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <Input
            label="Email"
            type="email"
            placeholder="correo@ejemplo.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            label="Contraseña"
            type="password"
            placeholder="Mínimo 8 caracteres"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {password.length > 0 && (
            <div className="flex gap-1">
              {[0, 1, 2, 3].map((i) => {
                const strength = password.length >= 12 ? 4 : password.length >= 8 ? 3 : password.length >= 6 ? 2 : 1
                const colors = ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-[var(--color-accent)]']
                return (
                  <div
                    key={i}
                    className={`h-1.5 flex-1 rounded-full transition-colors ${i < strength ? colors[strength - 1] : 'bg-[var(--color-border-default)]'}`}
                  />
                )
              })}
            </div>
          )}

          <Button type="submit" className="mt-3 w-full py-2.5" disabled={register.isPending}>
            {register.isPending ? 'Creando…' : 'Crear cuenta'}
          </Button>
        </form>
      </div>
    </div>
  )
}
