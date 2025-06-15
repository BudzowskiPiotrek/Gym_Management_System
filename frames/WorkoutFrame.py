from tkinter import Tk
from tkinter import ttk, messagebox
from Clases.Training import Training
from Clases.BDConector import BDConector
import mysql.connector
import re
import tkinter as tk # Importar tk para tk.W, tk.END, etc.

class WorkoutFrame(ttk.Frame):
    # ----LA PANTALLA DE REGISTRAR ENTRENAMIENTO DIARIO----

    def __init__(self, parent, app, training_data: Training = None):
        super().__init__(parent)
        self.db_conector = BDConector()
        
        self.app = app
        self.training_data = training_data
        self.entry_popup = None  # Para mantener una referencia al Entry de edición
        self.place(relx=0.5, rely=0.5, anchor="center")


        # --- Configuración del Grid Layout para este Frame ---
        self.grid_rowconfigure(0, weight=0)  # Fila para el título
        self.grid_rowconfigure(1, weight=1)  # Fila para la tabla (expandible)
        self.grid_rowconfigure(2, weight=0)  # Fila para los botones
        self.grid_columnconfigure(0, weight=1)

        # --- Título ---
        ttk.Label(
            self, text="Registro de Entrenamiento", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, pady=(20, 10), padx=10)

        # --- Contenedor para la Tabla y Scrollbar ---
        tree_container = ttk.Frame(self)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # --- Creación y Configuración del Treeview ---
        # Ahora las columnas son para los datos de las series. El nombre del ejercicio va en la columna #0 del árbol.
        column_ids = ("serie", "kg", "reps", "esfuerzo")
        self.tabla = ttk.Treeview(
            tree_container, columns=column_ids, show="tree headings"
        )
        self.tabla.grid(row=0, column=0, sticky="nsew")

        # Configurar la columna principal del árbol (#0) para los nombres de los ejercicios
        self.tabla.heading("#0", text="Ejercicio")
        self.tabla.column("#0", anchor=tk.W, width=100)

        # Configurar las otras columnas
        self.tabla.heading("serie", text="Serie")
        self.tabla.column("serie", width=80, anchor=tk.CENTER)
        self.tabla.heading("kg", text="Peso (KG)")
        self.tabla.column("kg", width=100, anchor=tk.CENTER)
        self.tabla.heading("reps", text="Repeticiones")
        self.tabla.column("reps", width=100, anchor=tk.CENTER)
        self.tabla.heading("esfuerzo", text="Esfuerzo (RIR)")
        self.tabla.column("esfuerzo", width=120, anchor=tk.CENTER)

        # --- Scrollbar ---
        scrollbar = ttk.Scrollbar(
            tree_container, orient=tk.VERTICAL, command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Evento para editar celdas ---
        self.tabla.bind("<Double-1>", self.on_tree_double_click)

        # --- Contenedor para los botones ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        button_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4), weight=1
        )  # Para que los botones se espacien

        # --- Botones ---
        ttk.Button(
            button_frame, text="Volver atrás", command=self.app.mostrar_inicio
        ).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(
            button_frame, text="Limpiar series", command=self.limpiar_tabla_completa # CAMBIO AQUI
        ).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(
            button_frame,
            text="Aumentar Peso (+10%)",
            command=lambda: self.modificar_peso(1.1),
        ).grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(
            button_frame,
            text="Reducir Peso (-10%)",
            command=lambda: self.modificar_peso(0.9),
        ).grid(row=0, column=3, padx=5, sticky="ew")
        ttk.Button(
            button_frame, text="Guardar Cambios", command=self.guardar_cambios
        ).grid(row=0, column=4, padx=5, sticky="ew")

        # --- Llenar la tabla con los datos del entrenamiento si se proporcionan ---
        if self.training_data:
            self.cargar_entrenamiento_en_historial(self.training_data)
        else:
            print("No se proporcionó ningún entrenamiento para mostrar en el historial.")

    # --- Método de clase WorkoutFrame para llenar la tabla ---
    def llenar_tabla(self, training_data: Training):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        ejercicio_nombres = {
            1: "Sentadilla con barra", 2: "Prensa de piernas", 3: "Extensiones de cuádriceps",
            4: "Curl femoral", 5: "Sentadilla búlgara", 6: "Gemelos en máquina de pie",
            7: "Zancadas con mancuernas", 8: "Hip thrust",
            # Empuje:
            9: "Press de banca con barra", 10: "Press inclinado con mancuernas", 11: "Press de hombros con barra",
            12: "Aperturas con mancuernas", 13: "Press francés", 14: "Elevaciones laterales",
            15: "Fondos en paralelas", 16: "Extensiones de tríceps en polea alta",
            # Tirón:
            17: "Dominadas", 18: "Remo con barra", 19: "Jalón al pecho",
            20: "Remo en máquina", 21: "Curl de bíceps con barra", 22: "Face pull",
            23: "Encogimiento de hombros con mancuernas", 24: "Curl de bíceps concentrado"
        }

        ejercicios_agrupados = {}
        if training_data.resultado:
            for resultado_ejercicio in training_data.resultado:
                ejercicio_id = resultado_ejercicio.ejercicio_id
                if ejercicio_id not in ejercicios_agrupados:
                    ejercicios_agrupados[ejercicio_id] = []
                ejercicios_agrupados[ejercicio_id].append(resultado_ejercicio)

            for ejercicio_id, resultados in ejercicios_agrupados.items():
                ejercicio_nombre = ejercicio_nombres.get(ejercicio_id, f"Ejercicio ID: {ejercicio_id}")
                parent_id = self.tabla.insert(
                    parent="", index=tk.END, text=ejercicio_nombre, open=True
                )
                resultados.sort(key=lambda x: x.serie)
                for resultado_serie in resultados:
                    valores_serie = [
                        f"Serie {resultado_serie.serie}",
                        resultado_serie.pesoUsado,
                        resultado_serie.repsReales,
                        resultado_serie.esfuerzoReal
                    ]
                    self.tabla.insert(parent=parent_id, index=tk.END, values=valores_serie)
        else:
            self.tabla.insert("", tk.END, text="No hay resultados de ejercicios para este entrenamiento.", values=("", "", "", ""))

    def limpiar_tabla_completa(self): # Nuevo método para limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        print("Tabla de series limpiada.")

    def cargar_entrenamiento_en_historial(self, entrenamiento: Training):
        self.llenar_tabla(entrenamiento)
        self.grid_slaves(row=0, column=0)[0].config(text=f"Registro de Entrenamiento: {entrenamiento.dia} - {entrenamiento.fecha.strftime('%d/%m/%Y')}")


    def on_tree_double_click(self, event):
        """Maneja el doble clic para iniciar la edición de una celda."""
        if self.entry_popup:
            self.entry_popup.destroy()

        item_id = self.tabla.focus()
        column_id = self.tabla.identify_column(event.x)

        # Solo permitir edición en filas de series (no en ejercicios) y en columnas numéricas
        if not self.tabla.parent(item_id) or column_id in ["#0", "#1"]:
            return

        bbox = self.tabla.bbox(item_id, column_id)
        if not bbox:
            return  # Si la celda no es visible

        x, y, width, height = bbox

        current_value = self.tabla.set(item_id, column_id)

        self.entry_popup = ttk.Entry(self.tabla)
        self.entry_popup.place(x=x, y=y, width=width, height=height)
        self.entry_popup.insert(0, current_value)
        self.entry_popup.focus_set()
        self.entry_popup.select_range(0, tk.END)

        self.entry_popup.bind(
            "<Return>", lambda e: self.guardar_edicion_celda(item_id, column_id)
        )
        self.entry_popup.bind(
            "<FocusOut>", lambda e: self.guardar_edicion_celda(item_id, column_id)
        )


    def guardar_edicion_celda(self, item_id, column_id):
        """Guarda el valor del Entry emergente en el Treeview y lo destruye."""
        if self.entry_popup:
            new_value = self.entry_popup.get()
            self.tabla.set(item_id, column=column_id, value=new_value)
            self.entry_popup.destroy()
            self.entry_popup = None


    def limpiar_seleccion(self):
        """Limpia los valores numéricos de la serie seleccionada."""
        selected_items = self.tabla.selection()
        for item_id in selected_items:
            if self.tabla.parent(item_id):  # Asegurarse de que es una serie
                self.tabla.set(item_id, "kg", "")
                self.tabla.set(item_id, "reps", "")
                self.tabla.set(item_id, "esfuerzo", "")


    def modificar_peso(self, incremento):
        """Aumenta o reduce el peso de las series seleccionadas."""
        selected_items = self.tabla.selection()
        for item_id in selected_items:
            if self.tabla.parent(item_id):  # Asegurarse de que es una serie
                try:
                    peso_actual = float(self.tabla.set(item_id, "kg"))
                    nuevo_peso = peso_actual * incremento
                    self.tabla.set(item_id, "kg", nuevo_peso)
                except (ValueError, TypeError):
                    print(
                        f"La celda de peso para el item {item_id} no contiene un número válido."
                    )


    def guardar_cambios(self):
        datos_finales = {}
        for parent_id in self.tabla.get_children():
            ejercicio = self.tabla.item(parent_id, "text")
            series = []
            for child_id in self.tabla.get_children(parent_id):
                valores = self.tabla.item(child_id, "values")[1:]
                series.append(valores)
            datos_finales[ejercicio] = series

        # GUARDAR EN BASE DE DATOS
        if hasattr(self.app, "db_conector"):
            # Opcionalmente puedes pasar más datos como el ID del entrenamiento
            self.app.db_conector.guardar_resultados_entrenamiento(datos_finales, self.training_data.id)
            print("¡Cambios guardados en la base de datos!")
        else:
            print("No se encontró el conector a base de datos.")

        import json

        print(json.dumps(datos_finales, indent=2))
        print("-----------------------")