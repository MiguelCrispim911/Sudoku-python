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

    def agregar_posibilidades_por_valor(self, fila_origen, col_origen, valor, matriz):
        """
        Agrega un valor específico a las posibilidades de todas las posiciones en la misma fila, 
        columna y cuadrícula 3x3 que la posición origen, pero solo si esas celdas están vacías
        y no tienen conflictos con ese valor.
        
        Args:
            fila_origen: fila de la casilla de referencia
            col_origen: columna de la casilla de referencia  
            valor: valor a agregar a las posibilidades
            matriz: referencia a la matriz para verificar celdas vacías
        """
        # Agregar a la misma fila
        for col in range(9):
            if col != col_origen and matriz.get_valor(fila_origen, col) == 0:  # Solo celdas vacías
                if self._puede_tener_valor_diccionario(fila_origen, col, valor, matriz):
                    posibilidades_actuales = self.get_posibilidades(fila_origen, col)
                    posibilidades_actuales.add(valor)
                    self.set_posibilidades(fila_origen, col, posibilidades_actuales)
        
        # Agregar a la misma columna
        for fila in range(9):
            if fila != fila_origen and matriz.get_valor(fila, col_origen) == 0:  # Solo celdas vacías
                if self._puede_tener_valor_diccionario(fila, col_origen, valor, matriz):
                    posibilidades_actuales = self.get_posibilidades(fila, col_origen)
                    posibilidades_actuales.add(valor)
                    self.set_posibilidades(fila, col_origen, posibilidades_actuales)
        
        # Agregar al mismo cuadrado 3x3
        cuadrado_fila = (fila_origen // 3) * 3
        cuadrado_col = (col_origen // 3) * 3
        
        for fila in range(cuadrado_fila, cuadrado_fila + 3):
            for col in range(cuadrado_col, cuadrado_col + 3):
                if (fila != fila_origen or col != col_origen) and matriz.get_valor(fila, col) == 0:  # Solo celdas vacías
                    if self._puede_tener_valor_diccionario(fila, col, valor, matriz):
                        posibilidades_actuales = self.get_posibilidades(fila, col)
                        posibilidades_actuales.add(valor)
                        self.set_posibilidades(fila, col, posibilidades_actuales)

    def _puede_tener_valor_diccionario(self, fila, col, valor, matriz):
        """
        Verifica si una celda puede tener un valor específico sin crear conflictos.
        """
        # Verificar fila
        for c in range(9):
            if c != col and matriz.get_valor(fila, c) == valor:
                return False
        
        # Verificar columna
        for f in range(9):
            if f != fila and matriz.get_valor(f, col) == valor:
                return False
        
        # Verificar cuadrícula 3x3
        cuadrado_fila = (fila // 3) * 3
        cuadrado_col = (col // 3) * 3
        
        for f in range(cuadrado_fila, cuadrado_fila + 3):
            for c in range(cuadrado_col, cuadrado_col + 3):
                if (f != fila or c != col) and matriz.get_valor(f, c) == valor:
                    return False
        
        return True