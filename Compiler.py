from constants import *
from Token import *
from Function import *
from Location import *
from Struct import *


class Compiler:
    def __init__(self, tokens):
        self.tokens = tokens
        self.functions = []
        self.globals = [[],[]] #[0] = bss, [1] = data
        self.constants = []

        self.current_token = tokens[0]
        self.ct_idx = 0

        self._bss = ""
        self._data = ""
        self._fdef = ""
        self.main = ""
    """
    #main function to be called
    #will call all others
    #step through token by token, and organize the program into functions and globals
    """
    def fill_info(self):


        #move constant strings to .data
        
        counter = 0
        fltcnter = 0
        i=0
        while(i < len(self.tokens)):
            tok = self.tokens[i]
            if(tok.value == "__asm"):
                i+=3
                continue
            
            if(tok.tok == T_STRING):
                
                tok.tok = T_ID
                value = tok.value
                tok.value = "STRING_CONSTANT_"+str(counter)
                
                self.globals[1].append({"STRING_CONSTANT_"+str(counter): value, "isfloat":False})
                counter += 1

            if(tok.tok == T_FLOAT):
                tok.tok = T_ID
                value = tok.value
                tok.value = "FLT_CONSTANT_"+str(fltcnter)
                self.globals[1].append({"FLT_CONSTANT_"+str(fltcnter) : value, "isfloat":True})
                fltcnter+=1

            
            i+=1

        self.globals[1].append({"__FLT_STANDARD_1":1.0, "isfloat":True})

        while self.current_token.tok != T_EOF:
            
            if(self.current_token.tok == T_EOL):
                self.advance()
            elif(self.current_token.tok == T_KEYWORD):
                if self.current_token.value in ["final", "var", "float"]:
                    self.createGlobal()
                elif self.current_token.value == "function":
                    self.createFunction()
                elif self.current_token.value == "struct":
                    self.createStructure()
                else:
                    throw(UnexpectedTokenError(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
            else:
                throw(UnexpectedTokenError(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        self.fill_functions()
        self.fill_globals()


    def createStructure(self):
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        name = self.current_token.value
        self.advance()
        #looking for parameters
        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        
        self.advance() #move past '{'
        #BODY
        body = []
        ignorables = 0
        while not (ignorables == 0 and self.current_token.tok == T_CLSCOPE):
            if(self.current_token.tok == T_OSCOPE):
                ignorables+=1
            if(self.current_token.tok == T_CLSCOPE):
                ignorables-=1
            body.append(self.current_token)
            self.advance()

        if(len(body) == 0):
            throw(EmptyFunction(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        
        struct = Struct(name, body)
        self._fdef+=struct.compile()
        self.advance()



    """
    Compile each function
    """
    def fill_functions(self):
        for function in self.functions:
            function.compile()
            self._fdef+=function.getFinalText()


    """
    #Generate assembly for global variables
    """
    def fill_globals(self):
        for glob in self.globals[0] : #bss:
            for g in glob:
                if(g != "isfloat"):
                    self._bss+=define_global(g)
                    if(isinstance(glob[g], float)):
                        self.main+="mov QWORD ["+g+"], "+str(glob[g])+"\n"
                    else:
                        self.main+="mov QWORD ["+g+"], "+hex(glob[g])+"\n"
        
        for glob in self.globals[1] : #data:
            for g in glob:
                if(g != "isfloat"):
                    if(isinstance(glob[g], str)):
                        self._data += g+": db `"+glob[g]+"`, 0\n"
                    elif (isinstance(glob[g], float)):
                        #self._data += g+": dq __float32("+str(glob[g])+")__\n"
                        self._data += g+": dq __float32__("+str(glob[g])+")\n"
                    else:
                        self._data += g+": dq "+hex(glob[g])+"\n"
        self.main+="call m"


    """
    #Based on the current position, create a function object including name, parameters, and function body   
    """
    def createFunction(self):
        self.advance()
        isFast = False
        if(self.current_token.tok == T_KEYWORD and self.current_token.value == "fast"):
            isFast = True
            self.advance()

        if(self.current_token.tok != T_ID):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        
        name = self.current_token.value
        self.advance()
        #looking for parameters
        if(self.current_token.tok != T_OPENP):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        self.advance()
        #closing parenthrsis, or parameters
        params = []
        types = []
        if(self.current_token.tok != T_CLOSEP):
            #parameters
            while self.current_token.tok != T_CLOSEP:
                if(self.current_token.tok == T_COMMA):
                    self.advance()
                elif (self.current_token.tok == T_ID):
                    params.append(self.current_token.value)
                    types.append("var")
                    self.advance()
                elif (self.current_token.tok == T_KEYWORD and self.current_token.value == "float"):
                    types.append("float")
                    self.advance()
                    if(self.current_token.tok != T_ID):throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
                    params.append(self.current_token.value)
                    self.advance()
                else:
                    throw(InvalidFunctionParameterDeclaration(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        

        self.advance()#move past ')'
        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        self.advance() #move past '{'
        #BODY
        body = []
        ignorables = 0
        while not (ignorables == 0 and self.current_token.tok == T_CLSCOPE):
            if(self.current_token.tok == T_OSCOPE):
                ignorables+=1
            if(self.current_token.tok == T_CLSCOPE):
                ignorables-=1
            body.append(self.current_token)
            self.advance()

        if(len(body) == 0):
            throw(EmptyFunction(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        

        function = Function(name,params,body,self,types)
        function.isFast=isFast
        self.advance()
        self.functions.append(function)
        
    """
    #Determine if a name represents a global variable
    @param name: name of a global
    @returns : boolean 
    """
    def globalExists(self, name):
        for c in self.globals:
            for glob in c:
                for g in glob:
                    if(g == name):
                        return True
        return False

    
    def globalIsString(self, name):
        for c in self.globals:
            for glob in c:
                for g in glob:
                    if(g == name):
                        return isinstance( glob[g], str)
        return False

    def globalIsFloat(self, name):
        for c in self.globals:
            for glob in c:
                for g in glob:
                    
                    if(g == name):
                        return glob["isfloat"] 
        return False

    def getFunctionByName(self, name):
        for fn in self.functions:
            if(fn.name == name):
                return fn
        return None

    """
    #Based on the current position, read the current line and identify a global variable
    """
    def createGlobal(self):
        isFinal = False
        if(self.current_token.value == "final"):
            isFinal = True
            self.advance()
        flt = False
        if(self.current_token.value == "float"):
            flt = True
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        id = self.current_token.value
        self.advance()
        if(self.current_token.tok == T_EOL):
            #endline
            self.globals[int(isFinal)].append( {id:0, "isfloat":flt} )
            self.advance()
            return

        if(self.current_token.tok != "="):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        self.advance()

        #value
        if(self.current_token.tok == T_INT or self.current_token.tok == T_FLOAT or self.current_token.tok == T_STRING or self.current_token.tok == T_BOOLEAN):
            self.globals[int(isFinal)].append({id:self.current_token.value, "isfloat":flt})
            self.advance()
            return

        #not constant value, other identifier

        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))

        for catagory in self.globals:
            for glob in catagory:
                for g in glob:
                    if g == self.current_token.value:
                        
                        self.globals[int(isFinal)].append({id:glob[g], "isfloat":flt})
                        self.advance() #EOL
                        self.advance()
                        return
        throw(UndefinedVariable(self.current_token.start,self.current_token.end,self.current_token.value, self.current_token.tok))
        

    """ 
    #Step to the next token
     """
    def advance(self):
        self.ct_idx+=1
        if self.ct_idx < len(self.tokens):
            self.current_token = self.tokens[self.ct_idx]
        else:
            self.current_token = Token(T_EOF)




