# conjunto de metodos para interactuar con el diccionario de posibilidades
class Diccionario:
    def __init__(self, posibilidades):
        self.posibilidades = posibilidades

    def get_posibilidades(self, fila, columna):
        """
        Obtiene las posibilidades para la posición (fila, columna).
        """
        return self.posibilidades.get((fila, columna), set())

    def set_posibilidades(self, fila, columna, valores):
        """
        Establece las posibilidades para la posición (fila, columna).
        """
        self.posibilidades[(fila, columna)] = valores

    def eliminar_posibilidad(self, fila, columna, valor):
        """
        Elimina un valor de las posibilidades en la posición (fila, columna).
        """
        if (fila, columna) in self.posibilidades:
            self.posibilidades[(fila, columna)].discard(valor)