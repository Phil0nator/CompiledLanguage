


class Declaration:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset
    def __repr__(self):
        return f"{self.name} : {hex(self.offset)}"
        


