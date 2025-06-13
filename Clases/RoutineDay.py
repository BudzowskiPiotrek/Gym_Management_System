from Exercise import Exercise


class RoutineDay:

    def __init__(self, id: int, dia: str, grupoMusc: str):
        self.id = id
        self.dia = dia  # nombre del dia...dia de pierna, dia de empuje...etc
        self.grupoMusc = grupoMusc
        self.ejercicios: list[Exercise] = []  # La lista vacía
