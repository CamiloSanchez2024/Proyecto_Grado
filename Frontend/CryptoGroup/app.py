import logging
import os
from pathlib import Path
from typing import Callable

import customtkinter as ctk
import requests
from PIL import Image
from tkinter import filedialog

try:
    from CTkMessagebox import CTkMessagebox
except Exception:  # pragma: no cover
    CTkMessagebox = None


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

URL_API = "http://localhost:8000/api/v1"

COLORES = {
    "fondo_principal": "#0D1117",
    "fondo_panel": "#161B22",
    "fondo_card": "#1C2333",
    "fondo_input": "#21262D",
    "borde_sutil": "#30363D",
    "azul_primario": "#1B365D",
    "azul_accion": "#0052CC",
    "azul_boton": "#2F6FED",
    "azul_glow": "#4C8EFF",
    "verde_exito": "#238636",
    "verde_texto": "#3FB950",
    "amarillo_proceso": "#9E6A03",
    "amarillo_texto": "#D29922",
    "rojo_error": "#DA3633",
    "rojo_texto": "#F85149",
    "texto_primario": "#E6EDF3",
    "texto_secundario": "#8B949E",
    "texto_muted": "#484F58",
    "texto_link": "#58A6FF",
}

FUENTES = {
    "titulo_pantalla": ("Segoe UI", 22, "bold"),
    "titulo_seccion": ("Segoe UI", 14, "bold"),
    "subtitulo": ("Segoe UI", 11, "normal"),
    "cuerpo": ("Segoe UI", 10, "normal"),
    "cuerpo_small": ("Segoe UI", 9, "normal"),
    "etiqueta": ("Segoe UI", 9, "bold"),
    "codigo": ("Consolas", 9, "normal"),
    "badge": ("Segoe UI", 8, "bold"),
}

ESPACIADO = {
    "padding_ventana": 20,
    "padding_card": 16,
    "gap_elementos": 12,
    "radio_card": 12,
    "radio_boton": 8,
    "radio_input": 6,
    "ancho_sidebar": 240,
    "alto_header": 64,
}

logger = logging.getLogger("cryptougroup_ui")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class BotonPrimario(ctk.CTkButton):
    def __init__(self, parent, texto: str, comando: Callable, **kwargs) -> None:
        super().__init__(
            parent,
            text=texto,
            command=comando,
            fg_color=COLORES["azul_boton"],
            hover_color=COLORES["azul_glow"],
            text_color=COLORES["texto_primario"],
            corner_radius=ESPACIADO["radio_boton"],
            font=FUENTES["cuerpo"],
            height=38,
            **kwargs,
        )


class BotonSecundario(ctk.CTkButton):
    def __init__(self, parent, texto: str, comando: Callable, **kwargs) -> None:
        super().__init__(
            parent,
            text=texto,
            command=comando,
            fg_color="transparent",
            border_width=1,
            border_color=COLORES["borde_sutil"],
            hover_color=COLORES["fondo_card"],
            text_color=COLORES["texto_secundario"],
            corner_radius=ESPACIADO["radio_boton"],
            font=FUENTES["cuerpo"],
            height=38,
            **kwargs,
        )


class BotonPeligro(ctk.CTkButton):
    def __init__(self, parent, texto: str, comando: Callable, **kwargs) -> None:
        super().__init__(
            parent,
            text=texto,
            command=comando,
            fg_color=COLORES["rojo_error"],
            hover_color="#b02a28",
            text_color=COLORES["texto_primario"],
            corner_radius=ESPACIADO["radio_boton"],
            font=FUENTES["cuerpo"],
            height=38,
            **kwargs,
        )


class InputEstilizado(ctk.CTkEntry):
    def __init__(self, parent, placeholder: str, **kwargs) -> None:
        super().__init__(
            parent,
            placeholder_text=placeholder,
            fg_color=COLORES["fondo_input"],
            border_color=COLORES["borde_sutil"],
            text_color=COLORES["texto_primario"],
            placeholder_text_color=COLORES["texto_muted"],
            corner_radius=ESPACIADO["radio_input"],
            height=38,
            **kwargs,
        )


class Separador(ctk.CTkFrame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, height=1, fg_color=COLORES["borde_sutil"], **kwargs)


class BadgeEstado(ctk.CTkLabel):
    ESTILOS = {
        "alto": {"fg_color": "#1a3a1a", "text_color": COLORES["verde_texto"]},
        "medio": {"fg_color": "#3a2a00", "text_color": COLORES["amarillo_texto"]},
        "bajo": {"fg_color": "#1a1a2e", "text_color": COLORES["texto_secundario"]},
        "error": {"fg_color": "#3a0d0d", "text_color": COLORES["rojo_texto"]},
    }

    def __init__(self, parent, texto: str, nivel: str = "bajo") -> None:
        estilo = self.ESTILOS.get(nivel, self.ESTILOS["bajo"])
        super().__init__(
            parent,
            text=texto.upper(),
            fg_color=estilo["fg_color"],
            text_color=estilo["text_color"],
            corner_radius=14,
            font=FUENTES["badge"],
            padx=8,
            pady=2,
        )


class TarjetaMetrica(ctk.CTkFrame):
    def __init__(
        self, parent, titulo: str, valor: str, icono: str, color_acento: str, subtexto: str
    ) -> None:
        super().__init__(
            parent,
            fg_color=COLORES["fondo_card"],
            corner_radius=ESPACIADO["radio_card"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        self.grid_columnconfigure(1, weight=1)
        ctk.CTkFrame(self, width=4, fg_color=color_acento, corner_radius=0).grid(
            row=0, column=0, rowspan=3, sticky="nsw"
        )
        ctk.CTkLabel(
            self, text=f"{icono}  {titulo}", font=FUENTES["etiqueta"], text_color=COLORES["texto_secundario"]
        ).grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))
        ctk.CTkLabel(
            self, text=str(valor), font=("Segoe UI", 22, "bold"), text_color=COLORES["texto_primario"]
        ).grid(row=1, column=1, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(
            self, text=subtexto, font=FUENTES["cuerpo_small"], text_color=COLORES["texto_muted"]
        ).grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))


class PantallaBase(ctk.CTkFrame):
    def __init__(self, parent, app: "VentanaPrincipal") -> None:
        super().__init__(parent, fg_color=COLORES["fondo_principal"])
        self.app = app
        self.grid_columnconfigure(0, weight=1)


