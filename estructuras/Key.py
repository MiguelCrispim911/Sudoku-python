class Key:
    def __init__(self, linea, columna, valor_anterior, valor_nuevo):
        self.linea = 0
        self.columna = 0
        self.valor_anterior = 0
        self.valor_nuevo = 0
        self.tipo = ""
    
    def get_linea(self):
        return self.linea
    
    def set_linea(self, linea):
        self.linea = linea
    
    def get_columna(self):
        return self.columna
    
    def set_columna(self, columna):
        self.columna = columna
    
    def get_valor_anterior(self):
        return self.valor_anterior
    
    def set_valor_anterior(self, valor_anterior):
        self.valor_anterior = valor_anterior
    
    def get_valor_nuevo(self):
        return self.valor_nuevo
    
    def set_valor_nuevo(self, valor_nuevo):
        self.valor_nuevo = valor_nuevo
    
    def get_tipo(self):
        return self.tipo
    
    def set_tipo(self, tipo):
        self.tipo = tipo
