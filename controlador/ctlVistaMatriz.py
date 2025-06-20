from estructuras.Key import Key
from estructuras.Nodo import Nodo

class CtlVistaMatriz:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.conectar_eventos()

    def conectar_eventos(self):
        """Conecta los eventos de las celdas con sus manejadores"""
        for (fila, columna), celda in self.vista.celdas.items():
            # Vincula el evento de cambio de valor - SOLO KeyRelease para cambios reales
            celda.bind('<KeyRelease>', lambda e, f=fila, c=columna: self.on_celda_change(e, f, c))
            # NO vinculamos FocusOut aquí para no interferir con la lógica de la Vista

    def on_celda_change(self, event, fila, columna):
        """Maneja el evento de cambio de valor en una celda"""
        if event.widget['state'] == 'readonly':
            return  # Ignorar celdas bloqueadas

        # Obtener valores
        valor_anterior = self.modelo.get_valor(fila, columna)
        nuevo_texto = event.widget.get().strip()
        valor_nuevo = int(nuevo_texto) if nuevo_texto.isdigit() else 0

        # Si no hubo cambio real, no hacer nada (sin mostrar mensaje)
        if valor_anterior == valor_nuevo:
            return

        # Procesar la entrada
        resultado = self.procesar_entrada(fila, columna, valor_anterior, valor_nuevo)
        
        if not resultado['exito']:
            # Revertir el cambio visual
            event.widget.delete(0, 'end')
            if valor_anterior != 0:
                event.widget.insert(0, str(valor_anterior))
            
            # Mostrar mensaje de error
            self.vista.mostrar_mensaje("Jugada Inválida", resultado['mensaje'])
            return
        
        # Si la jugada fue exitosa
        if resultado['key']:
            # Actualizar las visualizaciones de las listas
            self.vista.actualizar_listados(resultado['key'])
            
            # Si el juego está completo, mostrar mensaje
            if "completado" in resultado['mensaje'].lower():
                self.vista.mostrar_mensaje("¡Juego Completado!", resultado['mensaje'])

    def procesar_entrada(self, fila, columna, valor_anterior, valor_nuevo):
        """
        Procesa una nueva entrada en el sudoku y actualiza las estructuras de datos
        Retorna: diccionario con exito, mensaje, key
        """
        if valor_anterior == valor_nuevo:
            return {'exito': False, 'mensaje': "No hay cambio", 'key': None}

        # Verificar si la jugada es válida
        if not self.modelo.es_jugada_valida(fila, columna, valor_nuevo):
            return {'exito': False, 'mensaje': "Jugada inválida", 'key': None}

        # Crear el Key para la jugada
        key = self.modelo.crear_key(fila, columna, valor_anterior, valor_nuevo, "ingreso")

        # Actualizar el modelo
        self.modelo.set_valor(fila, columna, valor_nuevo)

        # Agregar la jugada a las listas
        self.modelo.agregar_jugada(key)

        # Verificar si el juego está completo
        if self.modelo.esta_juego_completo():
            return {'exito': True, 'mensaje': "¡Felicidades! Has completado el Sudoku", 'key': key}
        
        return {'exito': True, 'mensaje': "Jugada válida", 'key': key}

    def deshacer_jugada(self):
        """Deshace la última jugada"""
        ultimo_nodo = self.modelo.obtener_ultima_jugada_deshacer()
        
        if ultimo_nodo is None:
            self.vista.mostrar_mensaje("Deshacer", "No hay jugadas para deshacer")
            return
        
        # Obtener información de la jugada
        key = ultimo_nodo.get_key()
        fila = key.get_linea()
        columna = key.get_columna()
        valor_anterior = key.get_valor_anterior()
        valor_nuevo = key.get_valor_nuevo()  # Necesitamos este también
        
        # Revertir en el modelo
        self.modelo.set_valor(fila, columna, valor_anterior)
        
        # NUEVO: Actualizar posibilidades antes de actualizar la vista
        self.modelo.actualizar_posibilidades_deshacer(fila, columna, valor_anterior, valor_nuevo)
        
        # Actualizar la vista
        self.vista.establecer_valor(fila, columna, valor_anterior)

        # Actualizar las posibilidades en la vista
        self.vista.actualizar_posibilidades()
        
        # Mover de deshacer a rehacer
        self.modelo.mover_deshacer_a_rehacer(ultimo_nodo)
        
        # Crear y agregar Key para la acción de deshacer en jugadas
        key_deshacer = self.modelo.crear_key(fila, columna, key.get_valor_nuevo(), valor_anterior, "deshacer")
        nodo_jugadas = Nodo(key_deshacer)
        self.modelo.jugadas.insert(nodo_jugadas)
        
        # Actualizar vista de jugadas
        texto = f"L{fila + 1} C{columna + 1} {key.get_valor_nuevo()}->{valor_anterior} (deshacer)"
        self.vista.listbox_jugadas.insert(0, texto)
        
        # Actualizar listados de deshacer y rehacer
        self.vista.actualizar_listados_deshacer_rehacer()

    def rehacer_jugada(self):
        """Rehace la última jugada deshecha"""
        ultimo_nodo = self.modelo.obtener_ultima_jugada_rehacer()
        
        if ultimo_nodo is None:
            self.vista.mostrar_mensaje("Rehacer", "No hay jugadas para rehacer")
            return
        
        # Obtener información de la jugada
        key = ultimo_nodo.get_key()
        fila = key.get_linea()
        columna = key.get_columna()
        valor_anterior = key.get_valor_anterior()  # Necesitamos este también
        valor_nuevo = key.get_valor_nuevo()
        
        # Aplicar en el modelo
        self.modelo.set_valor(fila, columna, valor_nuevo)
        
        # NUEVO: Actualizar posibilidades antes de actualizar la vista
        self.modelo.actualizar_posibilidades_rehacer(fila, columna, valor_anterior, valor_nuevo)
        
        # Actualizar la vista
        self.vista.establecer_valor(fila, columna, valor_nuevo)
        
        # Actualizar las posibilidades en la vista
        self.vista.actualizar_posibilidades()
        
        # Mover de rehacer a deshacer
        self.modelo.mover_rehacer_a_deshacer(ultimo_nodo)
        
        # Crear y agregar Key para la acción de rehacer en jugadas
        key_rehacer = self.modelo.crear_key(fila, columna, key.get_valor_anterior(), valor_nuevo, "rehacer")
        nodo_jugadas = Nodo(key_rehacer)
        self.modelo.jugadas.insert(nodo_jugadas)
        
        # Actualizar vista de jugadas
        texto = f"L{fila + 1} C{columna + 1} {key.get_valor_anterior()}->{valor_nuevo} (rehacer)"
        self.vista.listbox_jugadas.insert(0, texto)
        
        # Actualizar listados de deshacer y rehacer
        self.vista.actualizar_listados_deshacer_rehacer()

    def dar_sugerencia(self):
        """Proporciona una sugerencia para la celda seleccionada"""
        # Verificar si hay una celda seleccionada
        if not self.vista.celda_seleccionada_pos:
            self.vista.mostrar_mensaje("Sugerencia", "No hay celda seleccionada")
            return
        
        fila, columna = self.vista.celda_seleccionada_pos
        
        # Obtener sugerencia del modelo
        resultado_sugerencia = self.modelo.obtener_sugerencia(fila, columna)
        
        if not resultado_sugerencia['exito']:
            # Mostrar mensaje de error
            self.vista.mostrar_mensaje("Sugerencia", resultado_sugerencia['mensaje'])
            return
        
        # Si la sugerencia fue exitosa, aplicarla
        valor_sugerido = resultado_sugerencia['valor']
        valor_anterior = self.modelo.get_valor(fila, columna)  # Debería ser 0
        
        # Procesar la sugerencia como una entrada normal
        resultado = self.procesar_entrada(fila, columna, valor_anterior, valor_sugerido)
        
        if resultado['exito']:
            # Actualizar la vista con el valor sugerido
            self.vista.establecer_valor(fila, columna, valor_sugerido)
            
            # Agregar el valor a noVolverASugerir
            self.modelo.agregar_a_no_volver_a_sugerir(fila, columna, valor_sugerido)
            
            # Actualizar las visualizaciones de las listas
            self.vista.actualizar_listados(resultado['key'])
            
            # Cambiar el tipo de la jugada para indicar que fue una sugerencia
            key = resultado['key']
            key.set_tipo("sugerencia")
            
            # Mostrar mensaje de éxito
            self.vista.mostrar_mensaje("Sugerencia", f"Sugerencia aplicada: {valor_sugerido}")
            
            # Si el juego está completo, mostrar mensaje
            if "completado" in resultado['mensaje'].lower():
                self.vista.mostrar_mensaje("¡Juego Completado!", resultado['mensaje'])
        else:
            # En caso de error (no debería ocurrir si la lógica es correcta)
            self.vista.mostrar_mensaje("Error", f"Error al aplicar sugerencia: {resultado['mensaje']}")
