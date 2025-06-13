from tkinter import ttk, messagebox
from Clases.BDConector import BDConector
import mysql.connector
import re

class SettingsFrame(ttk.Frame):
    # ----LA PANTALLA DE AJUSTES DE USUARIO----
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_conector = BDConector()
        
        # Aquí se controla la posición dentro del frame
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título de bienvenida
        ttk.Label(self, text="Bienvenido en ajustes de usuario o app", font=("Arial", 16)).pack(pady=30)
        
        # Etiqueta y campo para la nueva contraseña
        ttk.Label(self, text="Nueva Contraseña").pack(pady=0)
        self.entry_nueva_contraseña = ttk.Entry(self, width=40, show="*")
        self.entry_nueva_contraseña.pack(pady=5)
        
        # Etiqueta y campo para repetir la nueva contraseña
        ttk.Label(self, text="Repetir Contraseña").pack(pady=0)
        self.entry_repetir_contraseña = ttk.Entry(self, width=40, show="*")
        self.entry_repetir_contraseña.pack(pady=5)
        
        # Botón para cambiar la contraseña
        ttk.Button(self, text="Cambiar Contraseña", width=40, command=self.cambiar_contraseña).pack(pady=10)
        
        # Botón para volver atrás
        ttk.Button(self, text="Volver atrás", width=40, command=self.app.mostrar_inicio).pack(pady=10)

    # METODO PARA EL CAMBIO DE CONTRASEÑA DEL USUARIO
    # PRIMERO VALIDA SI LOS DOS CAMBPOS ESTAN RELLENADOS, DESPUES SI SON IGUALES
    # POSTERIORMENTE OBTENEMOS EL NOMBRE DE USUARIO Y CAMBIAMOS DE CONTRASEÑA
    def cambiar_contraseña(self):
        nueva_contraseña = self.entry_nueva_contraseña.get()
        repetir_contraseña = self.entry_repetir_contraseña.get()
        
        # VALIDACIONES, POR SI ESTAN LLENOS LOS DOS O SI SON IGUALES
        if not nueva_contraseña or not repetir_contraseña:
            messagebox.showerror("Error", "Por favor, introduce y repite la nueva contraseña.")
            return

        if nueva_contraseña != repetir_contraseña:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # EXPRECION REGULAR PARA VALIDAR CONTRASEÑA 
        patron_contraseña = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(patron_contraseña, nueva_contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula, un número y un carácter especial (@, $, !, %, *, ?, &).")
            return

        nombre_usuario_actual = self.app.usuario_datos  # OBTENEMOS NOMBRE DE USUARIO

        if not nombre_usuario_actual:
            messagebox.showerror("Error", "No se ha podido identificar al usuario actual para cambiar la contraseña.")
            return

        # INTENTAMOS CAMBIAR LA CONTRASEÑA
        try:
            resultado_cambio = self.db_conector.cambiar_contrasena_bd(nombre_usuario_actual, nueva_contraseña)
            
            if resultado_cambio is True:
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
                # SE LIMPIA LOS COMENTARIOS
                self.entry_nueva_contraseña.delete(0, 'end')
                self.entry_repetir_contraseña.delete(0, 'end')
            elif resultado_cambio == 'error_conexion':
                messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos. Verifica XAMPP.")
            else:
                messagebox.showerror("Error", "No se pudo cambiar la contraseña. Verifica si el usuario existe o contacta al soporte.")
                
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", f"Ocurrió un error con la base de datos al intentar cambiar la contraseña: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")