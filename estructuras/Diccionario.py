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

    def eliminar_posibilidades_por_valor(self, fila_origen, col_origen, valor):
        """
        Elimina un valor específico de todas las posiciones en la misma fila, 
        columna y cuadrícula 3x3 que la posición origen.
        
        Args:
            fila_origen: fila de la casilla que contiene el valor
            col_origen: columna de la casilla que contiene el valor  
            valor: valor a eliminar de las posibilidades
        """
        # Eliminar de la misma fila
        for col in range(9):
            if col != col_origen:  # No eliminar de la casilla origen
                self.eliminar_posibilidad(fila_origen, col, valor)
        
        # Eliminar de la misma columna
        for fila in range(9):
            if fila != fila_origen:  # No eliminar de la casilla origen
                self.eliminar_posibilidad(fila, col_origen, valor)
        
        # Eliminar del mismo cuadrado 3x3
        cuadrado_fila = (fila_origen // 3) * 3
        cuadrado_col = (col_origen // 3) * 3
        
        for fila in range(cuadrado_fila, cuadrado_fila + 3):
            for col in range(cuadrado_col, cuadrado_col + 3):
                if fila != fila_origen or col != col_origen:  # No eliminar de la casilla origen
                    self.eliminar_posibilidad(fila, col, valor)

    def inicializar_posibilidades_desde_tablero(self, tablero):
        """
        Inicializa las posibilidades eliminando valores que ya están ocupados
        en el tablero inicial.
        
        Args:
            tablero: matriz 9x9 donde 0 representa casillas vacías y 1-9 valores ocupados
        """
        # Primero, limpiar las posibilidades de las casillas ocupadas
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] != 0:  # Casilla ocupada
                    self.set_posibilidades(fila, col, set())  # Sin posibilidades
        
        # Luego, eliminar posibilidades basadas en valores existentes
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] != 0:  # Casilla ocupada
                    valor = tablero[fila][col]
                    self.eliminar_posibilidades_por_valor(fila, col, valor)