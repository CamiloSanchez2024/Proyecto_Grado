import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { ProgressBar } from '@/components/ui/ProgressBar'
import * as proteccionService from '@/services/proteccionService'
import { useArchivoStore } from '@/stores/archivoStore'
import type { ConfiguracionProteccionItem } from '@/types/proteccion.types'
import { useToast } from '@/contexts/useToast'
import { getErrorMessage } from '@/lib/utils'

export function ProcessingPage() {
  const toast = useToast()
  const queryClient = useQueryClient()
  const idArchivo = useArchivoStore((s) => s.idArchivo)
  const configuracionesGuardadas = useArchivoStore((s) => s.configuracionesGuardadas)
  const setNombreArchivoProcesado = useArchivoStore((s) => s.setNombreArchivoProcesado)
  const columnasIncluidas = useArchivoStore((s) => s.columnasIncluidas)
  const columnasDetectadas = useArchivoStore((s) => s.columnasDetectadas)
  const configuracionPorColumna = useArchivoStore((s) => s.configuracionPorColumna)
  const guardarConfigEnStore = useArchivoStore((s) => s.guardarConfiguraciones)
  const nombreProc = useArchivoStore((s) => s.nombreArchivoProcesado)

  const [clave, setClave] = useState('')
  const [show, setShow] = useState(false)
  const [log, setLog] = useState<string[]>([])
  const [progress, setProgress] = useState(0)
  const [estado, setEstado] = useState('Listo para procesar')

  function append(line: string) {
    setLog((l) => [...l, line])
  }

  function obtenerConfiguracionesActuales(): ConfiguracionProteccionItem[] {
    const objetivo = columnasIncluidas.length > 0 ? columnasIncluidas : columnasDetectadas
    return objetivo.map((col) => {
      const tipo = String(configuracionPorColumna[col] ?? 'aes-256').trim() || 'aes-256'
      return { columna: col, tipo_proteccion: tipo }
    })
  }

  const runProcess = useMutation({
    mutationFn: async () => {
      if (!idArchivo) throw new Error('Primero carga un archivo')
      let configs = configuracionesGuardadas
      if (configs.length === 0) {
        guardarConfigEnStore()
        configs = useArchivoStore.getState().configuracionesGuardadas
      }
      if (configs.length === 0) {
        const act = obtenerConfiguracionesActuales()
        if (act.length === 0) throw new Error('Configura y guarda encriptación primero')
        useArchivoStore.setState({ configuracionesGuardadas: act })
        configs = act
      }
      const claveUsuario = clave.trim() || null
      return proteccionService.procesarArchivo({
        id_archivo: idArchivo,
        configuraciones: configs,
        clave_usuario: claveUsuario,
      })
    },
    onSuccess: (data) => {
      setNombreArchivoProcesado(data.nombre_archivo_procesado)
      append('[SUCCESS] Archivo procesado correctamente.')
      append(`[INFO] ID de archivo procesado: ${data.id_archivo}`)
      setEstado('Proceso finalizado')
      setProgress(1)
      setClave('')
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      toast.show('Archivo procesado', 'success')
    },
    onError: (e) => {
      append(`[ERROR] ${getErrorMessage(e)}`)
      setEstado('Fallo de procesamiento')
      toast.show(getErrorMessage(e), 'error')
    },
  })

  function iniciar() {
    setLog([])
    setProgress(0)
    append('[INFO] Construyendo configuración...')
    setEstado('Procesando configuración de columnas...')
    let step = 0
    const interval = window.setInterval(() => {
      step = Math.min(step + 0.02, 0.35)
      setProgress(step)
      if (step >= 0.35) {
        window.clearInterval(interval)
        append('[INFO] Enviando petición a backend...')
        runProcess.mutate()
      }
    }, 30)
  }

  const downloadMut = useMutation({
    mutationFn: async () => {
      if (!idArchivo) throw new Error('No hay archivo procesado disponible')
      const { blob, filename } = await proteccionService.descargarArchivo(idArchivo)
      const name = filename ?? nombreProc ?? 'archivo_procesado.csv'
      proteccionService.triggerDownload(blob, name)
    },
    onSuccess: () => {
      append('[SUCCESS] Archivo descargado')
      toast.show('Archivo descargado correctamente', 'success')
    },
    onError: (e) => {
      append(`[ERROR] ${getErrorMessage(e)}`)
      toast.show(getErrorMessage(e), 'error')
    },
  })

  const resumen =
    configuracionesGuardadas.length === 0
      ? '- Sin configuraciones guardadas.\n- Ve a "Configurar" y guarda antes de procesar.'
      : configuracionesGuardadas.map((i) => `- ${i.columna}: ${i.tipo_proteccion}`).join('\n')

  return (
    <div className="flex max-w-4xl flex-col gap-5">
      <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
        <p className="text-sm font-medium text-[var(--color-text-secondary)]">
          Clave de encriptación AES (opcional, recomendada para validar desencriptación)
        </p>
        <div className="mt-3 flex items-end gap-3">
          <div className="flex-1">
            <Input
              type={show ? 'text' : 'password'}
              placeholder="Clave de usuario para AES"
              value={clave}
              onChange={(e) => setClave(e.target.value)}
            />
          </div>
          <button
            type="button"
            className="text-sm font-medium text-[var(--color-accent)] hover:underline"
            onClick={() => setShow((s) => !s)}
          >
            {show ? 'Ocultar' : 'Mostrar'}
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-5">
        <p className="text-sm font-medium text-[var(--color-text-secondary)]">Resumen de configuraciones guardadas</p>
        <pre className="mt-3 whitespace-pre-wrap rounded-lg bg-[var(--color-surface)] p-4 font-mono text-xs text-[var(--color-text-primary)]">
          {resumen}
        </pre>
      </div>

      <div className="space-y-2">
        <ProgressBar value={progress} />
        <p className="text-sm text-[var(--color-text-secondary)]">{estado}</p>
      </div>

      <div className="flex flex-wrap gap-2">
        <Link to="/app/cargar">
          <Button variant="secondary" type="button">
            Cargar archivo
          </Button>
        </Link>
        <Button type="button" disabled={runProcess.isPending} onClick={() => void iniciar()}>
          Iniciar procesamiento
        </Button>
        <Button variant="secondary" type="button" disabled={downloadMut.isPending} onClick={() => downloadMut.mutate()}>
          Descargar último resultado
        </Button>
      </div>

      <textarea
        readOnly
        className="min-h-[240px] w-full resize-y rounded-xl border border-[var(--color-border-default)] bg-[var(--color-surface)] p-4 font-mono text-xs text-[var(--color-text-primary)]"
        value={log.join('\n')}
      />
    </div>
  )
}
