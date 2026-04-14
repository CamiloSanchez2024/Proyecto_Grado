import { useMemo } from 'react'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useArchivoStore } from '@/stores/archivoStore'
import { useToast } from '@/contexts/useToast'

export function DetectionPage() {
  const toast = useToast()
  const columnasDetectadas = useArchivoStore((s) => s.columnasDetectadas)
  const columnasSensibles = useArchivoStore((s) => s.columnasSensiblesNombres)
  const columnasIncluidas = useArchivoStore((s) => s.columnasIncluidas)
  const setColumnasIncluidas = useArchivoStore((s) => s.setColumnasIncluidas)
  const usarSugeridas = useArchivoStore((s) => s.usarSugeridasSensibles)

  const sensSet = useMemo(() => new Set(columnasSensibles), [columnasSensibles])
  const includedSet = useMemo(() => new Set(columnasIncluidas), [columnasIncluidas])

  function toggle(col: string) {
    const n = new Set(includedSet)
    if (n.has(col)) n.delete(col)
    else n.add(col)
    setColumnasIncluidas([...n])
  }

  function guardar() {
    if (columnasIncluidas.length === 0) {
      toast.show('No seleccionaste columnas. No habrá protección al procesar.', 'warning')
      return
    }
    toast.show(`Selección guardada: ${columnasIncluidas.length} columnas incluidas.`, 'success')
  }

  function sugeridas() {
    usarSugeridas()
    toast.show(`Se aplicaron sugeridas: ${columnasSensibles.length} columnas.`, 'success')
  }

  if (columnasDetectadas.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--color-border-default)] bg-white p-8 text-center">
        <p className="text-[var(--color-text-muted)]">Primero carga y analiza un archivo en &quot;Cargar archivo&quot;.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="overflow-hidden rounded-xl border border-[var(--color-border-default)] bg-white">
        <div className="grid grid-cols-4 gap-2 border-b border-[var(--color-border-default)] bg-[var(--color-surface)] px-4 py-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
          <span>Columna</span>
          <span>Tipo detectado</span>
          <span>Confianza</span>
          <span className="text-center">Incluida</span>
        </div>
        <div className="max-h-[420px] overflow-auto">
          {columnasDetectadas.map((col) => {
            const sensible = sensSet.has(col)
            const on = includedSet.has(col)
            return (
              <div
                key={col}
                className="grid grid-cols-4 items-center gap-2 border-b border-[var(--color-border-subtle)] px-4 py-3 text-sm hover:bg-[var(--color-surface)] transition-colors"
              >
                <span className="font-medium text-[var(--color-text-primary)]">{col}</span>
                <span className="text-[var(--color-text-secondary)]">{sensible ? 'Sensible' : 'General'}</span>
                <span>
                  <Badge tone={sensible ? 'alto' : 'bajo'}>{sensible ? 'ALTO' : 'BAJO'}</Badge>
                </span>
                <label className="flex justify-center">
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-[var(--color-border-default)] accent-[var(--color-accent)]"
                    checked={on}
                    onChange={() => toggle(col)}
                  />
                </label>
              </div>
            )
          })}
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button onClick={guardar}>Guardar selección de columnas</Button>
        <Button variant="secondary" onClick={sugeridas}>
          Usar sugeridas (sensibles)
        </Button>
      </div>
    </div>
  )
}
