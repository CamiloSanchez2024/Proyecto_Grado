import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { ConfiguracionProteccionItem, TipoProteccion } from '@/types/proteccion.types'

interface ArchivoState {
  idArchivo: string | null
  nombreArchivoOriginal: string | null
  columnasDetectadas: string[]
  columnasSensiblesNombres: string[]
  columnasIncluidas: string[]
  /** Map columna -> tipo (UI state before "Guardar configuración") */
  configuracionPorColumna: Record<string, TipoProteccion | string>
  configuracionesGuardadas: ConfiguracionProteccionItem[]
  nombreArchivoProcesado: string | null
  totalFilas: number | null
  resetArchivo: () => void
  setFromUpload: (id: string, nombre: string) => void
  setFromAnalisis: (payload: {
    columnas: string[]
    columnasSensiblesNombres: string[]
    totalFilas: number
  }) => void
  setColumnasIncluidas: (cols: string[]) => void
  usarSugeridasSensibles: () => void
  setConfiguracionColumna: (columna: string, tipo: TipoProteccion | string) => void
  guardarConfiguraciones: () => void
  setNombreArchivoProcesado: (n: string | null) => void
  inicializarConfiguracionDesdeEstado: () => void
}

const defaultConfigForColumn = (
  columna: string,
  sensibles: Set<string>,
): TipoProteccion => (sensibles.has(columna) ? 'aes-256' : 'anonimizacion')

export const useArchivoStore = create<ArchivoState>()(
  persist(
    (set, get) => ({
      idArchivo: null,
      nombreArchivoOriginal: null,
      columnasDetectadas: [],
      columnasSensiblesNombres: [],
      columnasIncluidas: [],
      configuracionPorColumna: {},
      configuracionesGuardadas: [],
      nombreArchivoProcesado: null,
      totalFilas: null,

      resetArchivo: () =>
        set({
          idArchivo: null,
          nombreArchivoOriginal: null,
          columnasDetectadas: [],
          columnasSensiblesNombres: [],
          columnasIncluidas: [],
          configuracionPorColumna: {},
          configuracionesGuardadas: [],
          nombreArchivoProcesado: null,
          totalFilas: null,
        }),

      setFromUpload: (id, nombre) =>
        set({
          idArchivo: id,
          nombreArchivoOriginal: nombre,
          nombreArchivoProcesado: null,
        }),

      setFromAnalisis: ({ columnas, columnasSensiblesNombres, totalFilas }) => {
        const sens = new Set(columnasSensiblesNombres)
        const incluidas = [...columnasSensiblesNombres]
        const config: Record<string, TipoProteccion> = {}
        const objetivo =
          incluidas.length > 0 ? incluidas : columnas.length > 0 ? [...columnas] : []
        for (const c of objetivo) {
          config[c] = defaultConfigForColumn(c, sens)
        }
        set({
          columnasDetectadas: columnas,
          columnasSensiblesNombres,
          columnasIncluidas: incluidas,
          configuracionPorColumna: config,
          configuracionesGuardadas: [],
          totalFilas,
        })
      },

      setColumnasIncluidas: (cols) => {
        set({ columnasIncluidas: cols, configuracionesGuardadas: [] })
        const sens = new Set(get().columnasSensiblesNombres)
        const next: Record<string, TipoProteccion | string> = { ...get().configuracionPorColumna }
        for (const c of cols) {
          if (!(c in next)) {
            next[c] = defaultConfigForColumn(c, sens)
          }
        }
        for (const key of Object.keys(next)) {
          if (!cols.includes(key)) delete next[key]
        }
        set({ configuracionPorColumna: next })
      },

      usarSugeridasSensibles: () => {
        const s = get().columnasSensiblesNombres
        get().setColumnasIncluidas([...s])
      },

      setConfiguracionColumna: (columna, tipo) =>
        set((state) => ({
          configuracionPorColumna: { ...state.configuracionPorColumna, [columna]: tipo },
        })),

      guardarConfiguraciones: () => {
        const { columnasIncluidas, columnasDetectadas, configuracionPorColumna } = get()
        const objetivo =
          columnasIncluidas.length > 0 ? columnasIncluidas : columnasDetectadas
        const list: ConfiguracionProteccionItem[] = objetivo.map((col) => {
          const tipo = (configuracionPorColumna[col] as string)?.trim() || 'aes-256'
          return { columna: col, tipo_proteccion: tipo }
        })
        set({ configuracionesGuardadas: list })
      },

      setNombreArchivoProcesado: (n) => set({ nombreArchivoProcesado: n }),

      inicializarConfiguracionDesdeEstado: () => {
        const {
          columnasIncluidas,
          columnasDetectadas,
          columnasSensiblesNombres,
          configuracionPorColumna,
        } = get()
        const sens = new Set(columnasSensiblesNombres)
        const objetivo =
          columnasIncluidas.length > 0 ? columnasIncluidas : columnasDetectadas
        if (objetivo.length === 0) return
        const next = { ...configuracionPorColumna }
        for (const c of objetivo) {
          if (!(c in next)) {
            next[c] = defaultConfigForColumn(c, sens)
          }
        }
        set({ configuracionPorColumna: next })
      },
    }),
    {
      name: 'cryptougroup-archivo',
      storage: createJSONStorage(() => sessionStorage),
      partialize: (s) => ({
        idArchivo: s.idArchivo,
        nombreArchivoOriginal: s.nombreArchivoOriginal,
        columnasDetectadas: s.columnasDetectadas,
        columnasSensiblesNombres: s.columnasSensiblesNombres,
        columnasIncluidas: s.columnasIncluidas,
        configuracionPorColumna: s.configuracionPorColumna,
        configuracionesGuardadas: s.configuracionesGuardadas,
        nombreArchivoProcesado: s.nombreArchivoProcesado,
        totalFilas: s.totalFilas,
      }),
    },
  ),
)
