


class Declaration:
    def __init__(self, name, offset, isfloat):
        self.name = name
        self.offset = offset
        self.isfloat = isfloat
    def __repr__(self):
        return f"{self.name} : {str(self.offset)}\t isfloat: {self.isfloat}"
        


