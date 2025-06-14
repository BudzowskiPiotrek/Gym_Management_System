from Clases.Exercise import Exercise


class ExerciseResult:

    def __init__(
        self, id: int, serie: int, repsReales: int, pesoUsado: float, esfuerzoReal: int
    ):

        self.id = id
        self.repsReales = repsReales
        self.pesoUsado = pesoUsado
        self.esfuerzoReal = esfuerzoReal
        self.ejercicios: list[Exercise] = []  # La lista vacía
