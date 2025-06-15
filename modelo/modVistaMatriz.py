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

    def procesar_entrada(self, fila, columna, valor_anterior, valor_nuevo):
        """
        Procesa una nueva entrada en el sudoku y actualiza las estructuras de datos
        Retorna: (exito, mensaje, key)
        """
        if valor_anterior == valor_nuevo:
            return False, "No hay cambio", None  # No hay cambio real, ignoramos

        # Si el nuevo valor no es 0, verificar si la jugada es válida
        if valor_nuevo != 0:
            if not self.matriz.jugada_valida(fila, columna, valor_nuevo):
                return False, "Jugada inválida", None

        # Crear un nuevo Key con la información
        key = Key(fila, columna, valor_anterior, valor_nuevo)
        key.set_tipo("ingreso")

        # Actualizar la matriz de juego con el nuevo valor
        self.matrizJuego[fila][columna] = valor_nuevo

        # Crear nodo y agregar a la lista de jugadas
        nodo_jugadas = Nodo(key)
        self.jugadas.insert(nodo_jugadas)

        # Crear nodo y agregar a la lista de deshacer
        nodo_deshacer = Nodo(key)
        self.deshacer.insert(nodo_deshacer)

        # Limpiar la lista de rehacer ya que se ha hecho una nueva jugada
        self.rehacer.delete_todos_nodos()

        # Verificar si el juego está completo
        if self.matriz.juego_finalizado():
            return True, "¡Felicidades! Has completado el Sudoku", key
        
        return True, "Jugada válida", key