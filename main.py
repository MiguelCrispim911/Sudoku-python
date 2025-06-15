from vista.vistaInicial import VistaInicial
from estructuras.Lista import Lista
from estructuras.Pila import Pila

if __name__ == "__main__":
    # Inicialización de estructuras
    # Matriz del juego (9x9)
    matrizJuego = [[0 for _ in range(9)] for _ in range(9)]

    # Lista doblemente enlazada para deshacer
    deshacer = Lista()

    # Lista doblemente enlazada para jugadas
    jugadas = Lista()

    # Pila para rehacer (tamaño máximo 81 - número total de celdas en el Sudoku)
    rehacer = Pila(81)

    # Iniciar la vista inicial
    vista = VistaInicial(matrizJuego, deshacer, rehacer, jugadas)
    vista.iniciar()