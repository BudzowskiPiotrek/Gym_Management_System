import tkinter as tk
from tkinter import ttk

# Imports relativos a la raíz del proyecto
from Clases.Routines import Routines
from Clases.RoutineDay import RoutineDay

class SelectRoutine(ttk.Frame):
    
    def __init__(self, parent, app, lista_rutinas: list[Routines]):
        super().__init__(parent)
        self.app = app
        self.lista_rutinas = lista_rutinas
        self.rutinas_map = {rutina.nombre: rutina for rutina in self.lista_rutinas}
        self.dias_map = {}

        self.grid_columnconfigure(0, weight=1)
        ttk.Label(self, text="Configurar Nuevo Entrenamiento", font=("Arial", 16, "bold")).pack(pady=(20, 15))
        
        rutina_frame = ttk.Frame(self)
        rutina_frame.pack(pady=5, padx=20, fill='x')
        ttk.Label(rutina_frame, text="1. Selecciona la Rutina:", width=25).pack(side="left")
        self.desplegable_rutinas = ttk.Combobox(rutina_frame, state="readonly")
        self.desplegable_rutinas.pack(side="left", fill="x", expand=True)

        dia_frame = ttk.Frame(self)
        dia_frame.pack(pady=5, padx=20, fill='x')
        ttk.Label(dia_frame, text="2. Selecciona el Día:", width=25).pack(side="left")
        self.desplegable_dias = ttk.Combobox(dia_frame, state="disabled")
        self.desplegable_dias.pack(side="left", fill="x", expand=True)
        
        self.boton_continuar = ttk.Button(self, text="Continuar", command=self.confirmar_seleccion, state="disabled")
        self.boton_continuar.pack(pady=25)

        self.poblar_rutinas()
        self.desplegable_rutinas.bind("<<ComboboxSelected>>", self.on_rutina_seleccionada)
        self.desplegable_dias.bind("<<ComboboxSelected>>", self.on_dia_seleccionado)

    def poblar_rutinas(self):
        self.desplegable_rutinas['values'] = list(self.rutinas_map.keys())

    def on_rutina_seleccionada(self, event):
        nombre_rutina_sel = self.desplegable_rutinas.get()
        rutina_obj_sel = self.rutinas_map.get(nombre_rutina_sel)
        if not rutina_obj_sel: return
        self.dias_map = {dia_obj.dia: dia_obj for dia_obj in rutina_obj_sel.dia}
        self.desplegable_dias.set('')
        self.desplegable_dias['values'] = list(self.dias_map.keys())
        self.desplegable_dias.config(state="readonly")
        self.boton_continuar.config(state="disabled")

    def on_dia_seleccionado(self, event):
        self.boton_continuar.config(state="normal")

    def confirmar_seleccion(self):
        nombre_rutina = self.desplegable_rutinas.get()
        nombre_dia = self.desplegable_dias.get()
        rutina_final = self.rutinas_map.get(nombre_rutina)
        dia_final = self.dias_map.get(nombre_dia)
        if rutina_final and dia_final:
            self.app.iniciar_entrenamiento(rutina_final, dia_final)
        else:
            print("Error: Selección incompleta.")
