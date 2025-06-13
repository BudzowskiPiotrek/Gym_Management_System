import mysql.connector

class BDConector:
    def __init__(self):
        self.conexion = None # Inicializa la variable de conexión a None

    def conectar(self,):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",   # El host es localhost para XAMPP
                user="root",        # El usuario por defecto de XAMPP es 'root'
                password="",        # No hay contraseña por defecto (***POR AHORA***)
                database="appgym"   # El nombre de la base de datos (***PODEMOS CAMBIARLA CUANDO SEPAMOS NOMBRE DE LA APP***)
            )
            print("Conexión a la base de datos establecida correctamente.")
            return self.conexion
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.conexion = None
            return None

    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")
        

    # INTENTA INICIAR SESIÓN VERIFICANDO LAS CREDENCIALES DEL USUARIO.
    # MANEJA LA CONEXIÓN Y DESCONEXIÓN A LA BASE DE DATOS INTERNAMENTE.
    # RETORNA EL RESULTADO DE LA CONSULTA (FILA DE USUARIO) SI ES EXITOSO,
    # O NONE SI NO SE ENCUENTRA O HAY UN ERROR.
    def Login(self, nombre_usuario, contraseña):
        self.conectar() # Intenta conectar a la base de datos
        
        if not self.conexion or not self.conexion.is_connected():
            print("Error: No se pudo establecer conexión a la base de datos.")
            return None

        try:
            cursor = self.conexion.cursor()
            # Consulta para verificar nombre de usuario y contraseña
            query = """
                SELECT * FROM usuario
                WHERE nombre_usuario = %s AND contraseña = %s
            """
            cursor.execute(query, (nombre_usuario, contraseña))
            resultado = cursor.fetchone() # Obtiene la primera fila que coincide
            cursor.close()
            return resultado
        except mysql.connector.Error as err:
            print(f"Error al verificar credenciales: {err}")
            return None
        finally:
            self.desconectar() # Asegura que la conexión se cierre al finalizar