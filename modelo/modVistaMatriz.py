import random
from estructuras.Key import Key
from estructuras.Nodo import Nodo
from estructuras.Matriz import Matriz
from estructuras.Diccionario import Diccionario  # Importar la clase Diccionario

class ModVistaMatriz:
    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades,noVolverASugerir):
        self.matrizJuego = matrizJuego
        self.deshacer = deshacer
        self.rehacer = rehacer
        self.jugadas = jugadas
        self.posibilidades = posibilidades
        self.noVolverASugerir = noVolverASugerir 
        self.matriz = Matriz(matrizJuego)  # Instancia de la clase Matriz
        
        # Crear instancia del diccionario de posibilidades
        self.diccionario = Diccionario(posibilidades)
        # Inicializar posibilidades basadas en el tablero inicial
        self.diccionario.inicializar_posibilidades_desde_tablero(matrizJuego)

    def get_valor(self, fila, columna):
        """Obtiene el valor en la posición especificada"""
        return self.matriz.get_valor(fila, columna)
    
    def set_valor(self, fila, columna, valor):
        """Establece el valor en la posición especificada"""
        self.matriz.set_valor(fila, columna, valor)
    
    def es_jugada_valida(self, fila, columna, valor):
        """Verifica si una jugada es válida"""
        if valor == 0:  # Borrar siempre es válido
            return True
        return self.matriz.jugada_valida(fila, columna, valor)
    
    def esta_juego_completo(self):
        """Verifica si el juego está completo"""
        return self.matriz.juego_finalizado()
    
    def agregar_jugada(self, key):
        """Agrega una jugada a las listas correspondientes"""
        # Agregar a jugadas
        nodo_jugadas = Nodo(key)
        self.jugadas.insert(nodo_jugadas)
        
        # Agregar a deshacer
        nodo_deshacer = Nodo(key)
        self.deshacer.insert(nodo_deshacer)
        
        # Limpiar rehacer cuando se hace una nueva jugada
        self.rehacer.delete_todos_nodos()
        
        fila = key.get_linea()
        columna = key.get_columna()
        valor_anterior = key.get_valor_anterior()
        valor_nuevo = key.get_valor_nuevo()
        
        # Actualizar posibilidades según el tipo de jugada
        if valor_nuevo != 0:
            # Se agregó un valor: limpiar posibilidades de la celda y eliminar de relacionadas
            self.diccionario.set_posibilidades(fila, columna, set())
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor_nuevo)
        elif valor_anterior != 0:
            # Se borró un valor: restaurar posibilidades en la celda y en relacionadas
            # Restaurar posibilidades para la celda que se vacía
            posibilidades_celda = set()
            for num in range(1, 10):
                if self._puede_tener_valor(fila, columna, num):
                    posibilidades_celda.add(num)
            self.diccionario.set_posibilidades(fila, columna, posibilidades_celda)
            
            # Restaurar el valor borrado como posibilidad en celdas relacionadas
            self.agregar_posibilidades_por_valor(fila, columna, valor_anterior)
    
    def obtener_ultima_jugada_deshacer(self):
        """Obtiene la última jugada que puede deshacerse"""
        return self.deshacer.get_head()
    
    def obtener_ultima_jugada_rehacer(self):
        """Obtiene la última jugada que puede rehacerse"""
        return self.rehacer.get_head()
    
    def mover_deshacer_a_rehacer(self, nodo):
        """Mueve un nodo de deshacer a rehacer"""
        self.deshacer.delete_nodo(nodo)
        self.rehacer.insert(nodo)
    
    def mover_rehacer_a_deshacer(self, nodo):
        """Mueve un nodo de rehacer a deshacer"""
        self.rehacer.delete_nodo(nodo)
        self.deshacer.insert(nodo)
    
    def crear_key(self, fila, columna, valor_anterior, valor_nuevo, tipo="ingreso"):
        """Crea un objeto Key con los datos proporcionados"""
        key = Key(fila, columna, valor_anterior, valor_nuevo)
        key.set_tipo(tipo)
        return key
    
    def obtener_posibilidades_formateadas(self):
        """
        Obtiene las posibilidades formateadas para mostrar en la vista
        """
        posibilidades_texto = []
        
        for fila in range(9):
            for col in range(9):
                posibilidades_celda = self.diccionario.get_posibilidades(fila, col)
                if posibilidades_celda:  # Solo mostrar si hay posibilidades
                    # Convertir set a lista ordenada
                    valores = sorted(list(posibilidades_celda))
                    valores_str = ','.join(map(str, valores))
                    texto = f"L{fila+1}C{col+1}: {valores_str}"
                    posibilidades_texto.append(texto)
        
        return posibilidades_texto

    def agregar_posibilidades_por_valor(self, fila_origen, col_origen, valor):
        """
        Agrega un valor específico a las posibilidades de todas las posiciones en la misma fila, 
        columna y cuadrícula 3x3 que la posición origen, pero solo si esas celdas están vacías
        y no tienen conflictos con ese valor.
        
        Args:
            fila_origen: fila de la casilla de referencia
            col_origen: columna de la casilla de referencia  
            valor: valor a agregar a las posibilidades
        """
        # Agregar a la misma fila
        for col in range(9):
            if col != col_origen and self.matriz.get_valor(fila_origen, col) == 0:  # Solo celdas vacías
                if self._puede_tener_valor(fila_origen, col, valor):
                    posibilidades_actuales = self.diccionario.get_posibilidades(fila_origen, col)
                    posibilidades_actuales.add(valor)
                    self.diccionario.set_posibilidades(fila_origen, col, posibilidades_actuales)
        
        # Agregar a la misma columna
        for fila in range(9):
            if fila != fila_origen and self.matriz.get_valor(fila, col_origen) == 0:  # Solo celdas vacías
                if self._puede_tener_valor(fila, col_origen, valor):
                    posibilidades_actuales = self.diccionario.get_posibilidades(fila, col_origen)
                    posibilidades_actuales.add(valor)
                    self.diccionario.set_posibilidades(fila, col_origen, posibilidades_actuales)
        
        # Agregar al mismo cuadrado 3x3
        cuadrado_fila = (fila_origen // 3) * 3
        cuadrado_col = (col_origen // 3) * 3
        
        for fila in range(cuadrado_fila, cuadrado_fila + 3):
            for col in range(cuadrado_col, cuadrado_col + 3):
                if (fila != fila_origen or col != col_origen) and self.matriz.get_valor(fila, col) == 0:  # Solo celdas vacías
                    if self._puede_tener_valor(fila, col, valor):
                        posibilidades_actuales = self.diccionario.get_posibilidades(fila, col)
                        posibilidades_actuales.add(valor)
                        self.diccionario.set_posibilidades(fila, col, posibilidades_actuales)

    def _puede_tener_valor(self, fila, col, valor):
        """
        Verifica si una celda puede tener un valor específico sin crear conflictos.
        
        Args:
            fila: fila de la celda
            col: columna de la celda
            valor: valor a verificar
        
        Returns:
            bool: True si la celda puede tener ese valor, False en caso contrario
        """
        # Verificar fila
        for c in range(9):
            if c != col and self.matriz.get_valor(fila, c) == valor:
                return False
        
        # Verificar columna
        for f in range(9):
            if f != fila and self.matriz.get_valor(f, col) == valor:
                return False
        
        # Verificar cuadrícula 3x3
        cuadrado_fila = (fila // 3) * 3
        cuadrado_col = (col // 3) * 3
        
        for f in range(cuadrado_fila, cuadrado_fila + 3):
            for c in range(cuadrado_col, cuadrado_col + 3):
                if (f != fila or c != col) and self.matriz.get_valor(f, c) == valor:
                    return False
        
        return True

    def actualizar_posibilidades_deshacer(self, fila, columna, valor_anterior, valor_nuevo):
        """
        Actualiza las posibilidades cuando se deshace una jugada.
        
        Args:
            fila: fila de la jugada
            columna: columna de la jugada
            valor_anterior: valor que tenía antes (al que se regresa)
            valor_nuevo: valor que tenía después (el que se quita)
        """
        if valor_anterior == 0 and valor_nuevo != 0:
            # Se está quitando un número (valor_nuevo) y dejando la celda vacía
            # Restaurar posibilidades para la celda que se vacía
            posibilidades_celda = set()
            for num in range(1, 10):
                if self._puede_tener_valor(fila, columna, num):
                    posibilidades_celda.add(num)
            self.diccionario.set_posibilidades(fila, columna, posibilidades_celda)
            
            # Restaurar el valor_nuevo como posibilidad en celdas relacionadas
            self.agregar_posibilidades_por_valor(fila, columna, valor_nuevo)
            
        elif valor_anterior != 0 and valor_nuevo == 0:
            # Se está poniendo un número (valor_anterior) en una celda vacía
            # Limpiar posibilidades de la celda ocupada
            self.diccionario.set_posibilidades(fila, columna, set())
            # Eliminar el valor de las posibilidades relacionadas
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor_anterior)
            
        elif valor_anterior != 0 and valor_nuevo != 0:
            # Se está cambiando un número por otro
            # Limpiar posibilidades de la celda (sigue ocupada)
            self.diccionario.set_posibilidades(fila, columna, set())
            # Restaurar valor_nuevo como posibilidad en celdas relacionadas
            self.agregar_posibilidades_por_valor(fila, columna, valor_nuevo)
            # Eliminar valor_anterior de las posibilidades relacionadas
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor_anterior)

    def actualizar_posibilidades_rehacer(self, fila, columna, valor_anterior, valor_nuevo):
        """
        Actualiza las posibilidades cuando se rehace una jugada.
        
        Args:
            fila: fila de la jugada
            columna: columna de la jugada
            valor_anterior: valor que tenía antes (el que se quita)
            valor_nuevo: valor que tendrá después (al que se cambia)
        """
        if valor_anterior == 0 and valor_nuevo != 0:
            # Se está poniendo un número (valor_nuevo) en una celda vacía
            # Limpiar posibilidades de la celda ocupada
            self.diccionario.set_posibilidades(fila, columna, set())
            # Eliminar el valor de las posibilidades relacionadas
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor_nuevo)
            
        elif valor_anterior != 0 and valor_nuevo == 0:
            # Se está quitando un número (valor_anterior) y dejando la celda vacía
            # Restaurar posibilidades para la celda que se vacía
            posibilidades_celda = set()
            for num in range(1, 10):
                if self._puede_tener_valor(fila, columna, num):
                    posibilidades_celda.add(num)
            self.diccionario.set_posibilidades(fila, columna, posibilidades_celda)
            
            # Restaurar el valor_anterior como posibilidad en celdas relacionadas
            self.agregar_posibilidades_por_valor(fila, columna, valor_anterior)
            
        elif valor_anterior != 0 and valor_nuevo != 0:
            # Se está cambiando un número por otro
            # Limpiar posibilidades de la celda (sigue ocupada)
            self.diccionario.set_posibilidades(fila, columna, set())
            # Restaurar valor_anterior como posibilidad en celdas relacionadas
            self.agregar_posibilidades_por_valor(fila, columna, valor_anterior)
            # Eliminar valor_nuevo de las posibilidades relacionadas
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor_nuevo)

    def obtener_no_volver_a_sugerir_formateadas(self):
        """
        Retorna una lista con las entradas de noVolverASugerir formateadas para mostrar en el listbox.
        Muestra todas las llaves del diccionario, incluso si tienen valores vacíos.
        """
        resultado = []
        
        # Iterar por todas las posiciones (0,0) hasta (8,8)
        for fila in range(9):
            for columna in range(9):
                llave = (fila, columna)
                
                # Obtener el set de valores para esta posición
                valores_set = self.noVolverASugerir.get(llave, set())
                
                # Formatear la entrada
                if valores_set:  # Si tiene valores
                    valores_str = ','.join(map(str, sorted(valores_set)))
                    texto = f"L{fila + 1} C{columna + 1}: [{valores_str}]"
                else:  # Si está vacío
                    texto = f"L{fila + 1} C{columna + 1}: []"
                
                resultado.append(texto)
        
        return resultado
    
    def obtener_sugerencia(self, fila, columna):
        """
        Obtiene una sugerencia aleatoria para la posición especificada.
        
        Args:
            fila: fila de la celda
            columna: columna de la celda
        
        Returns:
            dict: {'exito': bool, 'valor': int, 'mensaje': str}
        """
        import random
        
        # Verificar si la celda ya está ocupada
        if self.get_valor(fila, columna) != 0:
            return {
                'exito': False,
                'valor': None,
                'mensaje': 'La casilla ya está llena, no se puede dar sugerencia'
            }
        
        # Obtener posibilidades para esta posición
        posibilidades_celda = self.diccionario.get_posibilidades(fila, columna)
        
        # Obtener valores que no se deben volver a sugerir
        no_sugerir = self.noVolverASugerir.get((fila, columna), set())
        
        # Calcular sugerencias disponibles (posibilidades - no_sugerir)
        sugerencias_disponibles = posibilidades_celda - no_sugerir
        
        # Verificar si hay sugerencias disponibles
        if not sugerencias_disponibles:
            return {
                'exito': False,
                'valor': None,
                'mensaje': 'No hay sugerencias disponibles para esta posición'
            }
        
        # Seleccionar un valor aleatorio
        valor_sugerido = random.choice(list(sugerencias_disponibles))
        
        return {
            'exito': True,
            'valor': valor_sugerido,
            'mensaje': f'Sugerencia: {valor_sugerido}'
        }
    
    def agregar_a_no_volver_a_sugerir(self, fila, columna, valor):
        """
        Agrega un valor al conjunto de noVolverASugerir para la posición especificada.
        
        Args:
            fila: fila de la celda
            columna: columna de la celda
            valor: valor a agregar
        """
        if (fila, columna) not in self.noVolverASugerir:
            self.noVolverASugerir[(fila, columna)] = set()
        
        self.noVolverASugerir[(fila, columna)].add(valor)