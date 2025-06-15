class Matriz:
    def __init__(self, matrizJuego):
        self.matrizJuego = matrizJuego

    def get_valor(self, fila, columna):
        """
        Obtiene el valor en la posición (fila, columna) de la matriz.
        """
        return self.matrizJuego[fila][columna]

    def set_valor(self, fila, columna, valor):
        """
        Establece el valor en la posición (fila, columna) de la matriz.
        """
        self.matrizJuego[fila][columna] = valor

    def jugada_valida(self, fila, columna, valor):
        """
        Verifica si la jugada es válida en la posición (fila, columna) con el valor dado.
        """
        # Verificar fila
        if valor in self.matrizJuego[fila]:
            return False
        
        # Verificar columna
        for i in range(9):
            if self.matrizJuego[i][columna] == valor:
                return False
        
        # Verificar subcuadro 3x3
        sub_fila = (fila // 3) * 3
        sub_columna = (columna // 3) * 3
        for i in range(sub_fila, sub_fila + 3):
            for j in range(sub_columna, sub_columna + 3):
                if self.matrizJuego[i][j] == valor:
                    return False
        
        return True
    
    def juego_finalizado(self):
        """
        Verifica si el juego ha finalizado (todas las posiciones están llenas).
        """
        for fila in self.matrizJuego:
            if 0 in fila:
                return False
        return True