import mysql.connector
from tkinter import Tk, messagebox, ttk


class Main:

    # ES UN PRE DISEÑO ESTA APRTE PODEMOS CAMBIAR A NUESTRO AGRADO, POR AHORA CREE ALGO MUY SIMPLE PARA IR PRACTICANDO ES LA PANTALLA DE LOGIN
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Login")
        self.ventana.geometry("600x400")
        self.ventana.resizable(False, False)

        # Contenedor centrado
        frame = ttk.Frame(self.ventana)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta y campo de nombre de usuario
        self.label_usuario = ttk.Label(
            frame, text="Nombre de Usuario", font=("Arial", 12)
        )
        self.label_usuario.pack(pady=(0, 5))

        self.entry_usuario = ttk.Entry(frame, width=30)
        self.entry_usuario.pack(pady=(0, 15))

        # Etiqueta y campo de contraseña
        self.label_contraseña = ttk.Label(frame, text="Contraseña", font=("Arial", 12))
        self.label_contraseña.pack(pady=(0, 5))

        self.entry_contraseña = ttk.Entry(frame, width=30, show="*")
        self.entry_contraseña.pack(pady=(0, 20))

        # Botones
        self.boton_entrar = ttk.Button(
            frame, text="Entrar", command=self.verificar_usuario
        )
        self.boton_entrar.pack(pady=5)

        self.boton_registrar = ttk.Button(frame, text="Registrar")
        self.boton_registrar.pack(pady=5)

        self.ventana.mainloop()

    # BASICAMENTE RECOGE CONTENIDO DE INPUT DE NOMBRE Y CONTRASEÑA Y MIRA SI HAY USUARIO ASI Y CON SU CONTRASEÑA, 
    # HABRA QUE MEJORAR ESTA PARTE, (EXTRESIONES REGULARES PARA QUE NO PEUDAN METERNOS CONSULTA EN EL LOGIN),
    # POR AHORA SOLO AL ENCONTRAR USUARIO ASIVA QUE SE COENCTO PERO NO PARA NADA AQUI METEREMOS YA CAMBIO DE INTEFACE EN FUTURO
    def verificar_usuario(self):
        # Obtener los valores ingresados por el usuario
        nombre_usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        # Conectar a la base de datos MySQL
        try:
            conexion = mysql.connector.connect(
                host="localhost",  # El host es localhost para XAMPP
                user="root",  # El usuario por defecto de XAMPP es 'root'
                password="",  # No hay contraseña por defecto (***POR AHORA***)
                database="appgym",  # El nombre de la base de datos (***PODEMOS CAMBIARLA CUANDO SEPAMOS NOMBRE DE LA APP***)
            )

            cursor = conexion.cursor()

            # Consultar en la base de datos si existe el usuario con la contraseña proporcionada
            cursor.execute(
                """
                SELECT * FROM usuario
                WHERE nombre_usuario = %s AND contraseña = %s
            """,
                (nombre_usuario, contraseña),
            )

            # Comprobar si el usuario existe
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showinfo("Conexión Exitosa", "¡Conectado con éxito!")
            # *** AQUI CARGAMOS EL DEF ( METODO ) QUE CARGA INTERFACE DE USUARIO, SI SERIA DE TIPO USUARIO, OPCIONES USUARIO,
            # SI ADMINSITRADOR, OPCIONES ADMINISTRADOR, SI ENTRENADOR PUES ENTRENADOR
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

            # Cerrar la conexión
            conexion.close()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Error de Conexión",
                f"No se pudo conectar a la base de datos. Error: {e}",
            )


# Ejecutar la interfaz
if __name__ == "__main__":
    Main()
