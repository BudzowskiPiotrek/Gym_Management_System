from tkinter import ttk, messagebox
from Clases.BDConector import BDConector
import mysql.connector
import re


class LoginFrame(ttk.Frame):
    # ----LA PANTALLA DE LOGIN----
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_conector = BDConector() # CREAMOS CONECTOR AQUI!
        
        # Aquí se controla la posición dentro del frame
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Etiqueta y campo de nombre de usuario
        ttk.Label(self, text="Nombre de Usuario").pack(pady=0)
        self.entry_usuario = ttk.Entry(self, width=40)
        self.entry_usuario.pack(pady=10)
        
        # Etiqueta y campo de contraseña
        ttk.Label(self, text="Contraseña").pack(pady=0)
        self.entry_contraseña = ttk.Entry(self, width=40, show="*")
        self.entry_contraseña.pack(pady=10)
        
        # Botones
        ttk.Button(self, text="Entrar", width=40, command=self.verificar_usuario).pack(pady=5)
        ttk.Button(self, text="Registrar", width=40, command=self.app.mostrar_registro).pack(pady=5)


    # ESTE METODO RECOJE VARIABLE DE NOMBRE Y CONTRASEÑA DE IMPUT, CONECTA CON LA BASE DE DATOS
    # Y SI DA TRUE ARRANCA INICIO DE LA APP (INICIO)
    def verificar_usuario(self):
        nombre_usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        
        # EXPRESIONES REGULARES
        patron_usuario = r"^[A-Za-z\d@$!%*?&ñÑ]{2,}$"
        patron_contraseña = r"^[A-Za-z\d@$!%*?&ñÑ]{8,}$"
        
        # VALIDAD NOMBRE
        if not re.match(patron_usuario, nombre_usuario):
            messagebox.showerror("Error", "Nombre de usuario inválido")
            return
        # VALIDAD CONTRASEÑA
        if not re.match(patron_contraseña, contraseña):
            messagebox.showerror("Error", "Contraseña inválida")
            return
        
        # CONECTAR A NUESTRA BASE DATOS
        try:
            # Login ya maneja la conexión y desconexión internamente.
            resultado = self.db_conector.Login(nombre_usuario, contraseña)
            
            if resultado:
                messagebox.showinfo("Éxito", "Usuario autenticado")
                self.app.usuario_datos = nombre_usuario # GUARDAMOS NOMBRE DE USUARIO DESPEUS DE ENTRAR
                self.app.mostrar_inicio()   # CARGA LA PRIMERA PANTALLA DE PROGRAMA PAPI! 
                
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                
        # ESTA PARTE VA DE POR SI NO HAY CONEXION O ERROR DE BASE DE DATOS
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", f"Ocurrió un error con la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
