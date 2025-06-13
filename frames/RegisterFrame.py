from tkinter import ttk, messagebox
from Clases.BDConector import BDConector
import mysql.connector
import re


class RegisterFrame(ttk.Frame):
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
        
        # Etiqueta y campo de correo 
        ttk.Label(self, text="Correo").pack(pady=0)
        self.entry_correo = ttk.Entry(self, width=40)
        self.entry_correo.pack(pady=10)
        
        # Botones
        ttk.Button(self, text="Confirmar Registro", width=40, command=self.registrar_usuario).pack(pady=5)
        ttk.Button(self, text="Volver Atrás", width=40, command=self.app.mostrar_login).pack(pady=5)


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

        
        try:                            # Intentar registrar el usuario usando el método de BDConector
            resultado_registro = self.db_conector.registrar_usuario_bd(nombre, contraseña, correo)
            
            if resultado_registro is True:
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                
                self.app.mostrar_login() # Si el registro fue exitoso, volvemos a la pantalla de login
                
            elif resultado_registro == 'usuario_existente':
                messagebox.showerror("Error", "El nombre de usuario ya está en uso. Elige otro.")
                
            elif resultado_registro == 'error_conexion':
                messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para el registro. Verifica XAMPP y la configuración de la BD.")
                
            else:                        # Esto capturaría el 'False' retornado por un error genérico de base de datos
                messagebox.showerror("Error", "No se pudo registrar el usuario debido a un problema interno. Contacta al soporte.")
                
                                        # Captura errores específicos de MySQL que puedan ocurrir durante la interacción
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", f"Ocurrió un error con la base de datos: {e}")
        except Exception as e:          # Captura cualquier otra excepción inesperada
            messagebox.showerror("Error", f"Ocurrió un error inesperado durante el registro: {e}")
