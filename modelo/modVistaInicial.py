import os

class ModVistaInicial:

    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.matrizJuego = matrizJuego
        self.deshacer = deshacer
        self.rehacer = rehacer
        self.jugadas = jugadas
        self.posibilidades = posibilidades

    def validar_archivo_txt(self, archivo):
        if not os.path.isfile(archivo):
            return False, "El archivo no existe."

        with open(archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        if len(lineas) != 9:
            return False, "El archivo debe contener exactamente 9 líneas."

        for linea in lineas:
            if len(linea.strip()) != 9 or not all(c in "123456789-" for c in linea.strip()):
                return False, "Cada línea debe tener 9 caracteres (1-9 o -)."

        return True, "Archivo válido."

    def llenar_matriz(self, archivo):
        """
        Llena matrizJuego con los datos del archivo.
        """
        with open(archivo, "r", encoding="utf-8") as f:
            for fila, linea in enumerate(f):
                for col, caracter in enumerate(linea.strip()):
                    if caracter == "-":
                        self.matrizJuego[fila][col] = 0
                    else:
                        self.matrizJuego[fila][col] = int(caracter)
    
    def borrar_posibilidades_posiciones_llenas(self):
        """
        Borra sugestiones para posiciones que estaran bloqueadas!!!
        """
        for i in range(9):
            for j in range(9):
                if self.matrizJuego[i][j] != 0:  
                    if (i, j) in self.posibilidades:
                        del self.posibilidades[(i, j)]  # Eliminar la entrada del diccionario

