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
    
    # def search(self, k):
    #     x = self.head
    #     while x is not None and x.get_key() != k:
    #         x = x.get_next()
    #     return x
    # No es necesario buscar nodos!!!!!!!!!!
    
    def delete(self, x):
        if x.get_next() is not None:
            x.get_next().set_prev(x.get_prev())
        if x.get_prev() is not None:
            x.get_prev().set_next(x.get_next())
        else:
            self.head = x.get_next()
    
    def display(self):
        x = self.head
        while x is not None:
            print(f"{x} -> {x.get_key()}")
            x = x.get_next()