class MainMemory:
    def __init__(self, initial_values):
        self.storage = initial_values.copy()

    def read(self, tag):
        return self.storage[tag]

    def write(self, tag, value):
        self.storage[tag] = value

    def get_all(self):
        return self.storage.copy()