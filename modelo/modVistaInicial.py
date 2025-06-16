import os
from estructuras.Diccionario import Diccionario  # AGREGAR ESTA LÍNEA

class ModVistaInicial:

    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.matrizJuego = matrizJuego
        self.deshacer = deshacer
        self.rehacer = rehacer
        self.jugadas = jugadas
        self.posibilidades = posibilidades
        
        # AGREGAR ESTA LÍNEA:
        self.diccionario = Diccionario(posibilidades)

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