import sys
from Lexer import *
from errors import *



class PreLexer:
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
            elif (self.current_char == "#" or self.current_char in ID_CHARS):
                tokens.append(self.make_identifier())
            elif(self.current_char in T_NUMBERS):
                tokens.append(self.make_number())
            elif (self.current_char == "\""):
                tokens.append(self.make_string())
            else:
                self.advance()
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
        if(not num.startswith("-") and "-" in num) or (num == "-"):
            print("Invalid Integer value: "+num)
            exit(1)
        if(dots==0):
            return Token(T_INT, value=int(num), start=start,end=self.loc)
        else:
            return Token(T_FLOAT,value=float(num), start=start,end=self.loc)


    

            
    def make_string(self):
        out = ''
        start = self.loc.copy()
        self.advance()
        esc = False
        while self.current_char != None and self.current_char != "\"":
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
        while self.current_char !=None and self.current_char in ID_CHARS+"#":
            out+=self.current_char
            
            self.advance()
        
        if out in KEYWORDS:
            _type = T_KEYWORD
            if(out == "true" or out == "false"):
                _type = T_BOOLEAN
                out = -int(out=="true")
        else:
            _type = T_ID

        return Token(_type, value=out,start=start,end=self.loc)






class Preprocessor:
    def __init__(self, data, cc, fn):
        self.data = data
        self.cc = cc
        self.lexer = PreLexer(0,data)
        self.tokens, error = self.lexer.make_tokens()

        self.current_token = self.tokens[0]

        self.ct_idx = 0

    def advance(self):
        self.ct_idx+=1
        self.current_token=self.tokens[self.ct_idx]
    
    def fileExists(self, file):
        for f in self.cc["FILES"]:
            if f == file:
                return True
        return False 
    
    def buildInclude(self):
        self.advance()
        if(self.current_token.tok != T_STRING):
            throw(EmptyIncludeStatement(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        
        file = self.current_token.value

        if(self.fileExists(file)):
            self.data=self.data.replace("#include \""+file+"\"", "",1)
            self.advance()
            return

        self.cc["FILES"].append(file)
        try:
            with open(file, "rb") as f:
                newdata = pre_process(f.read().decode(),self.cc)
        except:
            print("File does not exist: %s"%file)
            exit(1)
        self.data=self.data.replace("\"%s\""%file, "",1)
        self.data=self.data.replace("#include","\n"+newdata+"\n"+chr(3), 1)
        self.advance()

    def buildDefine(self):
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidDefinrdirective(self.current_token.start.idx,self.current_token.end,self.current_token.value))
        id = self.current_token.value
        self.advance()
        if(self.current_token.tok in T_INT+T_FLOAT+T_STRING+T_BOOLEAN):
            self.data=self.data.replace("#define "+id+" "+str(self.current_token.value),"",1)
            
            cc["DEF"].append({id:str(self.current_token.value)})
            self.advance()
        else:
            cc["DEF"].append({id:None})

            
    def process(self):
        while self.current_token.tok != T_EOF:
            if(self.current_token.tok == T_KEYWORD):
                if(self.current_token.value == "#include"):
                    self.buildInclude()
                elif(self.current_token.value == "#define"):
                    self.buildDefine()
                else:
                    self.advance()
            else:
                self.advance()

        for d in cc["DEF"]:
            for id in d:
                self.data=self.data.replace(id,d[id])

        return self.data


def pre_process(data,cc):
    prep = Preprocessor(data,cc, 0)


    return prep.process()





""" THE OLD WAY
def include(file_indicator, data,cc):

    if(file_indicator.startswith("\"")):
        with open(file_indicator.replace("\"",""), "rb") as f:
            cc["FILES"].append(file_indicator.replace("\"",""))        
            return pre_process(f.read().decode(),cc)














def pre_process(data,cc):
    lines = data.split("\n")
    i =0
    
    for line in lines:
        if(line.startswith("#")):
            if(line[1:8] == "include"):
               lines[i]=include(line.split(" ")[1],data,cc)+chr(3)#+"\n&&FN:"+line.split(" ")[1]+"&&"
            elif(line[1:7] == "define"):
                cc["DEF"][line.split(" ")[1]] = line.split(" ")[2]
                lines[i] = ""




            else:
                print("Unkown Preprocessor Directive: "+line)
                exit(1)
        i+=1

    data = ""
    for line in lines:
        data+=line+"\n"

    for definition in cc["DEF"]:
        data = data.replace(definition,cc["DEF"][definition])


    return data
"""