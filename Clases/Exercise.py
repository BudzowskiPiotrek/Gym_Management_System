from datetime import date


class Exercise:

    def __init__(
        self,
        id: int,
        nombre: str,
        series: int,
        repsObjetivo: int,
        pesoEstimado: float,
        descanso: int,
        esfuerzoEstimado: int,
    ):
        self.id = id
        self.nombre = nombre
        self.series = series
        self.repsObjetivo = repsObjetivo
        self.pesoEstimado = pesoEstimado
        self.descanso = descanso
        self.esfuerzoEstimado = esfuerzoEstimado

    def __repr__(self):
        return f"Exercise(id={self.id}, nombre='{self.nombre}')"