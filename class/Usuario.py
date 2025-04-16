from typing import Set

import CursoPython_AppGym.Rutina as Rutina
import CursoPython_AppGym.TipoUsuario as TipoUsuario


class Usuario:
    def __init__(
        self,
        id: int,
        nombre_usuario: str,
        contrasenia: str,
        correo: str,
        tipo: TipoUsuario
    ):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasnia = contrasenia
        self.correo = correo
        self.tipo = tipo
        self.rutinas: Set[Rutina] = set()

    # Getter y Setter de id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    # Getter y Setter de nombre_usuario
    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, nombre_usuario: str):
        self._nombre_usuario = nombre_usuario

    # Getter y Setter de tipo
    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo: TipoUsuario):
        self._tipo = tipo

    # Getter y Setter de rutinas
    @property
    def rutinas(self):
        return self._rutinas

    @rutinas.setter
    def rutinas(self, rutinas: Set[Rutina]):
        self._rutinas = rutinas