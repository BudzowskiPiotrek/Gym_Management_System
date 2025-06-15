import tkinter as tk
from tkinter import ttk
from Clases.BDConector import BDConector
from Clases.Training import Training 
from datetime import date

class SelectNewDayTraining(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_conector = BDConector() # CREAMOS CONECTOR AQUI!
        
        user_id_to_load = getattr(self.app, 'usuario_datos', None)
        if isinstance(user_id_to_load, dict) and 'id' in user_id_to_load: 
            user_id_to_load = user_id_to_load['id']
        elif hasattr(user_id_to_load, 'id'): 
            user_id_to_load = user_id_to_load.id
        self.user_id = user_id_to_load

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
        opciones_display = []
        if self.lista_entrenamientos:
            for ent in self.lista_entrenamientos:
                texto_opcion = f"{ent.dia} - {ent.fecha.strftime('%d/%m/%Y')}"
                opciones_display.append(texto_opcion)
                
        opciones_display.append("--- Nuevo Entrenamiento ---")
        opciones_display.append("Nuevo entreno Piernas")
        opciones_display.append("Nuevo entreno Tirón")
        opciones_display.append("Nuevo entreno Empuje")

        self.desplegable['values'] = opciones_display


    def on_seleccion_cambia(self, event):
        """Maneja el evento cuando cambia la selección en el desplegable."""
        indice_seleccionado = self.desplegable.current()
        opcion_seleccionada = self.desplegable.get() # Obtener la opción seleccionada como texto

        # Mapeo de las nuevas opciones de texto a los nombres de los días de entrenamiento
        nuevos_entrenos_map = {
            "Nuevo entreno Piernas": "Piernas",
            "Nuevo entreno Tirón": "Tirón",
            "Nuevo entreno Empuje": "Empuje"
        }

        # Lógica mejorada para manejar selecciones
        if opcion_seleccionada in nuevos_entrenos_map:
            # Si se seleccionó una de las nuevas opciones de entrenamiento
            dia_entrenamiento = nuevos_entrenos_map[opcion_seleccionada]
            self.entrenamiento_seleccionado = Training(
                id=0, # ID temporal, se actualizará al guardar en BD
                fecha=date.today(), # La fecha de hoy para el nuevo entrenamiento
                dia=dia_entrenamiento,
                notas="Nuevo entrenamiento a crear automáticamente."
            )
            # El botón siempre debe estar normal si es una de estas opciones y hay user_id
            if self.user_id is not None:
                self.boton_cargar.config(state="normal")
            else:
                self.boton_cargar.config(state="disabled") # No permitir si no hay usuario logueado
            print(f"Selección de nuevo entrenamiento: Día '{self.entrenamiento_seleccionado.dia}' (Fecha: {self.entrenamiento_seleccionado.fecha})")
        elif 0 <= indice_seleccionado < len(self.lista_entrenamientos):
            # Si se seleccionó un entrenamiento existente de la base de datos
            self.entrenamiento_seleccionado = self.lista_entrenamientos[indice_seleccionado]
            self.boton_cargar.config(state="normal") # Siempre habilitar si se selecciona un existente
            print(f"Selección de entrenamiento existente: {repr(self.entrenamiento_seleccionado)}")
        else:
            # Si no hay selección válida (ej. el separador "--- Nuevo Entrenamiento ---" o lista vacía)
            self.entrenamiento_seleccionado = None
            self.boton_cargar.config(state="disabled")
            if opcion_seleccionada != "--- Nuevo Entrenamiento ---" and opcion_seleccionada != "No hay entrenamientos disponibles":
                print("Error: Selección fuera de rango o lista vacía o separador seleccionado.")


    def cargar_entrenamiento_seleccionado_y_mostrar_historial(self):

        if self.entrenamiento_seleccionado:
            tipo_dia = self.entrenamiento_seleccionado.dia

            # Llama al método específico según el tipo de día para los nuevos entrenamientos
            if tipo_dia == "Piernas":
                self.ejecutar_metodo_piernas()
            elif tipo_dia == "Tirón":
                self.ejecutar_metodo_tiron()
            elif tipo_dia == "Empuje":
                self.ejecutar_metodo_empuje()
            else:
                # Si es un entrenamiento existente o de otro tipo, ir al registro general
                # Usa self.app.mostrar_entrenamiento para cargar el WorkoutFrame
                self.app.mostrar_entrenamiento(self.entrenamiento_seleccionado)
        else:
            print("Error: No hay ningún entrenamiento seleccionado.")

    def cargar_entrenamiento_seleccionado_y_mostrar_historial(self):
        if self.entrenamiento_seleccionado:
            self.app.mostrar_entrenamiento(self.entrenamiento_seleccionado)
        else:
            print("Error: No hay ningún entrenamiento seleccionado.")


    def ejecutar_metodo_piernas(self):
        print("Ejecutando método para Nuevo entreno Piernas...")
        if self.user_id is not None:
            # Llama al nuevo método del conector para crear el entrenamiento en la BD
            nuevo_entrenamiento_creado = self.db_conector.CrearNuevoEntrenamientoConEjerciciosPredeterminados(
                self.user_id, "Piernas")
            if nuevo_entrenamiento_creado:
                self.app.mostrar_entrenamiento(nuevo_entrenamiento_creado)
            else:
                print("No se pudo crear el nuevo entrenamiento de Piernas en la base de datos.")
        else:
            print("Error: No se pudo obtener el ID del usuario para crear el entrenamiento.")


    def ejecutar_metodo_tiron(self):
        print("Ejecutando método para Nuevo entreno Tirón...")
        if self.user_id is not None:
            nuevo_entrenamiento_creado = self.db_conector.CrearNuevoEntrenamientoConEjerciciosPredeterminados(
                self.user_id, "Tirón")
            if nuevo_entrenamiento_creado:
                self.app.mostrar_entrenamiento(nuevo_entrenamiento_creado)
            else:
                print("No se pudo crear el nuevo entrenamiento de Tirón en la base de datos.")
        else:
            print("Error: No se pudo obtener el ID del usuario para crear el entrenamiento.")


    def ejecutar_metodo_empuje(self):
        print("Ejecutando método para Nuevo entreno Empuje...")
        if self.user_id is not None:
            nuevo_entrenamiento_creado = self.db_conector.CrearNuevoEntrenamientoConEjerciciosPredeterminados(
                self.user_id, "Empuje")
            if nuevo_entrenamiento_creado:
                self.app.mostrar_entrenamiento(nuevo_entrenamiento_creado)
            else:
                print("No se pudo crear el nuevo entrenamiento de Empuje en la base de datos.")
        else:
            print("Error: No se pudo obtener el ID del usuario para crear el entrenamiento.")