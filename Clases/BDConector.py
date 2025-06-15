import mysql.connector
from Clases.Training import Training 
from Clases.Exercise import Exercise 
from Clases.ExerciseResult import ExerciseResult
from Clases.RoutineDay import RoutineDay
from Clases.Routines import Routines

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
            cursor = self.conexion.cursor(dictionary=True)
            # Consulta para verificar nombre de usuario y contraseña
            query = """
                SELECT id, nombre_usuario, tipo FROM usuario
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


    # Este método intenta registrar un nuevo usuario, verificando primero si el nombre de usuario ya existe. 
    # Maneja la conexión y desconexión a la base de datos internamente. 
    # Retorna True si el registro es exitoso, 'usuario_existente' 
    # si el nombre de usuario ya está en uso, False si hay un error de base de datos,
    # o 'error_conexion' si no se pudo conectar.
    def registrar_usuario_bd(self, nombre_usuario, contraseña, correo):
        self.conectar() # Intenta conectar a la base de datos

        if not self.conexion or not self.conexion.is_connected():
            print("Error: No se pudo establecer conexión a la base de datos para el registro.")
            return 'error_conexion'

        try:
            cursor = self.conexion.cursor()
            # CONSULTAR SI EL USUARIO YA EXISTE
            cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombre_usuario,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                cursor.close()
                return 'usuario_existente'
            
            # INSERTAR NUEVO USUARIO CON tipo = 'Usuario'
            cursor.execute("INSERT INTO usuario (nombre_usuario, contraseña, correo, tipo) VALUES (%s, %s, %s, %s)",
                (nombre_usuario, contraseña, correo, 'Usuario')
            )
            self.conexion.commit()   # PARA GUARDAR LOS CAMBIOS EN LA BASE DE DATOS
            cursor.close()
            return True
            
        except mysql.connector.Error as err:
            print(f"Error al registrar usuario: {err}")
            return False
        finally:
            self.desconectar() # Asegura que la conexión se cierre al finalizar


    # CAMBIA LA CONTRASEÑA DE UN USUARIO EXISTENTE EN LA BASE DE DATOS.
    # RETORNA:
    # - True si la contraseña se actualizó correctamente.
    # - False si el usuario no se encuentra o si ocurre un error en la base de datos.
    # - 'error_conexion' si no se pudo establecer la conexión a la base de datos.
    def cambiar_contrasena_bd(self, nombre_usuario, nueva_contraseña):
        self.conectar() # Intenta conectar a la base de datos

        if not self.conexion or not self.conexion.is_connected():
            print("Error: No se pudo establecer conexión a la base de datos para cambiar la contraseña.")
            return 'error_conexion'

        try:
            cursor = self.conexion.cursor()
            # Actualizar la contraseña del usuario
            query = """
                UPDATE usuario
                SET contraseña = %s
                WHERE nombre_usuario = %s
            """
            cursor.execute(query, (nueva_contraseña, nombre_usuario))
            self.conexion.commit() # Guardar los cambios
            
            # Verificar si se actualizó alguna fila
            if cursor.rowcount > 0:
                cursor.close()
                return True
            else:
                cursor.close()
                return False # Usuario no encontrado o contraseña ya era la misma
        except mysql.connector.Error as err:
            print(f"Error al cambiar contraseña: {err}")
            return False
        finally:
            self.desconectar() # Asegura que la conexión se cierre al finalizar


    # CARGA TODOS LOS ENTRENAMIENTOS DE EL USUARIO CON SUS RESULTAODOS
    def CargaEntrenamientos(self, usuario_id: int) -> list[Training]:
        self.conectar()

        if not self.conexion or not self.conexion.is_connected():
            print("Error: No se pudo establecer conexión a la base de datos para cargar entrenamientos.")
            return []

        entrenamientos_cargados: list[Training] = []
        try:
            cursor = self.conexion.cursor(dictionary=True) 
            # PRIMERO CREAMOS OBJETO ENTRENAMIENTO
            query_entrenamientos = """  
                SELECT id, usuario_id, fecha, dia, notas
                FROM entrenamientos
                WHERE usuario_id = %s
                ORDER BY fecha DESC, id DESC
            """
            cursor.execute(query_entrenamientos, (usuario_id,))
            resultados_entrenamientos = cursor.fetchall()

            for row_entrenamiento in resultados_entrenamientos:
                # SE CREA EL OBJETO Y SE LE RELLENA
                entrenamiento = Training(
                    id=row_entrenamiento['id'],
                    fecha=row_entrenamiento['fecha'],
                    dia=row_entrenamiento['dia'],
                    notas=row_entrenamiento['notas']
                )

                # SEGUNDO RELLENAMOS RESUNTADOS DE EJERCICIOS DE LA RUTINA
                query_resultados_ejercicios = """
                    SELECT id, entrenamiento_id, ejercicio_id, serie, repeticiones_reales, peso_usado, esfuerzo_real
                    FROM resultados_ejercicios
                    WHERE entrenamiento_id = %s
                    ORDER BY serie ASC
                """
                cursor.execute(query_resultados_ejercicios, (entrenamiento.id,))
                resultados_ejercicios = cursor.fetchall()

                for row_resultado in resultados_ejercicios:
                    # SE CREA EL OBJETO Y SE LE RELLENA
                    resultado_ejercicio = ExerciseResult(
                        id=row_resultado['id'],
                        entrenamiento_id=row_resultado['entrenamiento_id'], 
                        ejercicio_id=row_resultado['ejercicio_id'],         
                        serie=row_resultado['serie'],
                        repsReales=row_resultado['repeticiones_reales'], 
                        pesoUsado=row_resultado['peso_usado'],
                        esfuerzoReal=row_resultado['esfuerzo_real']
                    )
                    entrenamiento.resultado.append(resultado_ejercicio)
                entrenamientos_cargados.append(entrenamiento)

            cursor.close()
            return entrenamientos_cargados

        except mysql.connector.Error as err:
            print(f"Error al cargar entrenamientos o resultados de ejercicios: {err}")
            return []
        finally:
            self.desconectar()