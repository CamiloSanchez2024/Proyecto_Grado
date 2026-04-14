export type ApiErrorDetail = string | { loc?: unknown[]; msg: string; type?: string }[]

export interface ApiErrorBody {
  detail?: ApiErrorDetail
  success?: boolean
}
