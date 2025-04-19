from tkinter import ttk, messagebox
import mysql.connector
import re

class HomeFrame(ttk.Frame):
    # ----LA PANTALLA DE INICIO----
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        # Aquí se controla la posición dentro del frame
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título de bienvenida
        ttk.Label(self, text="Bienvenido a la app", font=("Arial", 16)).pack(pady=30)
        
        # Botón para Registrar Rutina Nueva
        ttk.Button(self, text="Registrar Rutina Nueva", command=self.app.mostrar_rutina, width=40).pack(pady=20)
        
        # Botón para Registrar Entrenamiento
        ttk.Button(self, text="Registrar Entrenamiento", command=self.app.mostrar_entrenamiento, width=40).pack(pady=20)
        
        # Botón para Historial
        ttk.Button(self, text="Historial de Entrenamientos", command=self.app.mostrar_historial, width=40).pack(pady=20)
        
        # Botón para Ajustes
        ttk.Button(self, text="Ajustes", command=self.app.mostrar_ajustes, width=40).pack(pady=5)
        
        # Botón para Ajustes
        ttk.Button(self, text="Salir", command=self.app.mostrar_login, width=40).pack(pady=5)
        
        