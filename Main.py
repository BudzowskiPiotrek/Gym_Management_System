import mysql.connector
import re
from tkinter import Tk, messagebox, ttk


class Main:
    # NO AUTO FORMATEAR PORFAVOR QUE SINO SE HACE POCO LEIBLE.
    
    # ES UN PRE DISEÑO ESTA PARTE PODEMOS CAMBIAR A NUESTRO AGRADO, POR AHORA CREE ALGO MUY SIMPLE PARA IR PRACTICANDO ES LA PANTALLA DE LOGIN
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Login")
        self.ventana.geometry("600x400")
        self.ventana.resizable(False, False)

        # Contenedor centrado
        self.frame_login = ttk.Frame(self.ventana)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta y campo de nombre de usuario
        self.label_usuario = ttk.Label(self.frame_login, text="Nombre de Usuario", font=("Arial", 12))
        self.label_usuario.pack(pady=(0, 5))

        self.entry_usuario = ttk.Entry(self.frame_login, width=30)
        self.entry_usuario.pack(pady=(0, 15))

        # Etiqueta y campo de contraseña
        self.label_contraseña = ttk.Label(self.frame_login, text="Contraseña", font=("Arial", 12))
        self.label_contraseña.pack(pady=(0, 5))

        self.entry_contraseña = ttk.Entry(self.frame_login, width=30, show="*")  # LA PARTE DE SHOW HACE QUE NO SE VEA LA CONTRASEÑA
        self.entry_contraseña.pack(pady=(0, 20))

        # Botones
        self.boton_entrar = ttk.Button(self.frame_login, text="Entrar", command=self.verificar_usuario,)  # SI PULSA ESTE BOTON ARRANCA DEF ( METODO ) DE VERIFICAR_USUARIO
        self.boton_entrar.pack(pady=5)

        self.boton_registrar = ttk.Button(self.frame_login, text="Registrar", command=self.mostrar_registro)
        self.boton_registrar.pack(pady=5)

        self.ventana.mainloop()

    def mostrar_registro(self):
        # OCULTAMOS LO DE LOGIN 
        self.frame_login.place_forget()

        # Crear un nuevo frame para el registro
        self.frame_registro = ttk.Frame(self.ventana)
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center")

        # Elementos de registro
        self.label_usuario_registro = ttk.Label(
            self.frame_registro, text="Nombre de Usuario", font=("Arial", 12)
        )
        self.label_usuario_registro.pack(pady=(0, 5))

        self.entry_usuario_registro = ttk.Entry(self.frame_registro, width=30)
        self.entry_usuario_registro.pack(pady=(0, 15))

        self.label_contraseña_registro = ttk.Label(self.frame_registro, text="Contraseña", font=("Arial", 12))
        self.label_contraseña_registro.pack(pady=(0, 5))

        self.entry_contraseña_registro = ttk.Entry(self.frame_registro, width=30, show="*")
        self.entry_contraseña_registro.pack(pady=(0, 15))

        self.label_correo_registro = ttk.Label(self.frame_registro, text="Correo", font=("Arial", 12))
        self.label_correo_registro.pack(pady=(0, 5))

        self.entry_correo_registro = ttk.Entry(self.frame_registro, width=30)
        self.entry_correo_registro.pack(pady=(0, 15))

        # Botones de selección

        self.boton_registrar_confirmar = ttk.Button(self.frame_registro, text="Confirmar Registro",)
        self.boton_registrar_confirmar.pack(pady=10)
        
        # Botón para volver atrás
        self.boton_volver = ttk.Button(self.frame_registro, text="Volver Atrás", command=self.volver_atras)
        
        self.boton_volver.pack(pady=5)
        
    
    def volver_atras(self):
        # Ocultar el frame de registro
        self.frame_registro.place_forget()
        
        # Mostrar el frame de login
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

    # BASICAMENTE RECOGE CONTENIDO DE INPUT DE NOMBRE Y CONTRASEÑA Y MIRA SI HAY USUARIO ASI Y CON SU CONTRASEÑA,
    # HABRA QUE MEJORAR ESTA PARTE, (EXTRESIONES REGULARES PARA QUE NO PEUDAN METERNOS CONSULTA EN EL LOGIN),
    # POR AHORA SOLO AL ENCONTRAR USUARIO ASIVA QUE SE COENCTO PERO NO PARA NADA AQUI METEREMOS YA CAMBIO DE INTEFACE EN FUTURO

    def verificar_usuario(self):
        nombre_usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        # EXPRESIONES REGULARES ESAS HAY QUE PESAR BIEN, PARA PROTEGER LA APP
        patron_usuario = r"^[a-zA-Z0-9ñÑ]+$"
        patron_contraseña = r"^[a-zA-Z0-9ñÑ]+$"

        # VALIDAD NOMBRE
        if not re.match(patron_usuario, nombre_usuario):
            messagebox.showerror("Error", "El nombre de usuario puede tener solo letras y numeros y letra ñ",)
            return

        # VALIDAD CONTRASEÑA
        if not re.match(patron_contraseña, contraseña):
            messagebox.showerror("Error", "La contraseña de usuario puede tener solo letras y numeros y letra ñ",)
            return

        # CONECTAR A NUESTRA BASE DATOS
        try:
            # ARRANCANDO LA CONEXION
            conexion = mysql.connector.connect(
                host="localhost",  # El host es localhost para XAMPP
                user="root",  # El usuario por defecto de XAMPP es 'root'
                password="",  # No hay contraseña por defecto (***POR AHORA***)
                database="appgym",  # El nombre de la base de datos (***PODEMOS CAMBIARLA CUANDO SEPAMOS NOMBRE DE LA APP***)
            )

            # EL CURSO ES UN OBJETO PARA PODER EJECUTAR LENJUAGE DE SQL, LO DE CONSULTAS
            cursor = conexion.cursor()

            # CONSULTA EN CUAL DONDE TIENES %S ENTRAN SUS VARIABLES CORESPONDIENTES
            cursor.execute(
                """
                SELECT * FROM usuario
                WHERE nombre_usuario = %s AND contraseña = %s
            """,
                (nombre_usuario, contraseña),
            )

            # TE DA TRUE O FALSE DEPENDIENDO SI ENCONTRO LA CONSULTA DE ARRIB
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showinfo("Conexión Exitosa", "¡Conectado con éxito!")
            # *** AQUI CARGAMOS EL DEF ( METODO ) QUE CARGA INTERFACE DE USUARIO, SI SERIA DE TIPO USUARIO, OPCIONES USUARIO,
            # SI ADMINSITRADOR, OPCIONES ADMINISTRADOR, SI ENTRENADOR PUES ENTRENADOR
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

            # APAGANDO LA CONEXION
            conexion.close()

        # ESTA PARTE VA DE POR SI NO HAY CONEXION PERO LO CIERTO QUE A FONDO NO SE COMO VA, ES COPIA PEGAR ESA PARTE
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos. Error: {e}",)


# ES COMO EL VOID MAIN EN JAVA. AHI EMPIEZA LA FIESTA
if __name__ == "__main__":
    Main()
