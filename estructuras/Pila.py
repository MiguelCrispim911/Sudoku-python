class Pila:
    def __init__(self, n):
        self.n = n
        self.top = -1
        self.s = [None] * n

    def empty(self):
        return self.top == -1

    def full(self):
        return self.top == self.n - 1

    def push(self, x):
        if self.full():
            print("Overflow")
        else:
            self.top += 1
            self.s[self.top] = x

    def pop(self):
        if self.empty():
            print("Underflow")
            return None
        else:
            item = self.s[self.top]
            self.top -= 1
            return item
