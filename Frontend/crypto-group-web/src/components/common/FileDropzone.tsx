import { useCallback, useState, type DragEvent } from 'react'
import { cn } from '@/lib/utils'

const ACCEPT = '.csv,.xlsx,.xls,application/vnd.ms-excel,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

export function FileDropzone({
  onFile,
  disabled,
}: {
  onFile: (file: File) => void
  disabled?: boolean
}) {
  const [over, setOver] = useState(false)

  const handleFiles = useCallback(
    (list: FileList | null) => {
      if (!list?.length) return
      onFile(list[0])
    },
    [onFile],
  )

  return (
    <div
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          document.getElementById('file-input-hidden')?.click()
        }
      }}
      onDragOver={(e: DragEvent) => {
        e.preventDefault()
        if (!disabled) setOver(true)
      }}
      onDragLeave={() => setOver(false)}
      onDrop={(e: DragEvent) => {
        e.preventDefault()
        setOver(false)
        if (disabled) return
        handleFiles(e.dataTransfer.files)
      }}
      className={cn(
        'flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-14 transition-colors bg-white',
        over ? 'border-[var(--color-accent)] bg-[var(--color-accent)]/5' : 'border-[var(--color-border-default)]',
        disabled && 'pointer-events-none opacity-50',
      )}
      onClick={() => !disabled && document.getElementById('file-input-hidden')?.click()}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[var(--color-accent)]/10 text-[var(--color-accent)]">
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
        </svg>
      </div>
      <p className="mt-3 font-medium text-[var(--color-text-primary)]">Arrastra tu archivo aquí</p>
      <p className="mt-1 text-center text-sm text-[var(--color-text-secondary)]">
        o haz clic para seleccionar
      </p>
      <div className="mt-3 flex flex-wrap justify-center gap-1.5">
        {['.csv', '.xlsx', '.xls'].map((ext) => (
          <span key={ext} className="rounded-md bg-[var(--color-surface)] px-2 py-0.5 text-xs font-medium text-[var(--color-text-secondary)]">
            {ext}
          </span>
        ))}
      </div>
      <input
        id="file-input-hidden"
        type="file"
        accept={ACCEPT}
        className="hidden"
        disabled={disabled}
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  )
}
