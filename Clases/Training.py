from datetime import date

from .ExerciseResult import ExerciseResult


# determina la fecha del entrenamiento, y tiene que tener una lista de resultados
class Training:

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

    def __repr__(self):
        # Representación útil para depuración
        return f"Training(id={self.id}, fecha={self.fecha}, dia='{self.dia}', notas='{self.notas}')"

    def __str__(self):
        # Representación amigable para el usuario
        return f"Entrenamiento del {self.fecha.strftime('%d/%m/%Y')}: {self.dia}"
