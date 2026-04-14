import { describe, expect, it } from 'vitest'
import { validatePassword, validateUsername } from '@/lib/validation'

describe('validation', () => {
  it('rejects short username', () => {
    expect(validateUsername('ab')).not.toBeNull()
  })
  it('accepts valid username', () => {
    expect(validateUsername('user_01')).toBeNull()
  })
  it('rejects weak password', () => {
    expect(validatePassword('short')).not.toBeNull()
    expect(validatePassword('lowercase1')).not.toBeNull()
  })
  it('accepts strong password', () => {
    expect(validatePassword('Secure12')).toBeNull()
  })
})
