class Nodo:
    def __init__(self, k):
        self.key = k
        self.prev = None
        self.next = None
    
    def get_key(self):
        return self.key
    
    def set_key(self, key):
        self.key = key
    
    def get_prev(self):
        return self.prev
    
    def set_prev(self, prev):
        self.prev = prev
    
    def get_next(self):
        return self.next
    
    def set_next(self, next):
        self.next = next