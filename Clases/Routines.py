from datetime import date
from .RoutineDay import RoutineDay


class Routines:
    def __init__(self,id:int,nombre:str,fecha:date):
        
        self.id=id
        self.nombre=nombre
        self.fecha=fecha
        self.dia: list[RoutineDay] = []#Lista de tipo de dia de entreno