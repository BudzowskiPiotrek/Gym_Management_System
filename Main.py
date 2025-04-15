import mysql.connector
import re
from tkinter import Tk, messagebox, ttk


class Main:
    # NO FORMATEAR TEXTO PORFAVOR SINO SE HACE POCO LEIBLE.
    # *** POR AHORA SE PUEDE REGISTRAR SOLO NUEVOS USUARIOS, NO EXISTE OPCION DE MAS ADMINISTRADORES O ENTRENADORES ***
    # *** YA ESTA FUNCIONAL LO DE REGISTRAL USUARIOS, HABRIA QUE MIRAR EN UN FUTURO LO DE ENCRIPTAR CONTRASEÑAS ***
    # *** PUEDES IR DESAROLLANDO DESDE DEF (METODO) INICIO QUE SERIA COMO PRIMERA VENTANA YA DE APP ***
    # *** YO TENGO UNA COPIA POR SI A CASO, PERO INTENTA SUBIR A UNA RAMA DIFERENTE QUE MAIN ***




    # ----LA PANTALLA DE LOGIN----
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
        self.boton_entrar = ttk.Button(self.frame_login, text="Entrar", command=self.verificar_usuario)    # SI PULSA ESTE BOTON ARRANCA DEF (METODO) DE VERIFICAR_USUARIO
        self.boton_entrar.pack(pady=5)
        
        self.boton_registrar = ttk.Button(self.frame_login, text="Registrar", command=self.mostrar_registro)    # SI PULSAS ESTE BOTON ARRANCA DEF (METODO) DE MOSTRAR REGISTRO
        self.boton_registrar.pack(pady=5)
        
        # INTERACCION CON USUARIO Y QUE VENTANA QUEDE ABIERTA HASTA CERRARLA
        self.ventana.mainloop()



    # ----LA PANTALLA DE REGISTRO----
    def mostrar_registro(self):
        # OCULTAMOS LO DE LOGIN 
        self.frame_login.place_forget()
        
        # Crear un nuevo frame para el registro
        self.frame_registro = ttk.Frame(self.ventana)
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center")
        
        # Etiqueta y campo de nombre de usuario
        self.label_usuario_registro = ttk.Label(self.frame_registro, text="Nombre de Usuario", font=("Arial", 12))
        self.label_usuario_registro.pack(pady=(0, 5))
        
        self.entry_usuario_registro = ttk.Entry(self.frame_registro, width=30)
        self.entry_usuario_registro.pack(pady=(0, 15))
        
        # Etiqueta y campo de contraseña
        self.label_contraseña_registro = ttk.Label(self.frame_registro, text="Contraseña", font=("Arial", 12))
        self.label_contraseña_registro.pack(pady=(0, 5))
        
        self.entry_contraseña_registro = ttk.Entry(self.frame_registro, width=30, show="*")
        self.entry_contraseña_registro.pack(pady=(0, 15))
        
        # Etiqueta y campo de correo 
        self.label_correo_registro = ttk.Label(self.frame_registro, text="Correo", font=("Arial", 12))
        self.label_correo_registro.pack(pady=(0, 5))
        
        self.entry_correo_registro = ttk.Entry(self.frame_registro, width=30)
        self.entry_correo_registro.pack(pady=(0, 15))
        
        # Botones
        self.boton_registrar_confirmar = ttk.Button(self.frame_registro, text="Confirmar Registro", command=self.registrar_usuario)     # SI PULSAS ESTE BOTON ARRANCA DEF (METODO) DE REGISTRAR USUARIO
        self.boton_registrar_confirmar.pack(pady=10)
        
        self.boton_volver = ttk.Button(self.frame_registro, text="Volver Atrás", command=self.volver_atras)     # SI PULSAS ESTE BOTON ARRANCA DEF (METODO) DE VOLVER ATRAS
        self.boton_volver.pack(pady=5)



    # ----LA PANTALLA DE INICIO----
    # AQUI TENEMOS QUE PENSAR BIEN QUE METER YA AQUI QUE YA ES LA PRIMERA PANTALLA DE LA APP,
    # HAZLA A TU AGRADO, Y PRACTICA A VER QUE SALE, POR AHORA SE LOGUEA Y DEJA EL FRAME VACIO xD
    def inicio(self):
        # OCULTAMOS LO DE LOGIN 
        self.frame_login.place_forget()








    # ESTE METODO RECOJE VARIABLE DE NOMBRE Y CONTRASEÑA DE IMPUT, CONECTA CON LA BASE DE DATOS
    # Y SI DA TRUE ARRANCA INICIO DE LA APP (INICIO)
    def verificar_usuario(self):
        nombre_usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        
        # EXPRESIONES REGULARES ESAS HAY QUE PESAR BIEN, PARA PROTEGER LA APP
        patron_usuario = r'^[A-Za-z\d@$!%*?&ñÑ]{2,}$'
        patron_contraseña = r'^[A-Za-z\d@$!%*?&ñÑ]{8,}$'
        
        # VALIDAD NOMBRE
        if not re.match(patron_usuario, nombre_usuario):
            messagebox.showerror("Error", "El nombre de usuario debe tener solo letras, números y los símbolos @$!%*?&. Además, puede incluir la letra 'ñ'. Debe tener al menos 2 caracteres.",)
            return        
        # VALIDAD CONTRASEÑA
        if not re.match(patron_contraseña, contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres y solo puede contener letras, números y los símbolos @$!%*?&. También puede incluir la letra 'ñ'.",)
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
                self.inicio()   # CARGA LA PRIMERA PANTALLA DE PROGRAMA PAPI! 
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                
            # APAGANDO LA CONEXION
            conexion.close()
            
        # ESTA PARTE VA DE POR SI NO HAY CONEXION PERO LO CIERTO QUE A FONDO NO SE COMO VA, ES COPIA PEGAR ESA PARTE
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos. Error: {e}",)



    # ESTE METODO RECOJE VARIABLE DE NOMBRE Y CONTRASEÑA Y CORREO DEL IMPUT, CONECTA CON LA BASE DE DATOS
    # COMPRUEBA SUS EXPRESIONES REGULARES, LUEGO SI EXISTE YA UN USUARIO CON MISMO NOMBRE Y SI CUMPLE CADA
    # UNO DE LOS PARAMETROS PUES GUARDA UN NUEVO REGISTRO EN NUESTRA BASE DE DATOS, CONTRASEÑA NO ESTA INCRIPTADA
    def registrar_usuario(self):
        nombre_usuario = self.entry_usuario_registro.get()
        contraseña = self.entry_contraseña_registro.get()
        correo = self.entry_correo_registro.get()
        
        # EXPRESIONES REGULARES ESAS HAY QUE PESAR BIEN, PARA PROTEGER LA APP
        patron_usuario = r'^[a-zA-Z][a-zA-Z0-9._]{2,19}$'
        patron_contraseña = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        # VALIDAD NOMBRE
        if not re.match(patron_usuario, nombre_usuario):
            messagebox.showerror("Error", "El nombre de usuario debe comenzar con una letra y solo puede contener letras, números, puntos o guiones bajos. Debe tener entre 3 y 20 caracteres.")
            return
        # VALIDAR CONTRASEÑA
        if not re.match(patron_contraseña, contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula, un número y un carácter especial (@, $, !, %, *, ?, &).")
            return
        # VALIDAR CORREO ELECTRÓNICO
        if not re.match(patron_correo, correo):
            messagebox.showerror("Error", "El correo electrónico ingresado no tiene un formato válido. Asegúrate de incluir un '@' y un dominio como '.com', '.org', etc.")
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
            
            # CONSULTAR SI EL USUARIO YA EXISTE
            cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombre_usuario,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                messagebox.showerror("Error", "El nombre de usuario ya está en uso. Elige otro.")
                return
            
            # INSERTAR NUEVO USUARIO CON tipo = 'Usuario'
            try:
                cursor.execute("INSERT INTO usuario (nombre_usuario, contraseña, correo, tipo) VALUES (%s, %s, %s, %s)",
                    (nombre_usuario, contraseña, correo, 'Usuario')
                )
                conexion.commit()   # PARA GUARDAR LOS CAMBIOS EN LA BASE DE DATOS
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario. Error: {e}")
            finally:
                cursor.close()
                conexion.close()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos. Error: {e}",)



    # ESTA BIEN EXPLICADO DENTRO PAPITO.
    def volver_atras(self):
        # OCULTAMOS LO DE REGISTRAR
        self.frame_registro.place_forget()
        
        # MOSTRAMOS LO DE LOGIN
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")



# ES COMO EL VOID MAIN EN JAVA. AHI EMPIEZA LA FIESTA
if __name__ == "__main__":
    Main()
