import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import * as proteccionService from '@/services/proteccionService'
import { useToast } from '@/contexts/useToast'
import { getErrorMessage } from '@/lib/utils'

export function ComparisonPage() {
  const toast = useToast()
  const [orig, setOrig] = useState<File | null>(null)
  const [dec, setDec] = useState<File | null>(null)

  const mut = useMutation({
    mutationFn: async () => {
      if (!orig || !dec) throw new Error('Selecciona ambos archivos')
      return proteccionService.compararArchivos(orig, dec)
    },
    onSuccess: () => toast.show('Comparación completada', 'success'),
    onError: (e) => toast.show(getErrorMessage(e), 'error'),
  })

  const data = mut.data

  return (
    <div className="max-w-4xl space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
          <p className="text-sm font-medium text-[var(--color-text-primary)]">Archivo original</p>
          <p className="mt-1 text-xs text-[var(--color-text-muted)]">Selecciona el archivo antes de ser procesado</p>
          <div className="mt-3 rounded-lg border border-dashed border-[var(--color-border-default)] p-3">
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              className="w-full text-sm text-[var(--color-text-secondary)] file:mr-3 file:rounded-md file:border-0 file:bg-[var(--color-accent)] file:px-3 file:py-1.5 file:text-xs file:font-medium file:text-white hover:file:bg-[var(--color-accent-hover)]"
              onChange={(e) => setOrig(e.target.files?.[0] ?? null)}
            />
          </div>
          {orig && <p className="mt-2 text-xs text-[var(--color-text-secondary)]">{orig.name}</p>}
        </div>
        <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
          <p className="text-sm font-medium text-[var(--color-text-primary)]">Archivo desencriptado</p>
          <p className="mt-1 text-xs text-[var(--color-text-muted)]">Selecciona el archivo después de desencriptar</p>
          <div className="mt-3 rounded-lg border border-dashed border-[var(--color-border-default)] p-3">
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              className="w-full text-sm text-[var(--color-text-secondary)] file:mr-3 file:rounded-md file:border-0 file:bg-[var(--color-accent)] file:px-3 file:py-1.5 file:text-xs file:font-medium file:text-white hover:file:bg-[var(--color-accent-hover)]"
              onChange={(e) => setDec(e.target.files?.[0] ?? null)}
            />
          </div>
          {dec && <p className="mt-2 text-xs text-[var(--color-text-secondary)]">{dec.name}</p>}
        </div>
      </div>

      <Button type="button" disabled={mut.isPending || !orig || !dec} onClick={() => mut.mutate()}>
        {mut.isPending ? 'Comparando…' : 'Ejecutar comparación'}
      </Button>

      {data ? (
        <div className="space-y-4 rounded-xl border border-[var(--color-border-default)] bg-white p-5">
          <div className="flex flex-wrap gap-4">
            <div className="rounded-lg bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
              Coincidencia: {data.coincidencia}%
            </div>
            <div className="rounded-lg bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700">
              Iguales: {data.filas_iguales}
            </div>
            <div className="rounded-lg bg-red-50 px-4 py-2 text-sm font-medium text-red-700">
              Diferentes: {data.filas_diferentes}
            </div>
          </div>

          {data.columnas_con_error.length > 0 ? (
            <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
              <p className="text-sm text-amber-700">Columnas con error: {data.columnas_con_error.join(', ')}</p>
            </div>
          ) : null}

          <pre className="max-h-80 overflow-auto rounded-lg bg-[var(--color-surface)] p-4 font-mono text-xs text-[var(--color-text-primary)]">
            {JSON.stringify(data.detalle, null, 2)}
          </pre>
        </div>
      ) : null}
    </div>
  )
}
