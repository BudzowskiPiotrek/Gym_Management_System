import tkinter as tk
from tkinter import ttk
from Clases.BDConector import BDConector
from datetime import date, timedelta
from Clases.Training import Training 
from Clases.Exercise import Exercise 
from Clases.ExerciseResult import ExerciseResult
from Clases.RoutineDay import RoutineDay
from Clases.Routines import Routines
import re


# --- Clases de Modelo de Datos (Las que proporcionaste) ---
# He añadido un método __repr__ para facilitar la depuración (imprimir objetos).
# --- La nueva clase Frame para la selección ---

class SelectDayTraining(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_conector = BDConector() # CREAMOS CONECTOR AQUI!
        
        user_id_to_load = getattr(self.app, 'usuario_datos', None)
        if isinstance(user_id_to_load, dict) and 'id' in user_id_to_load: 
            user_id_to_load = user_id_to_load['id']
        elif hasattr(user_id_to_load, 'id'): 
            user_id_to_load = user_id_to_load.id

        self.lista_entrenamientos: list[Training] = [] 
        if user_id_to_load is not None:
            print(f"Intentando cargar entrenamientos para el usuario ID: {user_id_to_load}")
            self.lista_entrenamientos = self.db_conector.CargaEntrenamientos(user_id_to_load)
            if not self.lista_entrenamientos:
                print("No se encontraron entrenamientos para este usuario en la base de datos.")
        else:
            print("Advertencia: No se pudo obtener el ID del usuario. No se cargarán entrenamientos desde la base de datos.")


        print("\n--- Entrenamientos Cargados (desde BD o vacíos) ---")
        if self.lista_entrenamientos:

            for ent in self.lista_entrenamientos:
                print(f"ID: {ent.id}, Entrenamiento: '{ent.dia}', Fecha: {ent.fecha}")
        else:
            print("No hay entrenamientos para mostrar.")
        print("--------------------------------------------------\n")


        self.entrenamiento_seleccionado: Training | None = None

        # --- Configuración del Grid Layout ---
        self.pack()
        # --- TEXTO DE ARRIBA ---
        ttk.Label(self, text="Selecciona un Entrenamiento", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Contenedor para el desplegable
        combo_frame = ttk.Frame(self)
        combo_frame.pack(pady=10, padx=20, fill='x')
        combo_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(combo_frame, text="Entrenamiento:").grid(row=0, column=0, padx=(0, 10))
        
        # --- El Desplegable (Combobox) ---
        self.desplegable = ttk.Combobox(combo_frame, state="readonly")
        self.desplegable.grid(row=0, column=1, sticky="ew")

        # --- Botón para Cargar ---
        # El estado inicial dependerá de si hay entrenamientos cargados
        self.boton_cargar = ttk.Button(self, text="Cargar Entrenamiento", command=self.cargar_entrenamiento_seleccionado_y_mostrar_historial, state="disabled")
        self.boton_cargar.pack(pady=20)
        
        # --- Lógica de llenado y eventos ---
        self.poblar_desplegable()
        self.desplegable.bind("<<ComboboxSelected>>", self.on_seleccion_cambia)

        # Pre-seleccionar el primer elemento si la lista no está vacía
        if self.lista_entrenamientos:
            self.desplegable.set(self.desplegable['values'][0]) # Establece el primer elemento como preseleccionado
            self.entrenamiento_seleccionado = self.lista_entrenamientos[0]
            self.boton_cargar.config(state="normal")
            print(f"Pre-selección inicial: {repr(self.entrenamiento_seleccionado)}")
        else:
            self.desplegable.set("No hay entrenamientos disponibles") # Mensaje si no hay nada
            self.boton_cargar.config(state="disabled")


    def poblar_desplegable(self):
        """
        Crea las cadenas de texto para el usuario y las carga en el Combobox
        a partir de la lista de entrenamientos cargados desde la BD.
        """
        opciones_display = []
        if self.lista_entrenamientos:
            for ent in self.lista_entrenamientos:
                # Formateamos una cadena legible para el usuario.
                texto_opcion = f"{ent.dia} - {ent.fecha.strftime('%d/%m/%Y')}"
                opciones_display.append(texto_opcion)
        else:
            opciones_display.append("No hay entrenamientos disponibles")
            
        self.desplegable['values'] = opciones_display

    def on_seleccion_cambia(self, event):
        """
        Se ejecuta cuando cambia la selección en el Combobox.
        """
        # Obtenemos el índice de la opción seleccionada.
        indice_seleccionado = self.desplegable.current()

        if 0 <= indice_seleccionado < len(self.lista_entrenamientos):
            self.entrenamiento_seleccionado = self.lista_entrenamientos[indice_seleccionado]
            # Habilitamos el botón de cargar ahora que hay una selección válida.
            self.boton_cargar.config(state="normal")
            print(f"Selección interna cambiada a: {repr(self.entrenamiento_seleccionado)}")
        else:
            self.entrenamiento_seleccionado = None
            self.boton_cargar.config(state="disabled")
            print("Error: Selección fuera de rango o lista vacía.")


    def cargar_entrenamiento_seleccionado_y_mostrar_historial(self):
        """
        Se ejecuta al pulsar el botón. Pasa el objeto seleccionado al controlador principal.
        """
        if self.entrenamiento_seleccionado:
            # Llama al método de tu `app` para pasar el entrenamiento
            # y mostrar la vista del historial.
            self.app.mostrar_historial(self.entrenamiento_seleccionado)
        else:
            print("Error: No hay ningún entrenamiento seleccionado.")
