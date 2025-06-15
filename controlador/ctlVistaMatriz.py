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
            # Vincula el evento de cambio de valor
            celda.bind('<KeyRelease>', lambda e, f=fila, c=columna: self.on_celda_change(e, f, c))
            # También vincula FocusOut para capturar cambios cuando se sale de la celda
            celda.bind('<FocusOut>', lambda e, f=fila, c=columna: self.on_celda_change(e, f, c))

    def on_celda_change(self, event, fila, columna):
        """Maneja el evento de cambio de valor en una celda"""
        if event.widget['state'] == 'readonly':
            return  # Ignorar celdas bloqueadas

        # Obtener el valor anterior
        valor_anterior = self.modelo.matrizJuego[fila][columna]
        
        # Obtener el nuevo valor
        nuevo_texto = event.widget.get().strip()
        valor_nuevo = int(nuevo_texto) if nuevo_texto.isdigit() else 0

        # Si hubo un cambio real de valor
        if valor_anterior != valor_nuevo:
            # Procesar la entrada en el modelo
            exito, mensaje, key = self.modelo.procesar_entrada(fila, columna, valor_anterior, valor_nuevo)
            
            if not exito and key is None:  # Jugada inválida
                # Revertir el cambio visual
                event.widget.delete(0, 'end')
                if valor_anterior != 0:
                    event.widget.insert(0, str(valor_anterior))
                
                # Mostrar mensaje de error
                self.vista.mostrar_mensaje("Jugada Inválida", mensaje)
                return
            
            if exito and key:
                # Actualizar las visualizaciones de las listas
                self.vista.actualizar_listados(key)
                
                # Si el juego está completo, mostrar mensaje
                if "completado" in mensaje.lower():
                    self.vista.mostrar_mensaje("¡Juego Completado!", mensaje)

    def deshacer_jugada(self):
        """Deshace la última jugada"""
        if self.modelo.deshacer.get_head() is None:
            self.vista.mostrar_mensaje("Deshacer", "No hay jugadas para deshacer")
            return
        
        # Obtener la última jugada
        ultimo_nodo = self.modelo.deshacer.get_head()
        key = ultimo_nodo.get_key()
        
        # Revertir en la matriz
        fila = key.get_linea()
        columna = key.get_columna()
        valor_anterior = key.get_valor_anterior()
        
        self.modelo.matrizJuego[fila][columna] = valor_anterior
        
        # Actualizar la vista
        self.vista.establecer_valor(fila, columna, valor_anterior)
        
        # Mover de deshacer a rehacer
        self.modelo.deshacer.delete_nodo(ultimo_nodo)
        self.modelo.rehacer.insert(ultimo_nodo)
        
        # Crear un Key para registrar la acción de deshacer en jugadas
        key_deshacer = Key(fila, columna, key.get_valor_nuevo(), valor_anterior)
        key_deshacer.set_tipo("deshacer")
        
        # Agregar SOLO a la lista de jugadas (no tocar deshacer/rehacer para esto)
        nodo_jugadas = Nodo(key_deshacer)
        self.modelo.jugadas.insert(nodo_jugadas)
        
        # Actualizar SOLO el listado de jugadas con la acción de deshacer
        texto = f"L{fila + 1} C{columna + 1} {key.get_valor_nuevo()}->{valor_anterior} (deshacer)"
        self.vista.listbox_jugadas.insert(0, texto)
        
        # Actualizar listados de deshacer y rehacer
        self.vista.actualizar_listados_deshacer_rehacer()

    def rehacer_jugada(self):
        """Rehace la última jugada deshecha"""
        if self.modelo.rehacer.get_head() is None:
            self.vista.mostrar_mensaje("Rehacer", "No hay jugadas para rehacer")
            return
        
        # Obtener la última jugada deshecha
        ultimo_nodo = self.modelo.rehacer.get_head()
        key = ultimo_nodo.get_key()
        
        # Aplicar en la matriz
        fila = key.get_linea()
        columna = key.get_columna()
        valor_nuevo = key.get_valor_nuevo()
        
        self.modelo.matrizJuego[fila][columna] = valor_nuevo
        
        # Actualizar la vista
        self.vista.establecer_valor(fila, columna, valor_nuevo)
        
        # Mover de rehacer a deshacer
        self.modelo.rehacer.delete_nodo(ultimo_nodo)
        self.modelo.deshacer.insert(ultimo_nodo)
        
        # Crear un Key para registrar la acción de rehacer en jugadas
        key_rehacer = Key(fila, columna, key.get_valor_anterior(), valor_nuevo)
        key_rehacer.set_tipo("rehacer")
        
        # Agregar SOLO a la lista de jugadas (no tocar deshacer/rehacer para esto)
        nodo_jugadas = Nodo(key_rehacer)
        self.modelo.jugadas.insert(nodo_jugadas)
        
        # Actualizar SOLO el listado de jugadas con la acción de rehacer
        texto = f"L{fila + 1} C{columna + 1} {key.get_valor_anterior()}->{valor_nuevo} (rehacer)"
        self.vista.listbox_jugadas.insert(0, texto)
        
        # Actualizar listados de deshacer y rehacer
        self.vista.actualizar_listados_deshacer_rehacer()