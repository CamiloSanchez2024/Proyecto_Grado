const USERNAME_RE = /^[a-zA-Z0-9_]{3,50}$/

export function validateUsername(username: string): string | null {
  const t = username.trim()
  if (!USERNAME_RE.test(t)) {
    return 'Usuario: 3-50 caracteres, letras, números o guiones bajos únicamente'
  }
  return null
}

export function validatePassword(password: string): string | null {
  if (password.length < 8) return 'Contraseña: al menos 8 caracteres'
  if (!/[A-Z]/.test(password)) return 'Contraseña: debe incluir una letra mayúscula'
  if (!/\d/.test(password)) return 'Contraseña: debe incluir un dígito'
  return null
}

export function validateEmail(email: string): string | null {
  const t = email.trim()
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(t)) return 'Email inválido'
  return null
}
