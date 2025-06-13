from datetime import date

from ExerciseResult import ExerciseResult


# determina la fecha del entrenamiento, y tiene que tener una lista de resultados
class Entrenmiento:

    def __init__(
        self,
        id: int,
        fecha: date,
        dia: str,
        notas: str,
    ):
        self.id = id
        self.fecha = fecha
        self.dia = dia
        self.notas = notas
        self.resultado: list[ExerciseResult] = []  # La lista vacía
