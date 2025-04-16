from tkinter import ttk, messagebox
import mysql.connector
import re


class LoginFrame(ttk.Frame):
    # ----LA PANTALLA DE LOGIN----
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        # Aquí se controla la posición dentro del frame
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Etiqueta y campo de nombre de usuario
        ttk.Label(self, text="Nombre de Usuario").pack(pady=5)
        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack(pady=5)
        
        # Etiqueta y campo de contraseña
        ttk.Label(self, text="Contraseña").pack(pady=5)
        self.entry_contraseña = ttk.Entry(self, show="*")
        self.entry_contraseña.pack(pady=5)
        
        # Botones
        ttk.Button(self, text="Entrar", command=self.verificar_usuario).pack(pady=5)
        ttk.Button(self, text="Registrar", command=self.app.mostrar_registro).pack(pady=5)


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
            # ARRANCANDO LA CONEXION
            conexion = mysql.connector.connect(
                host="localhost",   # El host es localhost para XAMPP
                user="root",        # El usuario por defecto de XAMPP es 'root'
                password="",        # No hay contraseña por defecto (***POR AHORA***)
                database="appgym",  # El nombre de la base de datos (***PODEMOS CAMBIARLA CUANDO SEPAMOS NOMBRE DE LA APP***)
            )
            
            # EL CURSO ES UN OBJETO PARA PODER EJECUTAR LENJUAGE DE SQL, LO DE CONSULTAS
            cursor = conexion.cursor()
            
            # CONSULTA EN CUAL DONDE TIENES %S ENTRAN SUS VARIABLES CORESPONDIENTES
            cursor.execute(
                """
                SELECT * FROM usuario
                WHERE nombre_usuario = %s AND contraseña = %s
            """,
                (nombre_usuario, contraseña),
            )
            
            # TE DA TRUE O FALSE DEPENDIENDO SI ENCONTRO LA CONSULTA DE ARRIB
            resultado = cursor.fetchone()
            
            if resultado:
                messagebox.showinfo("Éxito", "Usuario autenticado")
                # (*** JUSTO AQUI HAY QUE CARGAR TODOS DATOS DESDE LA ABSE DE DATOS PARA UNA COLECCION ***)
                self.app.mostrar_inicio()   # CARGA LA PRIMERA PANTALLA DE PROGRAMA PAPI! 
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                
            # APAGANDO LA CONEXION
            conexion.close()
            
        # ESTA PARTE VA DE POR SI NO HAY CONEXION
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", f"No se pudo conectar a la base de datos. Error: {e}")
