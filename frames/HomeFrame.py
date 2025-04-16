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
        
        ttk.Label(self, text="Bienvenido a la app", font=("Arial", 16)).pack(pady=20)