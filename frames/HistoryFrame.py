import tkinter as tk
from tkinter import ttk
from Clases.Training import Training

class HistoryFrame(ttk.Frame):

    def __init__(self, parent, app, training_data: Training = None):
        super().__init__(parent)
        self.app = app
        self.training_data = training_data 
        
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_rowconfigure(2, weight=0)  
        self.grid_columnconfigure(0, weight=1)
        
        ttk.Label(
            self, text="Registro de Entrenamiento", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, pady=(20, 10), padx=10)

        tree_container = ttk.Frame(self)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        column_ids = ("serie", "kg", "reps", "esfuerzo")
        self.tabla = ttk.Treeview(
            tree_container, columns=column_ids, show="tree headings"
        )
        self.tabla.grid(row=0, column=0, sticky="nsew")

        self.tabla.heading("#0", text="Ejercicio")
        self.tabla.column("#0", anchor=tk.W, width=100)

        self.tabla.heading("serie", text="Serie")
        self.tabla.column("serie", width=80, anchor=tk.CENTER)
        self.tabla.heading("kg", text="Peso (KG)")
        self.tabla.column("kg", width=100, anchor=tk.CENTER)
        self.tabla.heading("reps", text="Repeticiones")
        self.tabla.column("reps", width=100, anchor=tk.CENTER)
        self.tabla.heading("esfuerzo", text="Esfuerzo (RIR)")
        self.tabla.column("esfuerzo", width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(
            tree_container, orient=tk.VERTICAL, command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1) 

        ttk.Button(
            button_frame, text="Volver atrás", command=self.app.mostrar_inicio
        ).grid(row=0, column=0, padx=5, sticky="ew")


        if self.training_data:
            self.cargar_entrenamiento_en_historial(self.training_data)
        else:
            print("No se proporcionó ningún entrenamiento para mostrar en el historial.")


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


    def cargar_entrenamiento_en_historial(self, entrenamiento: Training):
        self.llenar_tabla(entrenamiento)
        self.grid_slaves(row=0, column=0)[0].config(text=f"Registro de Entrenamiento: {entrenamiento.dia} - {entrenamiento.fecha.strftime('%d/%m/%Y')}")