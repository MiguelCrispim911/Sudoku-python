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
        # Primero verificar que no haya celdas vacías
        for fila in self.matrizJuego:
            if 0 in fila:
                return False
        
        # Verificar filas - cada fila debe tener exactamente los números 1-9
        for fila in range(9):
            numeros_en_fila = set(self.matrizJuego[fila])
            if numeros_en_fila != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return False
        
        # Verificar columnas - cada columna debe tener exactamente los números 1-9
        for columna in range(9):
            numeros_en_columna = set()
            for fila in range(9):
                numeros_en_columna.add(self.matrizJuego[fila][columna])
            if numeros_en_columna != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return False
        
        # Verificar subcuadros 3x3 - cada subcuadro debe tener exactamente los números 1-9
        for sub_fila_inicio in range(0, 9, 3):
            for sub_columna_inicio in range(0, 9, 3):
                numeros_en_subcuadro = set()
                for fila in range(sub_fila_inicio, sub_fila_inicio + 3):
                    for columna in range(sub_columna_inicio, sub_columna_inicio + 3):
                        numeros_en_subcuadro.add(self.matrizJuego[fila][columna])
                if numeros_en_subcuadro != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                    return False
        
        # Si pasa todas las verificaciones, el juego está correctamente finalizado
        return True