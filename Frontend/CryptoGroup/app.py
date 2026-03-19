import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import os


COLOR_FONDO = "#0f172a"
COLOR_PANEL = "#1e293b"
COLOR_BOTON = "#2563eb"
COLOR_TEXTO = "white"

# -------- AJUSTAR FONDO --------
def ajustar_fondo(event):
    ancho = event.width
    alto = event.height
    imagen_redimensionada = imagen_original.resize((ancho, alto))
    fondo = ImageTk.PhotoImage(imagen_redimensionada)
    label_fondo.config(image=fondo)
    label_fondo.image = fondo


# -------- LIMPIAR VENTANA --------
def limpiar():
    for widget in ventana.winfo_children():
        if widget != label_fondo:
            widget.destroy()


# -------- PANTALLA PRINCIPAL --------
def pantalla_inicio():

    limpiar()

    panel = tk.Frame(
        ventana,
        bg=COLOR_PANEL,
        padx=40,
        pady=30
    )

    panel.place(relx=0.5, rely=0.45, anchor="center")

    titulo = tk.Label(
        panel,
        text="CryptoUGroup",
        font=("Segoe UI", 26, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL
    )
    titulo.pack(pady=10)

    descripcion = tk.Label(
        panel,
        text="""
Servicios de Seguridad Informática

• Encriptación de archivos AES
• Protección de contraseñas
• Seguridad de datos empresariales
• Generación de claves criptográficas

Protegemos la información crítica
mediante tecnologías modernas de cifrado.
""",
        font=("Segoe UI", 11),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL,
        justify="center"
    )
    descripcion.pack(pady=20)

    boton = tk.Button(
        panel,
        text="Iniciar Sesión",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_BOTON,
        fg="white",
        width=20,
        height=2,
        bd=0,
        command=pantalla_login
    )

    boton.pack(pady=10)


# -------- LOGIN --------
import requests

# -------- REGISTRO USUARIO --------
def pantalla_registro():
    limpiar()

    panel = tk.Frame(
        ventana,
        bg=COLOR_PANEL,
        padx=40,
        pady=25
    )
    panel.place(relx=0.5, rely=0.42, anchor="center")

    titulo = tk.Label(
        panel,
        text="Registro de Usuario",
        font=("Segoe UI", 24, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL
    )
    titulo.pack(pady=(0,10))

    tk.Label(panel, text="Usuario", fg=COLOR_TEXTO, bg=COLOR_PANEL, font=("Segoe UI",11)).pack()
    entry_username = tk.Entry(panel, width=25, font=("Segoe UI",11))
    entry_username.pack(pady=8)

    tk.Label(panel, text="Email", fg=COLOR_TEXTO, bg=COLOR_PANEL, font=("Segoe UI",11)).pack()
    entry_email = tk.Entry(panel, width=25, font=("Segoe UI",11))
    entry_email.pack(pady=8)

    tk.Label(panel, text="Contraseña", fg=COLOR_TEXTO, bg=COLOR_PANEL, font=("Segoe UI",11)).pack()
    entry_password = tk.Entry(panel, show="*", width=25, font=("Segoe UI",11))
    entry_password.pack(pady=8)

    tk.Label(panel, text="Nombre Completo", fg=COLOR_TEXTO, bg=COLOR_PANEL, font=("Segoe UI",11)).pack()
    entry_fullname = tk.Entry(panel, width=25, font=("Segoe UI",11))
    entry_fullname.pack(pady=8)

    botones = tk.Frame(panel, bg=COLOR_PANEL)
    botones.pack(pady=20)

    def registrar_usuario():
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()
        full_name = entry_fullname.get()

        if not username or not email or not password or not full_name:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        url = "http://localhost:8000/api/v1/auth/register"
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            if response.status_code == 200 and data.get("success"):
                messagebox.showinfo("Registro", data.get("message", "Registro exitoso"))
                pantalla_inicio()
            else:
                messagebox.showerror("Error", data.get("message", "Error en el registro"))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    boton_registrar = tk.Button(
        botones,
        text="Registrar",
        font=("Segoe UI",11,"bold"),
        bg=COLOR_BOTON,
        fg="white",
        width=12,
        height=1,
        bd=0,
        command=registrar_usuario
    )
    boton_registrar.grid(row=0, column=0, padx=10)

    boton_cancelar = tk.Button(
        botones,
        text="Cancelar",
        font=("Segoe UI",11),
        bg="#475569",
        fg="white",
        width=12,
        height=1,
        bd=0,
        command=pantalla_inicio
    )
    boton_cancelar.grid(row=0, column=1, padx=10)

    entry_username.focus()

# -------- LOGIN --------
def pantalla_login():

    limpiar()

    panel = tk.Frame(
        ventana,
        bg="#1e293b",
        padx=40,
        pady=25
    )

    panel.place(relx=0.5, rely=0.42, anchor="center")

    titulo = tk.Label(
        panel,
        text="Inicio de Sesión",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#1e293b"
    )
    titulo.pack(pady=(0,10))

    tk.Label(
        panel,
        text="Usuario",
        fg="white",
        bg="#1e293b",
        font=("Segoe UI",11)
    ).pack()

    global entry_usuario
    entry_usuario = tk.Entry(panel, width=25, font=("Segoe UI",11))
    entry_usuario.pack(pady=8)

    tk.Label(
        panel,
        text="Contraseña",
        fg="white",
        bg="#1e293b",
        font=("Segoe UI",11)
    ).pack()

    global entry_password
    entry_password = tk.Entry(panel, show="*", width=25, font=("Segoe UI",11))
    entry_password.pack(pady=8)
    entry_password.bind("<Return>", lambda event: verificar_login())

    # CONTENEDOR BOTONES
    botones = tk.Frame(panel, bg="#1e293b")
    botones.pack(pady=20)

    # BOTON INGRESAR
    boton_ingresar = tk.Button(
        botones,
        text="Ingresar",
        font=("Segoe UI",11,"bold"),
        bg="#2563eb",
        fg="white",
        width=12,
        height=1,
        bd=0,
        command=verificar_login
    )
    boton_ingresar.grid(row=0, column=0, padx=10)

    # BOTON CANCELAR
    boton_cancelar = tk.Button(
        botones,
        text="Cancelar",
        font=("Segoe UI",11),
        bg="#475569",
        fg="white",
        width=12,
        height=1,
        bd=0,
        command=pantalla_inicio
    )
    boton_cancelar.grid(row=0, column=1, padx=10)
    

    # ENTER PARA LOGIN
    entry_password.bind("<Return>", lambda event: verificar_login())

    # FOCO AUTOMATICO
    entry_usuario.focus()

    # -------- VERIFICAR LOGIN --------
def verificar_login():

    usuario = entry_usuario.get()
    password = entry_password.get()

    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "username": usuario,
        "password": password
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # Login exitoso
            data = response.json()
            access_token = data.get("access_token")
            # Obtener info usuario
            headers = {"Authorization": f"Bearer {access_token}"}
            userinfo_url = "http://localhost:8000/api/v1/auth/me"
            try:
                userinfo_resp = requests.get(userinfo_url, headers=headers)
                if userinfo_resp.status_code == 200:
                    userinfo = userinfo_resp.json()
                    panel_seguridad(userinfo)
                else:
                    panel_seguridad(None)
            except Exception:
                panel_seguridad(None)
        else:
            try:
                data = response.json()
                detalle = data.get("detail", "Usuario o contraseña incorrectos")
            except Exception:
                detalle = "Usuario o contraseña incorrectos"
            messagebox.showerror("Error", detalle)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    

# -------- PANEL DE SEGURIDAD --------
def panel_seguridad(userinfo=None):
    limpiar()
    panel = tk.Frame(
        ventana,
        bg=COLOR_PANEL,
        padx=40,
        pady=30
    )
    panel.place(relx=0.5, rely=0.45, anchor="center")
    titulo = tk.Label(
        panel,
        text="Panel de Seguridad",
        font=("Segoe UI", 22, "bold"),
        fg=COLOR_TEXTO,
        bg=COLOR_PANEL
    )
    titulo.pack(pady=15)
    tk.Button(
        panel,
        text="Encriptar Archivo",
        font=("Segoe UI",11,"bold"),
        bg=COLOR_BOTON,
        fg="white",
        width=22,
        height=2,
        bd=0,
        command=encriptar_archivo
    ).pack(pady=10)
    # Botón crear usuario solo para superusuario
    if userinfo and userinfo.get("is_superuser"):
        tk.Button(
            panel,
            text="Crear Usuario",
            font=("Segoe UI",11,"bold"),
            bg=COLOR_BOTON,
            fg="white",
            width=22,
            height=2,
            bd=0,
            command=pantalla_registro
        ).pack(pady=10)
    tk.Button(
        panel,
        text="Cerrar sesión",
        bg="#334155",
        fg="white",
        width=22,
        height=2,
        bd=0,
        command=pantalla_inicio
    ).pack(pady=10)
    tk.Button(
        panel,
        text="Desencriptar Archivo",
        font=("Segoe UI",11,"bold"),
        bg="#16a34a",
        fg="white",
        width=22,
        height=2,
        bd=0,
        command=desencriptar_archivo
    ).pack(pady=10)

# -------- ENCRIPTAR ARCHIVO --------
def encriptar_archivo():
    archivo = filedialog.askopenfilename()
    if not archivo:
        return
    clave = simpledialog.askstring(
        "Clave",
        "Ingrese una clave para encriptar:"
    )
    if not clave:
        return
    key = clave.encode().ljust(16)[:16]
    cipher = AES.new(key, AES.MODE_EAX)
    with open(archivo, "rb") as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    archivo_encriptado = archivo + ".enc"
    with open(archivo_encriptado, "wb") as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    messagebox.showinfo(
        "Encriptación",
        f"Archivo encriptado correctamente:\n{archivo_encriptado}"
    )

# -------- DESENCRIPTAR ARCHIVO --------
def desencriptar_archivo():

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo encriptado",
        filetypes=[("Archivos Encriptados", "*.enc")]
    )

    if not archivo:
        return

    # PEDIR CLAVE AL USUARIO
    clave = tk.simpledialog.askstring(
        "Clave",
        "Ingrese la clave de desencriptación:"
    )

    if not clave:
        return

    try:
        key = clave.encode().ljust(16)[:16]

        with open(archivo, "rb") as f:
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

        data = cipher.decrypt_and_verify(ciphertext, tag)

        archivo_desencriptado = archivo.replace(".enc", "_desencriptado")

        with open(archivo_desencriptado, "wb") as f:
            f.write(data)

        messagebox.showinfo(
            "Desencriptación",
            f"Archivo desencriptado correctamente:\n{archivo_desencriptado}"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            "No se pudo desencriptar el archivo.\nClave incorrecta o archivo corrupto."
        )

# -------- VENTANA --------
ventana = tk.Tk()
ventana.title("CryptoUGroup - Seguridad Informática")
ventana.geometry("800x600")

# -------- IMAGEN --------
import os
import sys

def obtener_ruta(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)

ruta_imagen = obtener_ruta("Imagenes/Logo.png")

imagen_original = Image.open(ruta_imagen)
imagen_original = imagen_original.resize((800,600))

fondo = ImageTk.PhotoImage(imagen_original)

label_fondo = tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

label_fondo.lower()

# -------- INICIO --------
pantalla_inicio()

ventana.mainloop()