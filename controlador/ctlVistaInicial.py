import os
from tkinter import messagebox, filedialog
from modelo.modVistaInicial import ModVistaInicial

class CtlVistaInicial:
    def __init__(self, vista, matrizJuego, deshacer, rehacer, jugadas):
        self.vista = vista
        self.modelo = ModVistaInicial(matrizJuego, deshacer, rehacer, jugadas)
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
            self.modelo.borrar_posibilidades_posiciones_llenas()  # Llamar a la nueva función
            self.vista.mostrar_mensaje("Éxito", "Archivo cargado correctamente.")
            self.vista.root.destroy()
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo primero.")