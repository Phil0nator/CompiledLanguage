
class Location:
    def __init__(self, idx, ln, col, fn, ftext):
        self.idx=idx
        self.ln = ln
        self.col=col
        self.fn=fn
        self.ftext=ftext

    def advance(self, current_char):
        self.idx+=1
        self.col+=1
        if current_char == "\n":
            self.ln+=1
            self.col=0

        return self

    def copy(self):
        return Location(self.idx,self.ln,self.col,self.fn,self.ftext)

