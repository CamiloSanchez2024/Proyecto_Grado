import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { FileDropzone } from '@/components/common/FileDropzone'
import { Button } from '@/components/ui/Button'
import * as proteccionService from '@/services/proteccionService'
import { useArchivoStore } from '@/stores/archivoStore'
import { useToast } from '@/contexts/useToast'
import { getErrorMessage } from '@/lib/utils'

export function UploadPage() {
  const toast = useToast()
  const queryClient = useQueryClient()
  const setFromUpload = useArchivoStore((s) => s.setFromUpload)
  const setFromAnalisis = useArchivoStore((s) => s.setFromAnalisis)
  const columnas = useArchivoStore((s) => s.columnasDetectadas)

  const mutation = useMutation({
    mutationFn: async (file: File) => {
      const up = await proteccionService.subirArchivo(file)
      setFromUpload(up.id_archivo, up.nombre_archivo)
      const an = await proteccionService.analizarArchivo(up.id_archivo)
      const sensibles = an.columnas_sensibles.map((x) => x.columna)
      setFromAnalisis({
        columnas: an.columnas,
        columnasSensiblesNombres: sensibles,
        totalFilas: an.total_filas,
      })
      return an
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      toast.show('Archivo cargado y analizado', 'success')
    },
    onError: (e) => toast.show(getErrorMessage(e), 'error'),
  })

  return (
    <div className="space-y-6">
      <FileDropzone onFile={(f) => mutation.mutate(f)} disabled={mutation.isPending} />

      {mutation.isPending ? (
        <div className="flex items-center gap-2 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3">
          <svg className="h-4 w-4 animate-spin text-blue-600" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p className="text-sm text-blue-700">Subiendo y analizando…</p>
        </div>
      ) : null}

      <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
        <p className="text-sm font-medium text-[var(--color-text-secondary)]">Vista previa de columnas</p>
        {columnas.length === 0 ? (
          <p className="mt-2 text-sm text-[var(--color-text-muted)]">Sin vista previa disponible</p>
        ) : (
          <ul className="mt-3 max-h-48 space-y-1 overflow-auto">
            {columnas.map((c) => (
              <li key={c} className="flex items-center gap-2 text-sm text-[var(--color-text-primary)]">
                <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-accent)]" />
                {c}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="flex justify-end">
        <Link to="/app/detectar">
          <Button type="button">Siguiente: Detectar datos</Button>
        </Link>
      </div>
    </div>
  )
}
