from tkinter import Tk
from tkinter import Tk, ttk
from Clases.Training import Training 
from frames.LoginFrame import LoginFrame
from frames.RegisterFrame import RegisterFrame
from frames.HomeFrame import HomeFrame
from frames.RoutineFrame import RoutineFrame
from frames.WorkoutFrame import WorkoutFrame
from frames.HistoryFrame import HistoryFrame
from frames.SettingsFrame import SettingsFrame
from frames.SelectDayTraining import SelectDayTraining
from frames.SelectNewDayTraining import SelectNewDayTraining


class AppMain():
    # *** NO FORMATEAR TEXTO PORFAVOR SINO SE HACE POCO LEIBLE ***
    # *** SE PUEDE REGISTRAR SOLO NUEVOS USUARIOS, NO EXISTE OPCION DE MAS ADMINISTRADORES O ENTRENADORES ***
    # *** MIRAR EN FUTURO COMO ENCRIPTAR CONTRASEÑA ***
    # *** REPLANTEAR LA APP PARA PODER SEGUIR ***
    
    
    # AJUSTES GENERALES DE LA VENTANA
    def __init__(self):
        
        self.ventana = Tk()
        self.ventana.title("App GymBro-2025")
        self.ventana.geometry("600x400")
        self.ventana.resizable(True, True)    # NO PERMITE AGRANDAR NI ACHICAR LA VENTANA
        
        
        self.style = ttk.Style()
        
        # Configurar el color de fondo de la ventana principal (más neutro)
        self.ventana.configure(bg="#f0f0f0") # Un gris muy claro, casi blanco

        # Configurar el color de fondo para todos los frames (ttk.Frame)
        self.style.configure('TFrame', background='#f0f0f0') 
        
        # Configurar el color de fondo para todos los botones ttk.Button (más pequeño y neutro)
        self.style.configure('TButton', 
                            background='#cccccc', # Gris medio para el fondo del botón
                            foreground='#333333',   # Gris oscuro para el texto del botón
                            font=('Arial', 9), # Fuente un poco más pequeña
                            padding=[5, 2]) # Relleno más pequeño [horizontal, vertical]
        
        # Configurar estilos específicos para diferentes estados del botón (opcional)
        self.style.map('TButton', 
                    background=[('active', '#bbbbbb')], # Gris más claro al pasar el ratón
                    foreground=[('active', '#333333')])

        # Configurar el color de fondo para las etiquetas (ttk.Label)
        self.style.configure('TLabel', 
                            background='#f0f0f0', # Mismo color de fondo que la ventana
                            foreground='#333333', # Color de texto gris oscuro
                            font=('Arial', 9))

        # Configurar el color de fondo para las entradas de texto (ttk.Entry)
        self.style.configure('TEntry', 
                            fieldbackground='white', # Fondo blanco para el campo de entrada
                            foreground='#333333',      # Texto gris oscuro
                            insertbackground='#333333',   # Cursor oscuro
                            bordercolor='#999999',     # Borde gris
                            focusthickness=1,           # Grosor del borde al enfocar
                            focuscolor='#666666')       # Color del borde al enfocar
        # --- Fin de configuración de estilos globales ---
        
        self.frame_actual = None                # NO HAY NINGUNA FRAME VISIBLE EN INICIO
        self.usuario_datos = None               # <- AQUI SE GUARDARA LA INFORMACION TRAS LOGUEAR
        self.mostrar_login()                    # CARGA LA PRIMERA PANTALLA DE PROGRAMA PAPI
        self.ventana.mainloop()                 # INTERACCION CON USUARIO Y QUE VENTANA QUEDE ABIERTA HASTA CERRARLA
        
        
    # RECIBE UNA CLASE DE FRAME PARA MOSTRAR ACTUAL Y DESASER LA ANTERIOR
    def cambiar_frame(self, frame_clase, data=None):
        if self.frame_actual:                   # COMPRUEBA SI YA HAY ALGUN FRAME CARGADO
            self.frame_actual.destroy()         # SI ES ASI LO DESTRUYE PARA CARGAR NUEVO
        if data:
            self.frame_actual = frame_clase(self.ventana, self, data)
        else:
            self.frame_actual = frame_clase(self.ventana, self)
    

    def mostrar_login(self):
        self.cambiar_frame(LoginFrame)


    def mostrar_registro(self):
        self.cambiar_frame(RegisterFrame)


    def mostrar_inicio(self):
        self.cambiar_frame(HomeFrame)


    def mostrar_rutina(self):
        self.cambiar_frame(RoutineFrame)


    def seleccionar_dia_entrenado(self):
        self.cambiar_frame(SelectDayTraining)


    def seleccionar_nuevo_dia_entrenado(self):
        self.cambiar_frame(SelectNewDayTraining)


    def mostrar_entrenamiento(self, entrenamiento_seleccionado: Training):
        self.cambiar_frame(WorkoutFrame, entrenamiento_seleccionado)


    def mostrar_historial(self, entrenamiento_seleccionado: Training):
        self.cambiar_frame(HistoryFrame, entrenamiento_seleccionado)


    def mostrar_ajustes(self):
        self.cambiar_frame(SettingsFrame)


# EJECUTA LA APP SOLO SI ESTE ARCHIVO ES EL PRINCIPAL
# CREA UNA INSTANCIA DE LA VENTANA Y LA INICIA
# ES COMO public static void main(String[] args) EN JAVA
if __name__ == "__main__":
    AppMain()
