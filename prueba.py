import tkinter as tk
from tkinter import ttk
from datetime import date

# --- Clases del Modelo de Datos ---
# En un proyecto real, estas clases estarían en sus propios archivos
# dentro del directorio 'Clases'. Los imports aquí son para que el
# ejemplo sea autoejecutable, pero en tu AppMain.py usarías:
# from Clases.Exercise import Exercise, etc.

class Exercise:
    def __init__(self, id: int, nombre: str, series: int, repsObjetivo: int, pesoEstimado: float, descanso: int, esfuerzoEstimado: int):
        self.id, self.nombre, self.series, self.repsObjetivo, self.pesoEstimado, self.descanso, self.esfuerzoEstimado = id, nombre, series, repsObjetivo, pesoEstimado, descanso, esfuerzoEstimado
    def __repr__(self):
        return f"Exercise(id={self.id}, nombre='{self.nombre}')"

class RoutineDay:
    def __init__(self, id: int, dia: str, grupoMusc: str):
        self.id, self.dia, self.grupoMusc = id, dia, grupoMusc
        self.ejercicios: list[Exercise] = []
    def __repr__(self):
        return f"RoutineDay(id={self.id}, dia='{self.dia}')"

class Routines:
    def __init__(self, id: int, nombre: str, fecha: date):
        self.id, self.nombre, self.fecha = id, nombre, fecha
        self.dia: list[RoutineDay] = []
    def __repr__(self):
        return f"Routines(id={self.id}, nombre='{self.nombre}')"


# --- Frame de Selección Refactorizado para usar el Modelo de Datos ---
class SeleccionRutinaFrame(ttk.Frame):
    """
    Componente que usa un modelo de datos de objetos para la selección en cascada.
    Este archivo está pensado para ser importado, no ejecutado directamente.
    """
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


# --- Ejemplo de cómo debería ser tu AppMain.py ---
# Este bloque demuestra el uso correcto del componente.
# Ejecuta este script desde la raíz de tu proyecto:
# python frames/SelectRoutine.py (si estás dentro de CursoPython_AppGym)
# O usa tu AppMain.py real.
if __name__ == "__main__":

    # --- Clase App de Demostración Actualizada ---
    class App(tk.Tk):
        def __init__(self, lista_de_rutinas: list[Routines]):
            super().__init__()
            self.title("Selección con Modelo de Datos")
            self.geometry("550x300")
            
            self.datos_rutinas_obj = lista_de_rutinas

            self.container = ttk.Frame(self)
            self.container.pack(fill="both", expand=True)
            self.mostrar_selector_rutina()

        def mostrar_selector_rutina(self):
            # Aquí importas y usas tu frame
            frame = SeleccionRutinaFrame(self.container, self, self.datos_rutinas_obj)
            frame.pack(fill="both", expand=True)

        def iniciar_entrenamiento(self, rutina: Routines, dia: RoutineDay):
            print("\n=== App ha recibido los OBJETOS para continuar ===")
            print(f"  Objeto Rutina: {repr(rutina)}")
            print(f"  Objeto Día: {repr(dia)}")
            print(f"    -> Grupo Muscular: {dia.grupoMusc}")
            print(f"    -> Contiene {len(dia.ejercicios)} ejercicios.")
            print("==================================================")

    # 1. Creamos objetos de ejemplo
    rutina_weider = Routines(id=1, nombre="Weider", fecha=date.today())
    rd_pecho = RoutineDay(id=101, dia="Pecho y Tríceps", grupoMusc="Empuje")
    rd_pecho.ejercicios.append(Exercise(1, "Press Banca", 4, 10, 80, 90, 2))
    rd_espalda = RoutineDay(id=102, dia="Espalda y Bíceps", grupoMusc="Tirón")
    rd_espalda.ejercicios.append(Exercise(2, "Dominadas", 4, 12, 0, 90, 1))
    rutina_weider.dia = [rd_pecho, rd_espalda]

    rutina_power = Routines(id=2, nombre="Powerlifting", fecha=date.today())
    rd_sentadilla = RoutineDay(id=201, dia="Día de Sentadilla", grupoMusc="Pierna")
    rd_sentadilla.ejercicios.append(Exercise(3, "Sentadilla", 5, 5, 140, 180, 3))
    rutina_power.dia = [rd_sentadilla]
    
    lista_de_rutinas_completa = [rutina_weider, rutina_power]
    
    # 3. Arrancamos la aplicación
    app = App(lista_de_rutinas=lista_de_rutinas_completa)
    app.mainloop()
