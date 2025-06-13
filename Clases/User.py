from Routines import Routines
from Training import Training


class User:

    def __init__(
        self, id: int, nombre: str, contraseña: str, tipo: str
    ):  # tipo creo el enum?????

        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña
        self.tipo = tipo
        self.rutinas: list[Routines] = []
        self.entrenamientos: list[Training] = []
