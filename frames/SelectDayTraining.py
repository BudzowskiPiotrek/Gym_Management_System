import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from Clases.Training import Training 
import re


# --- Clases de Modelo de Datos (Las que proporcionaste) ---
# He añadido un método __repr__ para facilitar la depuración (imprimir objetos).
# --- La nueva clase Frame para la selección ---
class SelectDayTraining(ttk.Frame):
    """
    Un Frame que muestra un desplegable para seleccionar un día de entrenamiento
    de una lista de objetos Entrenamiento.
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        hoy = date.today()
        # Guardamos la lista original de objetos. Es la "fuente de la verdad".
        self.lista_entrenamientos = [
                Training(id=1, fecha=hoy, dia="Día de Pecho y Tríceps", notas="Buen bombeo, energía alta."),
                Training(id=2, fecha=hoy - timedelta(days=2), dia="Día de Espalda y Bíceps", notas="Dominadas con lastre."),
                Training(id=3, fecha=hoy - timedelta(days=4), dia="Día de Pierna", notas="Récord personal en sentadilla."),
                Training(id=4, fecha=hoy - timedelta(days=6), dia="Día de Hombro", notas="Cuidado con el manguito rotador.")
            ]
        self.entrenamiento_seleccionado: Training | None = None

        # --- Configuración del Grid Layout ---
        #self.grid_columnconfigure(0, weight=1)
        self.pack()
        # --- Widgets ---
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
        #self.boton_cargar = ttk.Button(self, text="Cargar Entrenamiento", command=self.cargar_entrenamiento_seleccionado, state="disabled")
        self.boton_cargar = ttk.Button(self, text="Cargar Entrenamiento", command=self.app.mostrar_historial , state="disabled")
        self.boton_cargar.pack(pady=20)
        
        # --- Lógica de llenado y eventos ---
        self.poblar_desplegable()
        self.desplegable.bind("<<ComboboxSelected>>", self.on_seleccion_cambia)

    def poblar_desplegable(self):
        """
        Crea las cadenas de texto para el usuario y las carga en el Combobox.
        """
        opciones_display = []
        for ent in self.lista_entrenamientos:
            # Formateamos una cadena legible para el usuario.
            texto_opcion = f"{ent.dia} - {ent.fecha.strftime('%d/%m/%Y')}"
            opciones_display.append(texto_opcion)
        
        self.desplegable['values'] = opciones_display

    def on_seleccion_cambia(self, event):
        """
        Se ejecuta cuando el usuario selecciona una opción del Combobox.
        """
        # Obtenemos el índice de la opción seleccionada.
        indice_seleccionado = self.desplegable.current()
        
        # Usamos ese índice para buscar el OBJETO REAL en nuestra lista original.
        # Esta es la conexión clave entre la vista (texto) y el modelo (objeto).
        self.entrenamiento_seleccionado = self.lista_entrenamientos[indice_seleccionado]
        
        # Habilitamos el botón de cargar ahora que hay una selección válida.
        self.boton_cargar.config(state="normal")
        print(f"Selección interna cambiada a: {repr(self.entrenamiento_seleccionado)}")

    def cargar_entrenamiento_seleccionado(self):
        """
        Se ejecuta al pulsar el botón. Pasa el objeto seleccionado al controlador principal.
        """
        if self.entrenamiento_seleccionado:
            self.app.cargar_vista_entrenamiento(self.entrenamiento_seleccionado)
        else:
            print("Error: No hay ningún entrenamiento seleccionado.")

