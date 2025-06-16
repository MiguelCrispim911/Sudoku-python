from estructuras.Key import Key
from estructuras.Nodo import Nodo
from estructuras.Matriz import Matriz
from estructuras.Diccionario import Diccionario  # Importar la clase Diccionario

class ModVistaMatriz:
    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.matrizJuego = matrizJuego
        self.deshacer = deshacer
        self.rehacer = rehacer
        self.jugadas = jugadas
        self.posibilidades = posibilidades
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
        
        # Actualizar posibilidades si se agregó un valor
        if key.get_valor_nuevo() != 0:
            fila = key.get_linea()
            columna = key.get_columna()
            valor = key.get_valor_nuevo()
            
            # Limpiar posibilidades de la celda ocupada
            self.diccionario.set_posibilidades(fila, columna, set())
            # Eliminar el valor de las posibilidades relacionadas
            self.diccionario.eliminar_posibilidades_por_valor(fila, columna, valor)
    
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