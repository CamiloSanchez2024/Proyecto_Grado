import { Button } from '@/components/ui/Button'
import { Link } from 'react-router-dom'
import { Select } from '@/components/ui/Select'
import { TIPOS_PROTECCION, type TipoProteccion } from '@/types/proteccion.types'
import { useArchivoStore } from '@/stores/archivoStore'
import { useToast } from '@/contexts/useToast'

export function ConfigurationPage() {
  const toast = useToast()
  const columnasIncluidas = useArchivoStore((s) => s.columnasIncluidas)
  const columnasDetectadas = useArchivoStore((s) => s.columnasDetectadas)
  const columnasSensibles = useArchivoStore((s) => s.columnasSensiblesNombres)
  const configuracionPorColumna = useArchivoStore((s) => s.configuracionPorColumna)
  const setConfiguracionColumna = useArchivoStore((s) => s.setConfiguracionColumna)
  const guardarConfiguraciones = useArchivoStore((s) => s.guardarConfiguraciones)
  const inicializar = useArchivoStore((s) => s.inicializarConfiguracionDesdeEstado)

  const sensSet = new Set(columnasSensibles)
  const objetivo =
    columnasIncluidas.length > 0 ? columnasIncluidas : columnasDetectadas

  function guardar() {
    inicializar()
    guardarConfiguraciones()
    const list = useArchivoStore.getState().configuracionesGuardadas
    if (list.length === 0) {
      toast.show('No hay columnas para configurar', 'warning')
      return
    }
    toast.show('Configuración guardada correctamente', 'success')
  }

  if (objetivo.length === 0) {
    return (
      <div className="space-y-4">
        <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-8 text-center">
          <p className="text-[var(--color-text-muted)]">
            No hay columnas para configurar. Ve a Detectar datos y guarda selección.
          </p>
        </div>
        <div className="flex justify-end">
          <Link to="/app/procesar">
            <Button type="button">Siguiente: Procesar archivo</Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="space-y-3">
        {objetivo.map((columna) => {
          const tipo = (configuracionPorColumna[columna] as TipoProteccion) ?? (sensSet.has(columna) ? 'aes-256' : 'anonimizacion')
          const isHighSec = tipo === 'aes-256'
          return (
            <div
              key={columna}
              className="flex flex-wrap items-center gap-4 rounded-xl border border-[var(--color-border-default)] bg-white px-5 py-4"
            >
              <span className="min-w-[140px] font-medium text-[var(--color-text-primary)]">{columna}</span>
              <Select
                label=""
                className="min-w-[220px]"
                value={tipo}
                onChange={(e) =>
                  setConfiguracionColumna(columna, e.target.value as TipoProteccion)
                }
              >
                {TIPOS_PROTECCION.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </Select>
              <div className="flex items-center gap-1.5">
                <span className="text-sm text-[var(--color-text-secondary)]">Nivel:</span>
                <div className="flex gap-0.5">
                  {[0, 1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className={`h-2 w-4 rounded-sm ${i < (isHighSec ? 5 : 3) ? 'bg-[var(--color-accent)]' : 'bg-[var(--color-border-default)]'}`}
                    />
                  ))}
                </div>
              </div>
            </div>
          )
        })}
      </div>
      <div className="flex flex-wrap justify-end gap-2">
        <Button onClick={guardar}>Guardar configuración</Button>
        <Link to="/app/procesar">
          <Button type="button">Siguiente: Procesar archivo</Button>
        </Link>
      </div>
    </div>
  )
}
