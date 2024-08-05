class Stack:
    def __init__(self):
        self.stack = []

    def push(self, clientId, x, y, z):
        # Push a tuple (clientId, x, y, z) onto the stack
        self.stack.append((clientId, x, y, z))

    def pop(self):
        # Pop the top item from the stack and return it
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("pop from an empty stack")

    def peek(self):
        # Peek at the top item of the stack without removing it
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("peek from an empty stack")

    def is_empty(self):
        # Check if the stack is empty
        return len(self.stack) == 0

    def size(self):
        # Return the size of the stack
        return len(self.stack)

    def __str__(self):
        # Return a string representation of the stack
        return str(self.stack)