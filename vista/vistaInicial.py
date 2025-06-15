import tkinter as tk
from tkinter import filedialog, messagebox
from controlador.ctlVistaInicial import CtlVistaInicial

class VistaInicial:
    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades):
        self.root = tk.Tk()
        self.root.title("Sudoku - Cargar Juego")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Crear el controlador
        self.controlador = CtlVistaInicial(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades)

        # Título
        self.lblTitulo = tk.Label(self.root, text="SUDOKU", font=("Tahoma", 36, "bold"), fg="#464646")
        self.lblTitulo.pack(pady=30)

        # Botón para seleccionar archivo
        self.btnSeleccionarArchivo = tk.Button(self.root, text="Seleccionar Archivo TXT", 
                                             command=self.controlador.seleccionar_archivo, 
                                             font=("Tahoma", 14, "bold"), fg="red")
        self.btnSeleccionarArchivo.pack(pady=10)

        # Etiqueta para mostrar el archivo seleccionado
        self.lblArchivoSeleccionado = tk.Label(self.root, text="No se ha seleccionado ningún archivo", 
                                              font=("Tahoma", 12))
        self.lblArchivoSeleccionado.pack(pady=10)

        # Botón para confirmar
        self.btnConfirmar = tk.Button(self.root, text="Comenzar Juego", 
                                    command=self.controlador.confirmar_seleccion, 
                                    font=("Tahoma", 14, "bold"), fg="red")
        self.btnConfirmar.pack(pady=10)

    def set_archivo_seleccionado(self, nombre_archivo):
        self.lblArchivoSeleccionado.config(text=nombre_archivo)

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def iniciar(self):
        self.root.mainloop()