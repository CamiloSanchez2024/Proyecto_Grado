import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import * as proteccionService from '@/services/proteccionService'
import { useArchivoStore } from '@/stores/archivoStore'
import { useToast } from '@/contexts/useToast'
import { getErrorMessage, resolveDownloadFilename } from '@/lib/utils'

export function DecryptionPage() {
  const toast = useToast()
  const idFromStore = useArchivoStore((s) => s.idArchivo)
  /** null = usar ID del store cuando exista */
  const [idOverride, setIdOverride] = useState<string | null>(null)
  const idArchivo = (idOverride ?? idFromStore ?? '').trim()
  const [clave, setClave] = useState('')
  const [show, setShow] = useState(false)

  const mut = useMutation({
    mutationFn: async () => {
      if (!idArchivo) throw new Error('Indica el ID de archivo')
      if (!clave.trim()) throw new Error('Indica la clave de desencriptación')
      return proteccionService.desencriptarArchivo({
        id_archivo: idArchivo,
        clave_usuario: clave,
      })
    },
    onSuccess: async ({ blob, filename }) => {
      const name = await resolveDownloadFilename(blob, filename)
      proteccionService.triggerDownload(blob, name)
      toast.show('Archivo desencriptado descargado', 'success')
    },
    onError: (e) => toast.show(getErrorMessage(e), 'error'),
  })

  return (
    <div className="max-w-lg space-y-5">
      <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5 space-y-4">
        <div>
          <Input
            label="ID de archivo procesado"
            placeholder="UUID del archivo"
            value={idOverride ?? idFromStore ?? ''}
            onChange={(e) => setIdOverride(e.target.value)}
          />
          <button
            type="button"
            className="mt-2 text-xs font-medium text-[var(--color-accent)] hover:underline"
            onClick={() => setIdOverride(null)}
          >
            Usar último ID cargado
          </button>
        </div>

        <div>
          <Input
            label="Clave de desencriptación (uso temporal en memoria)"
            type={show ? 'text' : 'password'}
            placeholder="Clave AES"
            value={clave}
            onChange={(e) => setClave(e.target.value)}
          />
          <button
            type="button"
            className="mt-2 text-xs font-medium text-[var(--color-accent)] hover:underline"
            onClick={() => setShow((s) => !s)}
          >
            {show ? 'Ocultar clave' : 'Mostrar clave'}
          </button>
        </div>
      </div>

      <Button type="button" disabled={mut.isPending} onClick={() => mut.mutate()}>
        {mut.isPending ? 'Desencriptando…' : 'Desencriptar y descargar'}
      </Button>
    </div>
  )
}
