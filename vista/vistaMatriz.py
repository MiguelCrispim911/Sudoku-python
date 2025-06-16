import tkinter as tk
from tkinter import ttk, messagebox
from modelo.modVistaMatriz import ModVistaMatriz
from controlador.ctlVistaMatriz import CtlVistaMatriz

class VistaMatriz:
    def __init__(self, matrizJuego, deshacer, rehacer, jugadas, posibilidades,noVolverASugerir):
        self.matrizJuego = matrizJuego
        self.noVolverASugerir = noVolverASugerir
        # Crear el modelo internamente
        self.modelo = ModVistaMatriz(matrizJuego, deshacer, rehacer, jugadas, posibilidades, noVolverASugerir)
        
        # Variable para mantener la celda seleccionada actual
        self.celda_seleccionada = None
        self.celda_seleccionada_pos = None  # (fila, columna)
        
        self.root = tk.Tk()
        self.root.title("Sudoku - Juego")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # Frame principal que contendrá todo
        self.frame_principal = tk.Frame(self.root, bg='#f0f0f0')
        self.frame_principal.pack(expand=True, fill='both', padx=15, pady=15)

        # Frame para el grid del Sudoku (izquierda, más grande)
        self.frame_sudoku = tk.Frame(self.frame_principal, bg='#f0f0f0', width=900)
        self.frame_sudoku.pack(side=tk.LEFT, padx=15)

        # Frame para controles y listados (derecha, más estrecho)
        self.frame_derecho = tk.Frame(self.frame_principal, bg='#f0f0f0', width=250)
        self.frame_derecho.pack(side=tk.LEFT, fill='both', expand=True, padx=15)

        # Crear el grid del Sudoku
        self.celdas = {}
        self.crear_grid_sudoku()

        # Frame para los botones de control
        self.crear_controles()

        # Frame para los listados
        self.crear_listados()

        # Inicializar valores y bloquear celdas necesarias
        self.inicializar_celdas()
        
        # Crear el controlador después de tener todo configurado
        self.controlador = CtlVistaMatriz(self, self.modelo)

        # Conectar los botones
        self.conectar_botones()
        
        # Inicializar posibilidades después de que todo esté creado
        self.root.after_idle(self.inicializar_posibilidades_vista)

    def inicializar_posibilidades_vista(self):
        """Inicializa las posibilidades en la vista al comenzar el juego"""
        posibilidades = self.modelo.obtener_posibilidades_formateadas()
        
        # Limpiar el listbox de posibilidades
        self.listbox_posibilidades.delete(0, tk.END)
        
        # Agregar cada posibilidad al listbox
        for posibilidad in posibilidades:
            self.listbox_posibilidades.insert(tk.END, posibilidad)
        
        # Inicializar  noVolverASugerir
        self.actualizar_no_volver_a_sugerir()

    def conectar_botones(self):
        """Conecta los botones con sus funciones del controlador"""
        self.btn_deshacer.config(command=self.controlador.deshacer_jugada)
        self.btn_rehacer.config(command=self.controlador.rehacer_jugada)

    def validar_entrada(self, valor_completo):
        """Valida que solo se ingresen números del 1-9 (un solo dígito) o esté vacío"""
        # Solo permite: vacío, o un solo dígito del 1 al 9
        if valor_completo == '':
            return True
        if len(valor_completo) == 1 and valor_completo in '123456789':
            return True
        return False

    def crear_grid_sudoku(self):
        # Registrar la función de validación
        vcmd = (self.root.register(self.validar_entrada), '%P')
        
        # Crear marco exterior para el Sudoku
        marco_sudoku = tk.Frame(self.frame_sudoku, bg='black', bd=2)  # Borde más delgado
        marco_sudoku.pack(expand=True, padx=5, pady=5)  # Menos padding exterior
        
        for bloque_i in range(3):
            for bloque_j in range(3):
                frame_bloque = tk.Frame(marco_sudoku, bg='black', pady=1, padx=1)  # Padding reducido
                frame_bloque.grid(row=bloque_i, column=bloque_j, padx=2, pady=2)  # Espaciado reducido

                for i in range(3):
                    for j in range(3):
                        fila = bloque_i * 3 + i
                        columna = bloque_j * 3 + j

                        frame_celda = tk.Frame(frame_bloque, bg='black')
                        frame_celda.grid(row=i, column=j, padx=2, pady=2)  # Espaciado reducido                        # Usar Entry en lugar de Combobox para control total de colores
                        celda = tk.Entry(frame_celda,
                                       width=2,
                                       justify='center',
                                       font=('Arial Black', 24, 'bold'),  # Fuente más pequeña
                                       bg='#87CEEB',  # Fondo azul para celdas editables
                                       fg='#000000',  # Texto negro para números del usuario
                                       relief='solid',
                                       bd=2,
                                       validate='key',
                                       validatecommand=vcmd,
                                       highlightthickness=2,
                                       highlightcolor='#FF6600',  # Naranja al hacer focus
                                       highlightbackground='#CCCCCC')
                        celda.pack(padx=3, pady=3)  # Padding más pequeño
                        
                        # Agregar eventos de focus y click
                        celda.bind('<FocusIn>', lambda e, f=fila, c=columna: self.on_celda_focus(e, f, c))
                        celda.bind('<Button-1>', lambda e, f=fila, c=columna: self.on_celda_focus(e, f, c))
                        celda.bind('<FocusOut>', self.on_celda_focus_out)
                        
                        self.celdas[(fila, columna)] = celda

    def crear_controles(self):
        frame_controles = tk.Frame(self.frame_derecho, bg='#f0f0f0')
        frame_controles.pack(fill='x', pady=(0, 5))

        button_style = {'font': ('Arial', 12),
                       'width': 8,
                       'height': 1,
                       'bg': '#0078D7',
                       'fg': 'white',
                       'relief': 'raised',
                       'bd': 2}

        self.btn_deshacer = tk.Button(frame_controles, 
                                    text="Deshacer", 
                                    **button_style)
        self.btn_deshacer.pack(side=tk.LEFT, padx=5)
        
        self.btn_rehacer = tk.Button(frame_controles, 
                                   text="Rehacer", 
                                   **button_style)
        self.btn_rehacer.pack(side=tk.LEFT, padx=5)
        
        # Botón de sugerencia con estilo diferente
        suggestion_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 10,
            'height': 1,
            'bg': '#28A745',  # Verde
            'fg': 'white',
            'relief': 'raised',
            'state': 'disabled',  # Inicialmente deshabilitado
            'bd': 2
        }
        
        self.btn_sugerencia = tk.Button(frame_controles, 
                                      text="Sugerencia", 
                                      **suggestion_style)
        self.btn_sugerencia.config(state='disabled')  # Asegurar que está deshabilitado
        self.btn_sugerencia.pack(side=tk.LEFT, padx=5)

    def crear_listados(self):
        frame_todos_listados = tk.Frame(self.frame_derecho, bg='#f0f0f0')
        frame_todos_listados.pack(fill='both', expand=True)

        # MODIFICAR: Agregar "NoVolverASugerir" a la lista
        listados = ["Jugadas", "Deshacer", "Rehacer", "Posibilidades", "NoVolverASugerir"]
        
        for titulo in listados:
            frame = tk.LabelFrame(frame_todos_listados, 
                                text=titulo,
                                bg='#f0f0f0',
                                font=('Arial', 8, 'bold'))
            frame.pack(fill='both', expand=True, pady=0)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(frame,
                            font=('Courier', 7),
                            bg='white',
                            selectmode='browse',
                            relief='sunken',
                            bd=1,
                            height=1,
                            yscrollcommand=scrollbar.set)
            listbox.pack(fill='both', expand=True, padx=1, pady=0)

            scrollbar.config(command=listbox.yview)
            # MODIFICAR: Manejar el nombre especial
            nombre_atributo = titulo.lower().replace("novolverasugerir", "no_volver_a_sugerir")
            setattr(self, f"listbox_{nombre_atributo}", listbox)

    def bloquear_celda(self, fila, columna):
        """Bloquea una celda y usa el color por defecto del sistema con texto negro"""
        celda = self.celdas[(fila, columna)]
        celda.config(state="readonly",
                    bg='SystemButtonFace',  # Color por defecto del sistema
                    fg='#000000',  # Texto negro
                    relief='sunken',  # Estilo hundido para diferenciarlo
                    bd=1,
                    highlightthickness=0)  # Sin highlight cuando está bloqueada

    def inicializar_celdas(self):
        """Inicializa los valores y bloquea las celdas que vienen con valor inicial"""
        for i in range(9):
            for j in range(9):
                valor = self.matrizJuego[i][j]
                if valor != 0:
                    celda = self.celdas[(i, j)]
                    celda.insert(0, str(valor))  # Insertar el valor
                    self.bloquear_celda(i, j)

    def obtener_valor(self, fila, columna):
        """Obtiene el valor de una celda"""
        valor = self.celdas[(fila, columna)].get().strip()
        return int(valor) if valor.isdigit() else 0

    def establecer_valor(self, fila, columna, valor):
        """Establece el valor de una celda si no está bloqueada"""
        celda = self.celdas[(fila, columna)]
        if celda['state'] != 'readonly':
            celda.delete(0, tk.END)
            if valor != 0:
                celda.insert(0, str(valor))

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def actualizar_listados(self, key):
        """Actualiza los listboxes con la nueva jugada"""
        if key:
            # Formatear el texto de la jugada (L en lugar de F)
            texto = f"L{key.get_linea() + 1} C{key.get_columna() + 1} {key.get_valor_anterior()}->{key.get_valor_nuevo()} ({key.get_tipo()})"
            
            # Insertar al inicio de la lista de jugadas
            self.listbox_jugadas.insert(0, texto)
            
            # Insertar al inicio de la lista de deshacer
            self.listbox_deshacer.insert(0, texto)
            
            # Limpiar la lista de rehacer ya que se hizo una nueva jugada
            self.listbox_rehacer.delete(0, tk.END)
            
            # Actualizar posibilidades
            self.actualizar_posibilidades()

    def actualizar_listados_deshacer_rehacer(self):
        """Actualiza los listados de deshacer y rehacer después de operaciones"""
        # Limpiar los listboxes
        self.listbox_deshacer.delete(0, tk.END)
        self.listbox_rehacer.delete(0, tk.END)
        
        # Actualizar listbox de deshacer
        nodo = self.modelo.deshacer.get_head()
        while nodo is not None:
            key = nodo.get_key()
            texto = f"L{key.get_linea() + 1} C{key.get_columna() + 1} {key.get_valor_anterior()}->{key.get_valor_nuevo()} ({key.get_tipo()})"
            self.listbox_deshacer.insert(tk.END, texto)
            nodo = nodo.get_next()
        
        # Actualizar listbox de rehacer
        nodo = self.modelo.rehacer.get_head()
        while nodo is not None:
            key = nodo.get_key()
            texto = f"L{key.get_linea() + 1} C{key.get_columna() + 1} {key.get_valor_anterior()}->{key.get_valor_nuevo()} ({key.get_tipo()})"
            self.listbox_rehacer.insert(tk.END, texto)
            nodo = nodo.get_next()

    def on_celda_focus(self, event, fila, columna):
        """Maneja el evento cuando una celda recibe el focus"""
        celda = event.widget
        # Primero desactivar el botón
        self.btn_sugerencia.config(state='disabled')
        # Solo activar si la celda no está bloqueada
        if celda['state'] != 'readonly':
            self.celda_seleccionada = celda
            self.celda_seleccionada_pos = (fila, columna)
            self.btn_sugerencia.config(state='normal')
        else:
            self.celda_seleccionada = None
            self.celda_seleccionada_pos = None

    def on_celda_focus_out(self, event):
        """Maneja el evento cuando una celda pierde el focus"""
        self.celda_seleccionada = None
        self.celda_seleccionada_pos = None
        self.btn_sugerencia.config(state='disabled')
    
    def actualizar_posibilidades(self):
        """Actualiza el listbox de posibilidades y noVolverASugerir"""
        posibilidades = self.modelo.obtener_posibilidades_formateadas()
        
        # Limpiar el listbox de posibilidades  
        self.listbox_posibilidades.delete(0, tk.END)
        
        # Agregar cada posibilidad al listbox
        for posibilidad in posibilidades:
            self.listbox_posibilidades.insert(tk.END, posibilidad)
        
        # NUEVO: También actualizar noVolverASugerir
        self.actualizar_no_volver_a_sugerir()

    def actualizar_no_volver_a_sugerir(self):
        """Actualiza el listbox de noVolverASugerir"""
        no_sugerir_texto = self.modelo.obtener_no_volver_a_sugerir_formateadas()
        
        # Limpiar el listbox
        self.listbox_no_volver_a_sugerir.delete(0, tk.END)
        
        # Agregar cada entrada al listbox
        for entrada in no_sugerir_texto:
            self.listbox_no_volver_a_sugerir.insert(tk.END, entrada)

    def iniciar(self):
        self.root.mainloop()