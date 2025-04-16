from tkinter import ttk, messagebox
import mysql.connector
import re


class RegisterFrame(ttk.Frame):
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
        
        # Etiqueta y campo de correo 
        ttk.Label(self, text="Correo").pack(pady=5)
        self.entry_correo = ttk.Entry(self)
        self.entry_correo.pack(pady=5)
        
        # Botones
        ttk.Button(self, text="Confirmar Registro", command=self.registrar_usuario).pack(pady=5)
        ttk.Button(self, text="Volver Atrás", command=self.app.mostrar_login).pack(pady=5)


    # ESTE METODO RECOJE VARIABLE DE NOMBRE Y CONTRASEÑA DE IMPUT, CONECTA CON LA BASE DE DATOS
    # Y SI DA TRUE ARRANCA INICIO DE LA APP (INICIO)
    def registrar_usuario(self):
        nombre = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        correo = self.entry_correo.get()
        
        # EXPRESIONES REGULARES
        patron_usuario = r"^[a-zA-Z][a-zA-Z0-9._]{2,19}$"
        patron_contraseña = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        patron_correo = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        # VALIDAD NOMBRE
        if not re.match(patron_usuario, nombre):
            messagebox.showerror("Error", "El nombre de usuario debe comenzar con una letra y solo puede contener letras, números, puntos o guiones bajos. Debe tener entre 3 y 20 caracteres.")
            return
        # VALIDAD CONTRASEÑA
        if not re.match(patron_contraseña, contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula, un número y un carácter especial (@, $, !, %, *, ?, &).")
            return
        # VALIDAR CORREO ELECTRÓNICO
        if not re.match(patron_correo, correo):
            messagebox.showerror("Error", "El correo electrónico ingresado no tiene un formato válido. Asegúrate de incluir un '@' y un dominio como '.com', '.org', etc.")
            return

        try:
            # ARRANCANDO LA CONEXION
            conexion = mysql.connector.connect(
                host="localhost",  # El host es localhost para XAMPP
                user="root",  # El usuario por defecto de XAMPP es 'root'
                password="",  # No hay contraseña por defecto (***POR AHORA***)
                database="appgym",  # El nombre de la base de datos (***PODEMOS CAMBIARLA CUANDO SEPAMOS NOMBRE DE LA APP***)
            )
            
            # EL CURSO ES UN OBJETO PARA PODER EJECUTAR LENJUAGE DE SQL, LO DE CONSULTAS
            cursor = conexion.cursor()
            
            # CONSULTAR SI EL USUARIO YA EXISTE
            cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombre,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                messagebox.showerror("Error", "El nombre de usuario ya está en uso. Elige otro.")
                return
            
            # INSERTAR NUEVO USUARIO CON tipo = 'Usuario'
            try:
                cursor.execute("INSERT INTO usuario (nombre_usuario, contraseña, correo, tipo) VALUES (%s, %s, %s, %s)",
                    (nombre, contraseña, correo, 'Usuario')
                )
                conexion.commit()   # PARA GUARDAR LOS CAMBIOS EN LA BASE DE DATOS
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario. Error: {e}")
            finally:
                cursor.close()
                conexion.close()
                
        # ESTA PARTE VA DE POR SI NO HAY CONEXION
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos. Error: {e}",)
