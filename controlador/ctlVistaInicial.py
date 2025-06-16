import os
from tkinter import messagebox, filedialog
from modelo.modVistaInicial import ModVistaInicial
from vista.vistaMatriz import VistaMatriz

class CtlVistaInicial:
    def __init__(self, vista, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.vista = vista
        self.modelo = ModVistaInicial(matrizJuego, deshacer, rehacer, jugadas, posibilidades)
        self.archivo_seleccionado = None

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
        if archivo:
            valido, mensaje = self.modelo.validar_archivo_txt(archivo)
            if valido:
                self.archivo_seleccionado = archivo
                self.vista.set_archivo_seleccionado(os.path.basename(archivo))
            else:
                messagebox.showerror("Error", mensaje)

    def confirmar_seleccion(self):
        if self.archivo_seleccionado:
            self.modelo.llenar_matriz(self.archivo_seleccionado)
            self.modelo.diccionario.inicializar_posibilidades_desde_tablero(self.modelo.matrizJuego)
            self.vista.root.destroy()
            # Crear la vista matriz
            VistaMatriz(self.modelo.matrizJuego, self.modelo.deshacer, 
                       self.modelo.rehacer, self.modelo.jugadas, 
                       self.modelo.posibilidades)
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo primero.")