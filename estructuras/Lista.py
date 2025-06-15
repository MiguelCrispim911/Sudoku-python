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
    
    def delete_nodo(self, x):
        if x.get_next() is not None:
            x.get_next().set_prev(x.get_prev())
        if x.get_prev() is not None:
            x.get_prev().set_next(x.get_next())
        else:
            self.head = x.get_next()

    def delete_todos_nodos(self):
        x = self.head
        while x is not None:
            next_node = x.get_next()
            del x
            x = next_node
        self.head = None