class Rutina:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def __eq__(self, other):
        if isinstance(other, Rutina):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)