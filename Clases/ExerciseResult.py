from .Exercise import Exercise


class ExerciseResult:

    def __init__(
        self,
        id: int,
        entrenamiento_id: int,  
        ejercicio_id: int,  
        serie: int,
        repsReales: int,
        pesoUsado: float,
        esfuerzoReal: int,
    ):

        self.id = id
        self.entrenamiento_id = entrenamiento_id 
        self.ejercicio_id = ejercicio_id     
        self.serie = serie
        self.repsReales = repsReales
        self.pesoUsado = pesoUsado
        self.esfuerzoReal = esfuerzoReal

    def __repr__(self):
        return (
            f"ExerciseResult(id={self.id}, entrenamiento_id={self.entrenamiento_id}, "
            f"ejercicio_id={self.ejercicio_id}, serie={self.serie}, "
            f"repsReales={self.repsReales}, pesoUsado={self.pesoUsado}, "
            f"esfuerzoReal={self.esfuerzoReal})"
        )

    def __str__(self):
        return (
            f"Serie {self.serie}: {self.repsReales} reps @ {self.pesoUsado}kg "
            f"(Esfuerzo real: {self.esfuerzoReal})"
        )