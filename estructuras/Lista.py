from estructuras.Key import Key

class Lista:
    def __init__(self):
        self.head = None
    
    def get_head(self):
        return self.head
    
    def set_head(self, head):
        self.head = head
    
    def insert(self, x):
        x.set_prev(None)
        x.set_next(self.head)
        if self.head is not None:
            self.head.set_prev(x)
        self.head = x
    
    def search(self, k):
         x = self.head
         while x is not None and x.get_key() != k:
             x = x.get_next()
         return x
    
    
    def delete_nodo(self, x):
        if x.get_next() is not None:
            x.get_next().set_prev(x.get_prev())
        if x.get_prev() is not None:
            x.get_prev().set_next(x.get_next())
        else:
            self.head = x.get_next()
    
    def display(self):
        x = self.head
        while x is not None:
            key = x.get_key()
            print(f"f{key.get_linea()} c{key.get_columna()}  {key.get_valor_anterior()}-> {key.get_valor_nuevo()} ({key.get_tipo()})")
            x = x.get_next()

    def delete_todos_nodos(self):
        x = self.head
        while x is not None:
            next_node = x.get_next()
            del x
            x = next_node
        self.head = None
    
    def crear_key_string(self, linea, columna, valor_anterior, valor_nuevo, tipo):
        key = Key(linea, columna, valor_anterior, valor_nuevo)
        key.set_tipo(tipo)
        return key