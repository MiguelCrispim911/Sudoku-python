from vista.vistaInicial import VistaInicial
from estructuras.Lista import Lista


if __name__ == "__main__":
    # Inicialización de estructuras
    # Matriz del juego (9x9)
    matrizJuego = [[0 for _ in range(9)] for _ in range(9)]

    # Lista doblemente enlazada para deshacer
    deshacer = Lista()

    # Lista doblemente enlazada para jugadas
    jugadas = Lista()

    # Pila para rehacer (tamaño máximo 2000 jugadas)
    rehacer = Lista()

    #Diccionario Python para las posibilidades de cada celda
    posibilidades = {
        (fila, col): {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for fila in range(9)
        for col in range(9)
    }

    #Diccionario Python para las posibilidades de cada celda
    noVolverASugerir = {
        (fila, col): set() 
        for fila in range(9)
        for col in range(9)
    }


    # Iniciar la vista inicial
    vista = VistaInicial(matrizJuego, deshacer, rehacer, jugadas, posibilidades, noVolverASugerir)
    vista.iniciar()