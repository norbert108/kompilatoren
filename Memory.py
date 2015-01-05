
class Memory:

    def __init__(self):
        self.variables = {}

    def has_key(self, name):
        return name in self.variables.keys()

    def get(self, name):
        return self.variables.get(name)

    def put(self, name, value):
        self.variables[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None):
        self.stack = []
        if memory is not None:
            self.stack.append(memory)

    def get(self, name):
        stack_top = self.stack.pop()
        try:
            value = stack_top.get(name)
        except IndexError:
            return None
        self.stack.append(stack_top)

        return value

    # def insert(self, name, value):
    #     stack_top = self.stack.pop()
    #     stack_top.put(name, value)
    #     self.stack.append(stack_top)

    def set(self, name, value):
        stack_top = self.stack.pop()
        stack_top.put(name, value)
        self.stack.append(stack_top)

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()

