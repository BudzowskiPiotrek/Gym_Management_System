from tkinter import Tk
import mysql.connector
from frames.LoginFrame import LoginFrame
from frames.RegisterFrame import RegisterFrame
from frames.HomeFrame import HomeFrame
from frames.RoutineFrame import RoutineFrame
from frames.WorkoutFrame import WorkoutFrame
from frames.HistoryFrame import HistoryFrame
from frames.SettingsFrame import SettingsFrame


class AppMain:
    # *** NO FORMATEAR TEXTO PORFAVOR SINO SE HACE POCO LEIBLE ***
    # *** SE PUEDE REGISTRAR SOLO NUEVOS USUARIOS, NO EXISTE OPCION DE MAS ADMINISTRADORES O ENTRENADORES ***
    # *** MIRAR EN FUTURO COMO ENCRIPTAR CONTRASEÑA ***
    # *** REPLANTEAR LA APP PARA PODER SEGUIR ***
    
    
    # AJUSTES GENERALES DE LA VENTANA
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("App GymBro-2025")
        self.ventana.geometry("600x400")
        self.ventana.resizable(False, False)    # NO PERMITE AGRANDAR NI ACHICAR LA VENTANA
        self.frame_actual = None                # NO HAY NINGUNA FRAME VISIBLE EN INICIO
        self.usuario_datos = None               # <- AQUI SE GUARDARA LA INFORMACION TRAS LOGUEAR
        self.mostrar_login()                    # CARGA LA PRIMERA PANTALLA DE PROGRAMA PAPI
        self.ventana.mainloop()                 # INTERACCION CON USUARIO Y QUE VENTANA QUEDE ABIERTA HASTA CERRARLA


    # RECIBE UNA CLASE DE FRAME PARA MOSTRAR ACTUAL Y DESASER LA ANTERIOR
    def cambiar_frame(self, frame_clase):
        if self.frame_actual:                   # COMPRUEBA SI YA HAY ALGUN FRAME CARGADO
            self.frame_actual.destroy()         # SI ES ASI LO DESTRUYE PARA CARGAR NUEVO
        self.frame_actual = frame_clase(self.ventana, self)


    def mostrar_login(self):
        self.cambiar_frame(LoginFrame)


    def mostrar_registro(self):
        self.cambiar_frame(RegisterFrame)


    def mostrar_inicio(self):
        self.cambiar_frame(HomeFrame)


    def mostrar_rutina(self):
        self.cambiar_frame(RoutineFrame)


    def mostrar_entrenamiento(self):
        self.cambiar_frame(WorkoutFrame)


    def mostrar_historial(self):
        self.cambiar_frame(HistoryFrame)


    def mostrar_ajustes(self):
        self.cambiar_frame(SettingsFrame)


# EJECUTA LA APP SOLO SI ESTE ARCHIVO ES EL PRINCIPAL
# CREA UNA INSTANCIA DE LA VENTANA Y LA INICIA
# ES COMO public static void main(String[] args) EN JAVA
if __name__ == "__main__":
    AppMain()
