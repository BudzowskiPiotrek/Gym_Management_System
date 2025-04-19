from tkinter import ttk, messagebox
import mysql.connector
import re

class WorkoutFrame(ttk.Frame):
    # ----LA PANTALLA DE REGISTRAR ENTRENAMIENTO DIARIO----
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        # Aquí se controla la posición dentro del frame
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título de bienvenida
        ttk.Label(self, text="Bienvenido en registrar entrenamiento diario", font=("Arial", 16)).pack(pady=30)
        
        # Botón para volver atrás
        ttk.Button(self, text="Volver atrás", width=40, command=self.app.mostrar_inicio).pack(pady=10)