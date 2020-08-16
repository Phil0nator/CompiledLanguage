import os
import sys
from preprocessor import *
from constants import *



class Error:
    def __init__(self, start, end, error, details):
        self.start=start
        self.end=end
        self.error=error
        self.details=details
    def as_string(self):
        result = f'{self.error}:{self.details}\n'
        result += f'File : {cc["FILES"][len(cc["FILES"])-1-self.start.fn]}, line : {self.start.ln+1}'
        return result

def throw(e):
    print(e.as_string())

class UnexpectedTokenError(Error):
    def __init__(self, start, end, details):
        super().__init__(start,end,"Unexpected Token", details)



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



class Token:
    def __init__(self, tok, value=None, start=None, end=None):
        self.tok=tok
        self.value=value
    def __repr__(self):
        if self.value:
            return f'{self.tok} : {self.value}'
        return f'{self.tok}'


class Lexer:
    def __init__(self, fn ,text):
        self.fn = fn
        self.text=text
        self.loc = Location(-1,0,-1,fn,text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.loc.advance(self.current_char)
        self.current_char = self.text[self.loc.idx] if self.loc.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []


        while self.current_char != None:
            if(self.current_char in ' \t'):#ignore whitespace 
                self.advance()
            elif (ord(self.current_char) == 3):#file counter
                self.fn+=1
                self.loc.fn+=1
                self.loc.ln = 0
                self.advance()
            elif self.current_char in T_NUMBERS:
                tokens.append(self.make_number())
            elif self.current_char in ID_CHARS:
                tokens.append(self.make_identifier())
            elif self.current_char == "\"":
                tokens.append(self.make_string())
            elif self.current_char in TM_ALL:
                #print(self.current_char)
                #tokens.append(Token(self.current_char, start=self.loc))
                tokens.append(self.make_multichar())
            elif self.current_char == ";":
                tokens.append(Token(T_EOL, start=self.loc))
                self.advance()
            elif self.current_char == "\n":
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS,start=self.loc))
                self.advance()
            elif self.current_char == "&":
                tokens.append(Token(T_AMPERSAND, start=self.loc))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL, start=self.loc))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(T_DIV, start=self.loc))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(T_OPENP,start=self.loc))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(T_CLOSEP, start=self.loc))
                self.advance()
            elif self.current_char== "{":
                tokens.append(Token(T_OSCOPE, start=self.loc))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(T_CLSCOPE, start=self.loc))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(T_OPENLINDEX, start=self.loc))
                self.advance()

            elif self.current_char == "]":
                tokens.append(Token(T_CLSLINDEX, start=self.loc))
                self.advance()


            

            
            
            else:
                start = self.loc.copy()
                char = self.current_char
                self.advance()
                return [], UnexpectedTokenError(start,self.loc,"'%s'"%char)





        tokens.append(Token(T_EOF, start=self.loc))      

        return tokens, None
    def make_number(self):
        num = ''
        dots = 0
        start=self.loc.copy()
        while self.current_char != None and self.current_char in T_NUMBERS + '.':
            if self.current_char == ".":
                if dots == 1: break #two decimals in one number??
                dots+=1
                num+="."
            else:
                num+=self.current_char
            self.advance()

            if(dots==0):
                return Token(T_INT, value=int(num), start=start,end=self.loc)
            else:
                return Token(T_FLOAT,value=float(num), start=start,end=self.loc)


    def make_multichar(self):
        out =''
        start = self.loc.copy()
        out+=self.current_char
        self.advance()
        if(self.current_char == None or self.current_char not in TM_ALL):
            return Token(out,start=start)
        out+=self.current_char
        self.advance()
        return Token(out,start=start,end=self.loc)
    

            
    def make_string(self):
        out = ''
        start = self.loc.copy()
        self.advance()
        esc = False
        while self.current_char != None and self.current_char != "!":
            if (self.current_char == "\\"):
                esc=True
            else:
                if(esc):
                    esc=False
                    out += ESCAPE_CHARS[self.current_char]
                else:
                    out+=self.current_char

            self.advance()

        self.advance()
        return Token(T_STRING,value=out,start=start,end=self.loc)

    def make_identifier(self):
        out = ''
        start = self.loc.copy()
        while self.current_char !=None and self.current_char in ID_CHARS:
            out+=self.current_char
            
            self.advance()
        
        if out in KEYWORDS:
            _type = T_KEYWORD
        else:
            _type = T_ID

        return Token(_type, value=out,start=start,end=self.loc)

class Compiler:
    def __init__(self, tokens, cc):
        self.tokens=tokens
        self.asm = ""+top_stub
        self._data = ""
        self._text = "call main"
        self._bss = ""
        self._fdef = ""
        self.functions = []
        self.cc= cc


    def writeToFile(self, fname):
        with open(fname, "wb") as f:
            f.write(self.asm.encode())








cc = {}

def main(file_to_compile):
    
    global cc
    data = ""

    


    
    cc["DEF"] = {}
    cc["GL_VAR"] = []
    cc["FILES"] = [sys.argv[1]]

    with open(file_to_compile, "rb") as f:
        data = f.read().decode()

    data = pre_process(data,cc)
    l = Lexer(0, data)
    tokens, errors = l.make_tokens()
    if(errors != None):
        print(errors.as_string())
        exit(1)
    print(tokens)

    
    
if( __name__ == "__main__"):
    main(sys.argv[1])
