from estructuras.Key import Key
from estructuras.Nodo import Nodo
from estructuras.Matriz import Matriz

class ModVistaMatriz:
    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.matrizJuego = matrizJuego
        self.deshacer = deshacer
        self.rehacer = rehacer
        self.jugadas = jugadas
        self.posibilidades = posibilidades
        self.matriz = Matriz(matrizJuego)  # Instancia de la clase Matriz

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