class PantallaLogin(PantallaBase):
    def __init__(self, parent, app: "VentanaPrincipal") -> None:
        super().__init__(parent, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)

        panel_marca = ctk.CTkFrame(self, fg_color=COLORES["fondo_panel"], corner_radius=0)
        panel_marca.grid(row=0, column=0, sticky="nsew")
        panel_form = ctk.CTkFrame(self, fg_color=COLORES["fondo_principal"], corner_radius=0)
        panel_form.grid(row=0, column=1, sticky="nsew")

        cuerpo_marca = ctk.CTkFrame(panel_marca, fg_color="transparent")
        cuerpo_marca.pack(expand=True, fill="both", padx=30, pady=30)
        if app.logo_grande:
            ctk.CTkLabel(cuerpo_marca, image=app.logo_grande, text="").pack(pady=(10, 8))
        ctk.CTkLabel(
            cuerpo_marca, text="CryptoUGroup", font=FUENTES["titulo_pantalla"], text_color=COLORES["texto_primario"]
        ).pack()
        ctk.CTkLabel(
            cuerpo_marca, text="Data Protection Platform", font=FUENTES["subtitulo"], text_color=COLORES["texto_secundario"]
        ).pack(pady=(0, 10))
        Separador(cuerpo_marca).pack(fill="x", pady=10)
        for texto in (
            "🔐  Encriptacion AES-256 Empresarial",
            "🛡️  Deteccion Automatica de Datos Sensibles",
            "📊  Dashboard de Auditoria en Tiempo Real",
            "⚡  Procesamiento Seguro de Archivos Excel/CSV",
        ):
            ctk.CTkLabel(
                cuerpo_marca, text=texto, font=FUENTES["cuerpo"], text_color=COLORES["texto_secundario"], anchor="w"
            ).pack(fill="x", pady=6)

        formulario = ctk.CTkFrame(
            panel_form,
            fg_color=COLORES["fondo_card"],
            corner_radius=ESPACIADO["radio_card"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        formulario.pack(expand=True, padx=80, pady=60, fill="x")
        ctk.CTkLabel(
            formulario, text="Iniciar Sesion", font=FUENTES["titulo_seccion"], text_color=COLORES["texto_primario"]
        ).pack(pady=(22, 4))
        ctk.CTkLabel(
            formulario,
            text="Accede a tu plataforma de proteccion de datos",
            font=FUENTES["subtitulo"],
            text_color=COLORES["texto_secundario"],
        ).pack(pady=(0, 14))
        self.entrada_usuario = InputEstilizado(formulario, "👤  Usuario")
        self.entrada_usuario.pack(fill="x", padx=30, pady=6)
        self.entrada_password = InputEstilizado(formulario, "🔒  Contrasena", show="*")
        self.entrada_password.pack(fill="x", padx=30, pady=6)
        self.mostrar_password = False
        BotonSecundario(
            formulario,
            "Mostrar/Ocultar Contrasena",
            self._toggle_password,
            width=220,
        ).pack(pady=6)
        BotonPrimario(formulario, "Iniciar Sesion", self._iniciar_sesion).pack(fill="x", padx=30, pady=(10, 8))
        BotonSecundario(formulario, "Registrarse", app.mostrar_registro).pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(
            formulario,
            text="CryptoUGroup v1.0 — Proteccion Empresarial de Datos",
            font=FUENTES["cuerpo_small"],
            text_color=COLORES["texto_muted"],
        ).pack(pady=(0, 16))
        self.entrada_password.bind("<Return>", lambda _event: self._iniciar_sesion())

    def _toggle_password(self) -> None:
        self.mostrar_password = not self.mostrar_password
        self.entrada_password.configure(show="" if self.mostrar_password else "*")

    def _iniciar_sesion(self) -> None:
        payload = {
            "username": self.entrada_usuario.get().strip(),
            "password": self.entrada_password.get().strip(),
        }
        if not payload["username"] or not payload["password"]:
            self.app.mostrar_notificacion("Completa usuario y contrasena", "advertencia")
            return
        try:
            respuesta = requests.post(f"{URL_API}/auth/login", json=payload, timeout=15)
            if respuesta.status_code == 200:
                data = respuesta.json()
                self.app.token_acceso = data.get("access_token", "")
                self.app.nombre_usuario = payload["username"]
                self.app.mostrar_dashboard()
            else:
                detalle = respuesta.json().get("detail", "Credenciales invalidas")
                self.app.mostrar_notificacion(detalle, "error")
        except Exception as error:
            logger.exception("Error en login")
            self.app.mostrar_notificacion(f"No fue posible iniciar sesion: {error}", "error")


class PantallaRegistro(PantallaBase):
    def __init__(self, parent, app: "VentanaPrincipal") -> None:
        super().__init__(parent, app)
        panel = ctk.CTkFrame(
            self,
            fg_color=COLORES["fondo_card"],
            corner_radius=ESPACIADO["radio_card"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        panel.pack(expand=True, padx=220, pady=80, fill="x")
        ctk.CTkLabel(panel, text="Registro de Usuario", font=FUENTES["titulo_seccion"]).pack(pady=(20, 12))
        self.campos = {
            "username": InputEstilizado(panel, "Usuario"),
            "email": InputEstilizado(panel, "Email"),
            "password": InputEstilizado(panel, "Contrasena", show="*"),
            "full_name": InputEstilizado(panel, "Nombre completo"),
        }
        for entrada in self.campos.values():
            entrada.pack(fill="x", padx=30, pady=6)
        BotonPrimario(panel, "Crear cuenta", self._registrar).pack(fill="x", padx=30, pady=(14, 6))
        BotonSecundario(panel, "Volver", app.mostrar_login).pack(fill="x", padx=30, pady=(0, 20))

    def _registrar(self) -> None:
        payload = {clave: entrada.get().strip() for clave, entrada in self.campos.items()}
        if not all(payload.values()):
            self.app.mostrar_notificacion("Todos los campos son obligatorios", "advertencia")
            return
        try:
            respuesta = requests.post(f"{URL_API}/auth/register", json=payload, timeout=15)
            data = respuesta.json()
            if respuesta.status_code in {200, 201}:
                self.app.mostrar_notificacion(data.get("message", "Usuario creado"), "exito")
                self.app.mostrar_login()
            else:
                self.app.mostrar_notificacion(data.get("detail", "Error de registro"), "error")
        except Exception as error:
            logger.exception("Error registrando usuario")
            self.app.mostrar_notificacion(f"No fue posible registrar: {error}", "error")


class TablaLogsAuditoria(ctk.CTkScrollableFrame):
    def __init__(self, parent, app: "VentanaPrincipal") -> None:
        super().__init__(parent, fg_color=COLORES["fondo_card"], corner_radius=ESPACIADO["radio_card"])
        self.app = app
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        for i, titulo in enumerate(["Accion", "Nivel", "Detalle", "Fecha"]):
            ctk.CTkLabel(
                self,
                text=titulo,
                font=FUENTES["etiqueta"],
                text_color=COLORES["texto_muted"],
                fg_color=COLORES["fondo_panel"],
            ).grid(row=0, column=i, sticky="ew", padx=1, pady=(0, 4))

    def cargar_datos(self, registros: list[dict]) -> None:
        for widget in self.winfo_children():
            info = widget.grid_info()
            if info and int(info.get("row", 0)) > 0:
                widget.destroy()
        for indice, registro in enumerate(registros, start=1):
            color_fila = COLORES["fondo_card"] if indice % 2 == 0 else COLORES["fondo_panel"]
            ctk.CTkLabel(self, text=registro.get("accion", ""), fg_color=color_fila, anchor="w").grid(
                row=indice, column=0, sticky="ew", padx=1, pady=1
            )
            nivel = str(registro.get("nivel", "info")).lower()
            nivel_badge = "error" if nivel == "error" else "medio" if nivel == "warning" else "alto"
            badge = BadgeEstado(self, nivel.upper(), nivel_badge)
            badge.grid(row=indice, column=1, padx=8, pady=4)
            ctk.CTkLabel(
                self, text=str(registro.get("detalle", ""))[:90], fg_color=color_fila, anchor="w"
            ).grid(row=indice, column=2, sticky="ew", padx=1, pady=1)
            ctk.CTkLabel(
                self, text=registro.get("fecha_evento", ""), fg_color=color_fila, anchor="w", font=FUENTES["codigo"]
            ).grid(row=indice, column=3, sticky="ew", padx=1, pady=1)


class VistaDashboard(PantallaBase):
    def __init__(self, parent, app: "VentanaPrincipal") -> None:
        super().__init__(parent, app)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, fg_color=COLORES["fondo_panel"], corner_radius=0, width=ESPACIADO["ancho_sidebar"])
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.header = ctk.CTkFrame(self, fg_color=COLORES["fondo_panel"], corner_radius=0, height=ESPACIADO["alto_header"])
        self.header.grid(row=0, column=1, sticky="ew")
        self.header.grid_propagate(False)
        self.contenido = ctk.CTkFrame(self, fg_color=COLORES["fondo_principal"], corner_radius=0)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_header("Dashboard")
        self.pantalla_activa = None
        self.mostrar_pantalla("inicio")

    def _construir_sidebar(self) -> None:
        marca = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        marca.pack(fill="x", padx=16, pady=(14, 8))
        if self.app.logo_pequeno:
            ctk.CTkLabel(marca, image=self.app.logo_pequeno, text="").pack(side="left")
        ctk.CTkLabel(marca, text="CryptoUGroup", font=FUENTES["titulo_seccion"]).pack(side="left", padx=8)
        Separador(self.sidebar).pack(fill="x", padx=12, pady=8)

        opciones = [
            ("📊  Dashboard", "inicio"),
            ("📁  Cargar Archivo", "cargar"),
            ("🔍  Detectar Datos", "detectar"),
            ("⚙️  Configurar", "configurar"),
            ("▶️  Procesar", "procesar"),
            ("🔓  Desencriptar", "desencriptar"),
            ("🧪  Comparar Archivos", "comparar"),
            ("📋  Logs Auditoria", "logs"),
        ]
        for texto, clave in opciones:
            BotonSecundario(self.sidebar, texto, lambda c=clave: self.mostrar_pantalla(c)).pack(
                fill="x", padx=12, pady=4
            )
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True, fill="both")
        Separador(self.sidebar).pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(
            self.sidebar,
            text=f"👤  {self.app.nombre_usuario}\nRol: Operador",
            font=FUENTES["cuerpo_small"],
            text_color=COLORES["texto_secundario"],
            justify="left",
        ).pack(fill="x", padx=12, pady=6)
        BotonPeligro(self.sidebar, "Cerrar Sesion", self.app.mostrar_login).pack(fill="x", padx=12, pady=(0, 14))

    def _construir_header(self, titulo_pantalla: str) -> None:
        for widget in self.header.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.header,
            text=f"Dashboard > {titulo_pantalla}",
            font=FUENTES["cuerpo"],
            text_color=COLORES["texto_secundario"],
        ).pack(side="left", padx=16)
        ctk.CTkLabel(
            self.header,
            text=titulo_pantalla,
            font=FUENTES["titulo_seccion"],
            text_color=COLORES["texto_primario"],
        ).pack(side="left", padx=12)
        BadgeEstado(self.header, f"{self.app.nombre_usuario}  •  Sistema Activo", "alto").pack(side="right", padx=16, pady=14)

    def mostrar_pantalla(self, nombre_pantalla: str) -> None:
        mapeo = {
            "inicio": ("Inicio", self._pantalla_inicio),
            "cargar": ("Cargar Archivo", self._pantalla_cargar),
            "detectar": ("Detectar Datos", self._pantalla_detectar),
            "configurar": ("Configurar Encriptacion", self._pantalla_configurar),
            "procesar": ("Procesar Archivo", self._pantalla_procesar),
            "desencriptar": ("Desencriptar Archivo", self._pantalla_desencriptar),
            "comparar": ("Comparar Archivos", self._pantalla_comparar),
            "logs": ("Logs Auditoria", self._pantalla_logs),
        }
        titulo, constructor = mapeo[nombre_pantalla]
        self._construir_header(titulo)
        if self.pantalla_activa is not None:
            self.pantalla_activa.destroy()
        self.pantalla_activa = constructor()
        self.pantalla_activa.grid(row=0, column=0, sticky="nsew", padx=ESPACIADO["padding_ventana"], pady=ESPACIADO["padding_ventana"])

    def _contenedor_base(self, titulo: str, subtitulo: str = "") -> ctk.CTkFrame:
        contenedor = ctk.CTkFrame(
            self.contenido,
            fg_color=COLORES["fondo_card"],
            corner_radius=ESPACIADO["radio_card"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        ctk.CTkLabel(contenedor, text=titulo, font=FUENTES["titulo_seccion"]).pack(anchor="w", padx=16, pady=(14, 4))
        if subtitulo:
            ctk.CTkLabel(
                contenedor, text=subtitulo, font=FUENTES["subtitulo"], text_color=COLORES["texto_secundario"]
            ).pack(anchor="w", padx=16, pady=(0, 10))
        return contenedor

    def _pantalla_inicio(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Resumen de Plataforma", "Metricas en tiempo real")
        info = self.app.obtener_dashboard()
        tarjetas = ctk.CTkFrame(contenedor, fg_color="transparent")
        tarjetas.pack(fill="x", padx=16, pady=(0, 12))
        tarjetas.grid_columnconfigure((0, 1, 2, 3), weight=1)
        valores = [
            ("Archivos Procesados", str(info["archivos_procesados"]), "📁", COLORES["azul_boton"], "Total procesados"),
            ("Datos Sensibles", str(info["datos_sensibles_detectados"]), "🔍", COLORES["amarillo_texto"], "Campos detectados"),
            ("Encriptaciones", str(sum(info["tipos_encriptacion_usados"].values())), "🔐", COLORES["verde_texto"], "Operaciones exitosas"),
            ("Ultima Actividad", "Reciente", "⏱️", COLORES["texto_link"], "Hace pocos minutos"),
        ]
        for idx, item in enumerate(valores):
            TarjetaMetrica(tarjetas, *item).grid(row=0, column=idx, padx=6, sticky="nsew")
        return contenedor

    def _pantalla_cargar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Cargar Archivo", "Sube archivos .xlsx, .xls o .csv")
        zona = ctk.CTkFrame(
            contenedor,
            fg_color=COLORES["fondo_input"],
            border_width=2,
            border_color=COLORES["azul_boton"],
            corner_radius=12,
            height=220,
        )
        zona.pack(fill="x", padx=16, pady=(0, 10))
        zona.pack_propagate(False)
        ctk.CTkLabel(zona, text="📂", font=("Segoe UI Emoji", 48), text_color=COLORES["texto_secundario"]).pack(pady=(28, 4))
        ctk.CTkLabel(zona, text="Arrastra tu archivo aqui", font=FUENTES["titulo_seccion"]).pack()
        ctk.CTkLabel(
            zona, text="o haz clic para seleccionar\nFormatos soportados: .xlsx, .csv, .xls", text_color=COLORES["texto_secundario"]
        ).pack(pady=4)
        BotonPrimario(zona, "📂  Seleccionar Archivo", self._seleccionar_archivo).pack(pady=10)

        self.preview_carga = ctk.CTkScrollableFrame(contenedor, fg_color=COLORES["fondo_panel"], height=180)
        self.preview_carga.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self._actualizar_preview_carga()
        return contenedor

    def _actualizar_preview_carga(self) -> None:
        for widget in self.preview_carga.winfo_children():
            widget.destroy()
        if not self.app.columnas_detectadas:
            ctk.CTkLabel(self.preview_carga, text="Sin vista previa disponible", text_color=COLORES["texto_muted"]).pack(anchor="w", padx=8, pady=8)
            return
        ctk.CTkLabel(self.preview_carga, text="Columnas detectadas", font=FUENTES["etiqueta"]).pack(anchor="w", padx=8, pady=(8, 4))
        for columna in self.app.columnas_detectadas:
            ctk.CTkLabel(self.preview_carga, text=f"• {columna}", text_color=COLORES["texto_secundario"]).pack(anchor="w", padx=8, pady=2)

    def _seleccionar_archivo(self) -> None:
        ruta = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Datos", "*.csv *.xlsx *.xls")])
        if not ruta:
            return
        self.app.ruta_archivo_local = ruta
        try:
            with open(ruta, "rb") as descriptor:
                archivos = {"archivo": (os.path.basename(ruta), descriptor)}
                respuesta = requests.post(
                    f"{URL_API}/proteccion-datos/subir-archivo",
                    headers=self.app._headers_auth(),
                    files=archivos,
                    timeout=30,
                )
            if respuesta.status_code in {200, 201}:
                self.app.id_archivo_actual = respuesta.json().get("id_archivo", "")
                self.app.analizar_archivo_actual()
                self._actualizar_preview_carga()
                self.app.mostrar_notificacion("Archivo cargado y analizado", "exito")
            else:
                detalle = respuesta.json().get("detail", "No se pudo cargar el archivo")
                self.app.mostrar_notificacion(detalle, "error")
        except Exception as error:
            logger.exception("Error en carga de archivo")
            self.app.mostrar_notificacion(f"Error al cargar: {error}", "error")

    def _pantalla_detectar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Deteccion de Datos Sensibles", "Revision y clasificacion automatica")
        self.switches_inclusion: dict[str, ctk.StringVar] = {}
        tabla = ctk.CTkScrollableFrame(contenedor, fg_color=COLORES["fondo_panel"], height=380)
        tabla.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        encabezados = ["Columna", "Tipo Detectado", "Confianza", "Incluida"]
        fila_head = ctk.CTkFrame(tabla, fg_color=COLORES["fondo_input"])
        fila_head.pack(fill="x", pady=(2, 4))
        for texto in encabezados:
            ctk.CTkLabel(fila_head, text=texto, font=FUENTES["etiqueta"]).pack(side="left", expand=True, padx=8, pady=6)
        if not self.app.columnas_detectadas:
            ctk.CTkLabel(tabla, text="Primero carga y analiza un archivo.", text_color=COLORES["texto_muted"]).pack(pady=12)
            return contenedor
        for columna in self.app.columnas_detectadas:
            sensible = columna in self.app.columnas_sensibles
            fila = ctk.CTkFrame(tabla, fg_color=COLORES["fondo_card"])
            fila.pack(fill="x", pady=2)
            ctk.CTkLabel(fila, text=columna).pack(side="left", expand=True, padx=8, pady=6)
            ctk.CTkLabel(fila, text="Sensible" if sensible else "General").pack(side="left", expand=True, padx=8)
            BadgeEstado(fila, "ALTO" if sensible else "BAJO", "alto" if sensible else "bajo").pack(side="left", expand=True)
            valor_inicial = "on" if columna in self.app.columnas_incluidas else "off"
            variable_inclusion = ctk.StringVar(value=valor_inicial)
            self.switches_inclusion[columna] = variable_inclusion
            ctk.CTkSwitch(fila, text="", variable=variable_inclusion).pack(side="left", expand=True)

        barra_acciones = ctk.CTkFrame(contenedor, fg_color="transparent")
        barra_acciones.pack(fill="x", padx=16, pady=(0, 12))
        BotonPrimario(
            barra_acciones,
            "Guardar seleccion de columnas",
            self._guardar_columnas_incluidas,
        ).pack(side="left", padx=(0, 8))
        BotonSecundario(
            barra_acciones,
            "Usar sugeridas (sensibles)",
            self._usar_sugeridas_sensibles,
        ).pack(side="left")
        return contenedor

    def _guardar_columnas_incluidas(self) -> None:
        columnas = [
            columna
            for columna, variable in self.switches_inclusion.items()
            if variable.get() == "on"
        ]
        self.app.columnas_incluidas = columnas
        self.app.configuraciones_guardadas = []
        if not columnas:
            self.app.mostrar_notificacion(
                "No seleccionaste columnas. No habra proteccion al procesar.",
                "advertencia",
            )
            return
        self.app.mostrar_notificacion(
            f"Seleccion guardada: {len(columnas)} columnas incluidas.",
            "exito",
        )

    def _usar_sugeridas_sensibles(self) -> None:
        self.app.columnas_incluidas = list(self.app.columnas_sensibles)
        self.app.configuraciones_guardadas = []
        self.app.mostrar_notificacion(
            f"Se aplicaron sugeridas: {len(self.app.columnas_incluidas)} columnas.",
            "exito",
        )
        self.mostrar_pantalla("detectar")

    def _pantalla_configurar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Configuracion de Encriptacion", "Define proteccion por columna")
        opciones = [
            "aes-256",
            "hashing",
            "tokenizacion",
            "pseudonimizacion",
            "anonimizacion",
        ]
        self.app.selectores = {}
        scroll = ctk.CTkScrollableFrame(contenedor, fg_color=COLORES["fondo_panel"], height=370)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        columnas_objetivo = (
            self.app.columnas_incluidas
            if self.app.columnas_incluidas
            else list(self.app.columnas_detectadas)
        )
        if not columnas_objetivo:
            ctk.CTkLabel(
                scroll,
                text="No hay columnas para configurar. Ve a Detectar Datos y guarda seleccion.",
                text_color=COLORES["texto_muted"],
            ).pack(anchor="w", padx=10, pady=10)
            return contenedor
        for columna in columnas_objetivo:
            card = ctk.CTkFrame(scroll, fg_color=COLORES["fondo_card"], border_width=1, border_color=COLORES["borde_sutil"])
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=columna, font=FUENTES["etiqueta"]).pack(side="left", padx=10, pady=10)
            combo = ctk.CTkComboBox(card, values=opciones, width=220)
            combo.pack(side="left", padx=8)
            combo.set("aes-256" if columna in self.app.columnas_sensibles else "anonimizacion")
            self.app.selectores[columna] = combo
            ctk.CTkLabel(
                card, text="Nivel seguridad: ★★★★★" if combo.get() == "aes-256" else "Nivel seguridad: ★★★☆☆", text_color=COLORES["texto_secundario"]
            ).pack(side="left", padx=8)
        BotonPrimario(contenedor, "Guardar configuracion", self._guardar_configuracion).pack(
            padx=16, pady=(0, 14), anchor="e"
        )
        return contenedor

    def _guardar_configuracion(self) -> None:
        self.app.configuraciones_guardadas = self.app.obtener_configuraciones_actuales()
        if not self.app.configuraciones_guardadas:
            self.app.mostrar_notificacion("No hay columnas para configurar", "advertencia")
            return
        self.app.mostrar_notificacion("Configuracion guardada correctamente", "exito")

    def _pantalla_procesar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Procesamiento Seguro", "Aplica protecciones y genera archivo final")
        card_clave = ctk.CTkFrame(
            contenedor,
            fg_color=COLORES["fondo_panel"],
            corner_radius=ESPACIADO["radio_input"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        card_clave.pack(fill="x", padx=16, pady=(0, 10))
        ctk.CTkLabel(
            card_clave,
            text="Clave de encriptacion AES (opcional, recomendada para validar desencriptacion)",
            font=FUENTES["etiqueta"],
            text_color=COLORES["texto_secundario"],
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.entrada_clave_procesar = InputEstilizado(
            card_clave, "Clave de usuario para AES", show="*"
        )
        self.entrada_clave_procesar.pack(fill="x", padx=10, pady=(0, 8))
        BotonSecundario(
            card_clave,
            "Mostrar/Ocultar clave",
            self._toggle_clave_procesar,
            width=210,
        ).pack(anchor="w", padx=10, pady=(0, 10))

        resumen = ctk.CTkFrame(
            contenedor,
            fg_color=COLORES["fondo_panel"],
            corner_radius=ESPACIADO["radio_input"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        resumen.pack(fill="x", padx=16, pady=(0, 10))
        ctk.CTkLabel(
            resumen,
            text="Resumen de configuraciones guardadas",
            font=FUENTES["etiqueta"],
            text_color=COLORES["texto_secundario"],
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.resumen_config = ctk.CTkTextbox(
            resumen,
            height=80,
            fg_color=COLORES["fondo_input"],
            text_color=COLORES["texto_primario"],
            font=FUENTES["codigo"],
        )
        self.resumen_config.pack(fill="x", padx=10, pady=(0, 10))
        self._actualizar_resumen_config()

        self.barra = ctk.CTkProgressBar(
            contenedor,
            fg_color=COLORES["fondo_input"],
            progress_color=COLORES["azul_boton"],
            height=10,
            corner_radius=4,
        )
        self.barra.pack(fill="x", padx=16, pady=(6, 8))
        self.barra.set(0)
        self.estado = ctk.CTkLabel(
            contenedor, text="Listo para procesar", text_color=COLORES["texto_secundario"], font=FUENTES["subtitulo"]
        )
        self.estado.pack(pady=(0, 8))

        barra_acciones = ctk.CTkFrame(contenedor, fg_color="transparent")
        barra_acciones.pack(fill="x", padx=16, pady=(0, 10))
        BotonSecundario(
            barra_acciones, "📁  Cargar archivo", lambda: self.mostrar_pantalla("cargar")
        ).pack(side="left", padx=(0, 8))
        BotonPrimario(
            barra_acciones, "▶️  Iniciar procesamiento", self._ejecutar_procesamiento
        ).pack(side="left", padx=(0, 8))
        BotonSecundario(
            barra_acciones, "⬇️  Descargar ultimo resultado", self._descargar_resultado
        ).pack(side="left")

        self.log_texto = ctk.CTkTextbox(
            contenedor, height=280, fg_color=COLORES["fondo_input"], text_color=COLORES["texto_primario"], font=FUENTES["codigo"]
        )
        self.log_texto.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        return contenedor

    def _toggle_clave_procesar(self) -> None:
        if self.entrada_clave_procesar.cget("show") == "*":
            self.entrada_clave_procesar.configure(show="")
        else:
            self.entrada_clave_procesar.configure(show="*")

    def _actualizar_resumen_config(self) -> None:
        self.resumen_config.delete("0.0", "end")
        if not self.app.configuraciones_guardadas:
            self.resumen_config.insert("end", "- Sin configuraciones guardadas.\n")
            self.resumen_config.insert("end", "- Ve a 'Configurar' y guarda antes de procesar.")
            return
        for item in self.app.configuraciones_guardadas:
            self.resumen_config.insert(
                "end", f"- {item['columna']}: {item['tipo_proteccion']}\n"
            )

    def _agregar_log(self, texto: str) -> None:
        self.log_texto.insert("end", f"{texto}\n")
        self.log_texto.see("end")

    def _animar_carga(self, objetivo: float, callback_final: Callable | None = None) -> None:
        valor_actual = self.barra.get()
        if valor_actual < objetivo:
            self.barra.set(min(valor_actual + 0.02, objetivo))
            self.after(30, lambda: self._animar_carga(objetivo, callback_final))
        elif callback_final:
            callback_final()

    def _ejecutar_procesamiento(self) -> None:
        if not self.app.id_archivo_actual:
            self.app.mostrar_notificacion("Primero carga un archivo", "advertencia")
            return
        if not self.app.configuraciones_guardadas:
            configuraciones_actuales = self.app.obtener_configuraciones_actuales()
            if configuraciones_actuales:
                self.app.configuraciones_guardadas = configuraciones_actuales
                self._actualizar_resumen_config()
            else:
                self.app.mostrar_notificacion("Configura y guarda encriptacion primero", "advertencia")
                return
        self._agregar_log("[INFO] Construyendo configuracion...")
        self.estado.configure(text="Procesando configuracion de columnas...")
        self._animar_carga(0.35, self._enviar_procesamiento)

    def _enviar_procesamiento(self) -> None:
        clave_usuario = self.entrada_clave_procesar.get().strip()
        payload = {
            "id_archivo": self.app.id_archivo_actual,
            "configuraciones": list(self.app.configuraciones_guardadas),
            "clave_usuario": clave_usuario or None,
        }
        try:
            self._agregar_log("[INFO] Enviando peticion a backend...")
            respuesta = requests.post(
                f"{URL_API}/proteccion-datos/procesar-archivo",
                headers=self.app._headers_auth(),
                json=payload,
                timeout=90,
            )
            if respuesta.status_code != 200:
                raise ValueError(respuesta.json().get("detail", "Error al procesar"))
            data = respuesta.json()
            self.app.nombre_archivo_procesado = data["nombre_archivo_procesado"]
            self._agregar_log("[SUCCESS] Archivo procesado correctamente.")
            self.estado.configure(text="Proceso finalizado")
            self._animar_carga(1.0)
            self.entrada_clave_procesar.delete(0, "end")
        except Exception as error:
            self._agregar_log(f"[ERROR] {error}")
            self.estado.configure(text="Fallo de procesamiento")
            self.app.mostrar_notificacion(str(error), "error")

    def _descargar_resultado(self) -> None:
        if not self.app.id_archivo_actual:
            self.app.mostrar_notificacion("No hay archivo procesado disponible", "advertencia")
            return
        try:
            descarga = requests.get(
                f"{URL_API}/proteccion-datos/descargar-archivo/{self.app.id_archivo_actual}",
                headers=self.app._headers_auth(),
                timeout=90,
            )
            if descarga.status_code != 200:
                raise ValueError("No se pudo descargar archivo")
            nombre = self.app.nombre_archivo_procesado or "archivo_procesado.csv"
            ruta = filedialog.asksaveasfilename(initialfile=nombre, defaultextension=os.path.splitext(nombre)[1] or ".csv")
            if ruta:
                with open(ruta, "wb") as descriptor:
                    descriptor.write(descarga.content)
                self._agregar_log("[SUCCESS] Archivo descargado")
                self.app.mostrar_notificacion("Archivo descargado correctamente", "exito")
        except Exception as error:
            self._agregar_log(f"[ERROR] {error}")
            self.app.mostrar_notificacion(str(error), "error")

    def _pantalla_logs(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base("Logs de Auditoria", "Consulta trazabilidad de operaciones")
        filtros = ctk.CTkFrame(contenedor, fg_color="transparent")
        filtros.pack(fill="x", padx=16, pady=(0, 8))
        self.filtro_buscar = InputEstilizado(filtros, "Buscar...")
        self.filtro_buscar.pack(side="left", padx=4)
        self.filtro_nivel = ctk.CTkComboBox(filtros, values=["TODOS", "INFO", "WARNING", "ERROR"], width=140)
        self.filtro_nivel.set("TODOS")
        self.filtro_nivel.pack(side="left", padx=4)
        BotonPrimario(filtros, "Aplicar filtros", self._cargar_logs).pack(side="left", padx=4)
        self.tabla_logs = TablaLogsAuditoria(contenedor, self.app)
        self.tabla_logs.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        self.footer_logs = ctk.CTkLabel(contenedor, text="", text_color=COLORES["texto_muted"])
        self.footer_logs.pack(anchor="w", padx=16, pady=(0, 12))
        self._cargar_logs()
        return contenedor

    def _pantalla_desencriptar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base(
            "Desencriptacion de Archivo",
            "Solicita la clave al usuario para revertir AES/token/pseudonimo",
        )
        card = ctk.CTkFrame(
            contenedor,
            fg_color=COLORES["fondo_panel"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        card.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(
            card,
            text="ID de archivo procesado",
            font=FUENTES["etiqueta"],
            text_color=COLORES["texto_secundario"],
        ).pack(anchor="w", padx=12, pady=(10, 4))
        self.entrada_id_desencriptar = InputEstilizado(card, "UUID del archivo")
        if self.app.id_archivo_actual:
            self.entrada_id_desencriptar.insert(0, self.app.id_archivo_actual)
        self.entrada_id_desencriptar.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            card,
            text="Clave de desencriptacion (uso temporal en memoria)",
            font=FUENTES["etiqueta"],
            text_color=COLORES["texto_secundario"],
        ).pack(anchor="w", padx=12, pady=(4, 4))
        self.entrada_clave_desencriptar = InputEstilizado(
            card, "Clave de desencriptacion", show="*"
        )
        self.entrada_clave_desencriptar.pack(fill="x", padx=12, pady=(0, 8))
        BotonSecundario(
            card,
            "Mostrar/Ocultar clave",
            self._toggle_clave_desencriptar,
            width=220,
        ).pack(anchor="w", padx=12, pady=(0, 10))

        acciones = ctk.CTkFrame(card, fg_color="transparent")
        acciones.pack(fill="x", padx=12, pady=(0, 12))
        BotonPrimario(
            acciones,
            "🔓  Desencriptar y descargar",
            self._ejecutar_desencriptacion,
        ).pack(side="left", padx=(0, 8))
        BotonSecundario(
            acciones,
            "Usar ultimo ID cargado",
            self._cargar_id_actual_desencriptar,
        ).pack(side="left")

        self.log_desencriptar = ctk.CTkTextbox(
            contenedor,
            height=260,
            fg_color=COLORES["fondo_input"],
            text_color=COLORES["texto_primario"],
            font=FUENTES["codigo"],
        )
        self.log_desencriptar.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self.log_desencriptar.insert(
            "end",
            "[INFO] Ingrese id_archivo y clave para iniciar desencriptacion.\n",
        )
        return contenedor

    def _toggle_clave_desencriptar(self) -> None:
        if self.entrada_clave_desencriptar.cget("show") == "*":
            self.entrada_clave_desencriptar.configure(show="")
        else:
            self.entrada_clave_desencriptar.configure(show="*")

    def _cargar_id_actual_desencriptar(self) -> None:
        self.entrada_id_desencriptar.delete(0, "end")
        self.entrada_id_desencriptar.insert(0, self.app.id_archivo_actual or "")

    def _ejecutar_desencriptacion(self) -> None:
        id_archivo = self.entrada_id_desencriptar.get().strip()
        clave = self.entrada_clave_desencriptar.get().strip()
        if not id_archivo or not clave:
            self.app.mostrar_notificacion(
                "Debe ingresar id_archivo y clave de desencriptacion", "advertencia"
            )
            return
        payload = {
            "id_archivo": id_archivo,
            "clave_usuario": clave,
            "configuraciones": self.app.configuraciones_guardadas or None,
        }
        try:
            self.log_desencriptar.insert("end", "[INFO] Solicitando desencriptacion...\n")
            respuesta = requests.post(
                f"{URL_API}/proteccion-datos/desencriptar-archivo",
                headers=self.app._headers_auth(),
                json=payload,
                timeout=120,
            )
            if respuesta.status_code != 200:
                raise ValueError(respuesta.json().get("detail", "Error de desencriptacion"))
            nombre_sugerido = f"desencriptado_{id_archivo}.xlsx"
            disposition = respuesta.headers.get("content-disposition", "")
            if "filename=" in disposition:
                nombre_sugerido = disposition.split("filename=")[-1].strip('"')
            ruta = filedialog.asksaveasfilename(
                initialfile=nombre_sugerido, defaultextension=".xlsx"
            )
            if ruta:
                with open(ruta, "wb") as descriptor:
                    descriptor.write(respuesta.content)
                self.log_desencriptar.insert(
                    "end", f"[SUCCESS] Archivo desencriptado guardado: {ruta}\n"
                )
                self.app.mostrar_notificacion("Desencriptacion completada", "exito")
        except Exception as error:
            self.log_desencriptar.insert("end", f"[ERROR] {error}\n")
            self.app.mostrar_notificacion(str(error), "error")
        finally:
            # Limpieza de clave en UI.
            self.entrada_clave_desencriptar.delete(0, "end")

    def _pantalla_comparar(self) -> ctk.CTkFrame:
        contenedor = self._contenedor_base(
            "Comparador de Integridad",
            "Compara archivo original vs archivo desencriptado",
        )
        panel = ctk.CTkFrame(
            contenedor,
            fg_color=COLORES["fondo_panel"],
            border_width=1,
            border_color=COLORES["borde_sutil"],
        )
        panel.pack(fill="x", padx=16, pady=(0, 10))
        self.ruta_original_comparar = ""
        self.ruta_desencriptado_comparar = ""

        fila_1 = ctk.CTkFrame(panel, fg_color="transparent")
        fila_1.pack(fill="x", padx=12, pady=(10, 4))
        BotonSecundario(
            fila_1, "Seleccionar archivo original", self._seleccionar_original_comparar
        ).pack(side="left")
        self.label_original = ctk.CTkLabel(
            fila_1, text="Sin archivo", text_color=COLORES["texto_secundario"]
        )
        self.label_original.pack(side="left", padx=10)

        fila_2 = ctk.CTkFrame(panel, fg_color="transparent")
        fila_2.pack(fill="x", padx=12, pady=(4, 10))
        BotonSecundario(
            fila_2,
            "Seleccionar archivo desencriptado",
            self._seleccionar_desencriptado_comparar,
        ).pack(side="left")
        self.label_desencriptado = ctk.CTkLabel(
            fila_2, text="Sin archivo", text_color=COLORES["texto_secundario"]
        )
        self.label_desencriptado.pack(side="left", padx=10)

        BotonPrimario(panel, "🧪  Ejecutar comparacion", self._ejecutar_comparacion).pack(
            anchor="w", padx=12, pady=(0, 12)
        )

        self.reporte_comparacion = ctk.CTkTextbox(
            contenedor,
            height=300,
            fg_color=COLORES["fondo_input"],
            text_color=COLORES["texto_primario"],
            font=FUENTES["codigo"],
        )
        self.reporte_comparacion.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self.reporte_comparacion.insert(
            "end", "[INFO] Seleccione ambos archivos para validar integridad.\n"
        )
        return contenedor

    def _seleccionar_original_comparar(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Archivo original", filetypes=[("Datos", "*.csv *.xlsx *.xls")]
        )
        if ruta:
            self.ruta_original_comparar = ruta
            self.label_original.configure(text=os.path.basename(ruta))

    def _seleccionar_desencriptado_comparar(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Archivo desencriptado",
            filetypes=[("Datos", "*.csv *.xlsx *.xls")],
        )
        if ruta:
            self.ruta_desencriptado_comparar = ruta
            self.label_desencriptado.configure(text=os.path.basename(ruta))

    def _ejecutar_comparacion(self) -> None:
        if not self.ruta_original_comparar or not self.ruta_desencriptado_comparar:
            self.app.mostrar_notificacion(
                "Debe seleccionar archivo original y desencriptado", "advertencia"
            )
            return
        try:
            with open(self.ruta_original_comparar, "rb") as original, open(
                self.ruta_desencriptado_comparar, "rb"
            ) as desencriptado:
                archivos = {
                    "archivo_original": (
                        os.path.basename(self.ruta_original_comparar),
                        original,
                    ),
                    "archivo_desencriptado": (
                        os.path.basename(self.ruta_desencriptado_comparar),
                        desencriptado,
                    ),
                }
                respuesta = requests.post(
                    f"{URL_API}/proteccion-datos/comparar-archivos",
                    headers=self.app._headers_auth(),
                    files=archivos,
                    timeout=120,
                )
            if respuesta.status_code != 200:
                raise ValueError(respuesta.json().get("detail", "Error al comparar"))
            data = respuesta.json()
            self.reporte_comparacion.delete("0.0", "end")
            self.reporte_comparacion.insert(
                "end", f"Coincidencia: {data['coincidencia']}%\n"
            )
            self.reporte_comparacion.insert(
                "end", f"Filas iguales: {data['filas_iguales']}\n"
            )
            self.reporte_comparacion.insert(
                "end", f"Filas diferentes: {data['filas_diferentes']}\n"
            )
            self.reporte_comparacion.insert(
                "end",
                f"Columnas con error: {', '.join(data['columnas_con_error']) or 'Ninguna'}\n\n",
            )
            self.reporte_comparacion.insert("end", "Detalle (max 20 filas):\n")
            for item in data.get("detalle", [])[:20]:
                self.reporte_comparacion.insert(
                    "end",
                    f"- Fila {item['fila']} | {item['columna']} | "
                    f"original='{item['valor_original']}' vs "
                    f"desencriptado='{item['valor_desencriptado']}'\n",
                )
            self.app.mostrar_notificacion("Comparacion completada", "exito")
        except Exception as error:
            self.reporte_comparacion.insert("end", f"[ERROR] {error}\n")
            self.app.mostrar_notificacion(str(error), "error")

    def _cargar_logs(self) -> None:
        try:
            respuesta = requests.get(
                f"{URL_API}/proteccion-datos/logs-auditoria",
                headers=self.app._headers_auth(),
                timeout=20,
            )
            registros = respuesta.json() if respuesta.status_code == 200 else []
            texto = self.filtro_buscar.get().strip().lower()
            nivel = self.filtro_nivel.get().strip().upper()
            filtrados = []
            for item in registros:
                pasa_texto = not texto or texto in str(item).lower()
                pasa_nivel = nivel == "TODOS" or item.get("nivel", "").upper() == nivel
                if pasa_texto and pasa_nivel:
                    filtrados.append(item)
            self.tabla_logs.cargar_datos(filtrados)
            self.footer_logs.configure(text=f"Mostrando {len(filtrados)} de {len(registros)} registros")
        except Exception as error:
            logger.exception("Error cargando logs")
            self.app.mostrar_notificacion(f"No fue posible cargar logs: {error}", "error")


class VentanaPrincipal(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CryptoUGroup — Data Protection Platform")
        self.geometry("1200x750")
        self.minsize(1200, 750)
        self.configure(fg_color=COLORES["fondo_principal"])

        self.token_acceso = ""
        self.nombre_usuario = "Invitado"
        self.id_archivo_actual = ""
        self.ruta_archivo_local = ""
        self.nombre_archivo_procesado = ""
        self.columnas_detectadas: list[str] = []
        self.columnas_sensibles: list[str] = []
        self.columnas_incluidas: list[str] = []
        self.selectores: dict[str, ctk.CTkComboBox] = {}
        self.configuraciones_guardadas: list[dict[str, str]] = []
        self.logo_grande: ctk.CTkImage | None = None
        self.logo_pequeno: ctk.CTkImage | None = None
        self._cargar_logo()

        self.contenedor = ctk.CTkFrame(self, fg_color=COLORES["fondo_principal"])
        self.contenedor.pack(fill="both", expand=True)
        self.pantalla_actual = None
        self.mostrar_login()

    def _buscar_logo(self) -> Path | None:
        base = Path(__file__).resolve().parent
        candidatos = [
            base / "images" / "logo.png",
            base / "images" / "Logo.png",
            base / "Imagenes" / "Logo.png",
            base / "Imagenes" / "Logo.jpeg",
        ]
        for ruta in candidatos:
            if ruta.exists():
                return ruta
        return None

    def _cargar_logo(self) -> None:
        ruta_logo = self._buscar_logo()
        if not ruta_logo:
            logger.warning("No se encontro logo en images/ o Imagenes/")
            return
        imagen = Image.open(ruta_logo)
        self.logo_grande = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(120, 120))
        self.logo_pequeno = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(40, 40))

    def _mostrar_pantalla(self, pantalla: ctk.CTkFrame) -> None:
        if self.pantalla_actual is not None:
            self.pantalla_actual.destroy()
        self.pantalla_actual = pantalla
        self.pantalla_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self._mostrar_pantalla(PantallaLogin(self.contenedor, self))

    def mostrar_registro(self) -> None:
        self._mostrar_pantalla(PantallaRegistro(self.contenedor, self))

    def mostrar_dashboard(self) -> None:
        self._mostrar_pantalla(VistaDashboard(self.contenedor, self))

    def _headers_auth(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token_acceso}"}

    def analizar_archivo_actual(self) -> None:
        if not self.id_archivo_actual:
            return
        try:
            respuesta = requests.post(
                f"{URL_API}/proteccion-datos/analizar-archivo",
                headers=self._headers_auth(),
                params={"id_archivo": self.id_archivo_actual},
                timeout=30,
            )
            if respuesta.status_code != 200:
                raise ValueError(respuesta.json().get("detail", "Error en analisis"))
            data = respuesta.json()
            self.columnas_detectadas = data.get("columnas", [])
            self.columnas_sensibles = [item["columna"] for item in data.get("columnas_sensibles", [])]
            self.columnas_incluidas = list(self.columnas_sensibles)
            self.configuraciones_guardadas = []
        except Exception as error:
            logger.exception("Error analizando archivo")
            self.mostrar_notificacion(f"Error en analisis: {error}", "error")

    def obtener_configuraciones_actuales(self) -> list[dict[str, str]]:
        configuraciones: list[dict[str, str]] = []
        for columna, selector in self.selectores.items():
            try:
                tipo = selector.get().strip()
            except Exception:
                tipo = ""
            if not tipo:
                tipo = "aes-256"
            configuraciones.append({"columna": columna, "tipo_proteccion": tipo})
        return configuraciones

    def obtener_dashboard(self) -> dict:
        try:
            respuesta = requests.get(
                f"{URL_API}/proteccion-datos/dashboard",
                headers=self._headers_auth(),
                timeout=15,
            )
            if respuesta.status_code == 200:
                return respuesta.json()
        except Exception as error:
            logger.warning("No se pudo cargar dashboard: %s", error)
        return {
            "archivos_procesados": 0,
            "datos_sensibles_detectados": 0,
            "tipos_encriptacion_usados": {},
        }

    def mostrar_notificacion(self, mensaje: str, tipo: str = "info") -> None:
        if CTkMessagebox is not None:
            icono = "check" if tipo == "exito" else "warning" if tipo == "advertencia" else "cancel" if tipo == "error" else "info"
            CTkMessagebox(title="CryptoUGroup", message=mensaje, icon=icono)
            return
        ctk.CTkInputDialog(text=mensaje, title="CryptoUGroup")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
