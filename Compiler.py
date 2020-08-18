from constants import *
from Token import *
from Function import *


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
        while self.current_token.tok != T_EOF:
            
            if(self.current_token.tok == T_EOL):
                self.advance()
            elif(self.current_token.tok == T_KEYWORD):
                if self.current_token.value in "final var":
                    self.createGlobal()
                elif self.current_token.value == "function":
                    self.createFunction()
                else:
                    self.advance()
        self.fill_functions()
        self.fill_globals()


    

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
                self._bss+=define_global(g)
                self.main+="mov DWORD ["+g+"], "+hex(glob[g])+"\n"
        
        for glob in self.globals[1] : #data:
            for g in glob:
                self._data += g+": db "+hex(glob[g])
        self.main+="call m"


    """
    #Based on the current position, create a function object including name, parameters, and function body   
    """
    def createFunction(self):
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))
        
        name = self.current_token.value
        self.advance()
        #looking for parameters
        if(self.current_token.tok != T_OPENP):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))

        self.advance()
        #closing parenthesis, or parameters
        params = []
        if(self.current_token.tok != T_CLOSEP):
            #parameters
            while self.current_token.tok != T_CLOSEP:
                if(self.current_token.tok == T_COMMA):
                    self.advance()
                elif (self.current_token.tok == T_ID):
                    params.append(self.current_token.value)
                    self.advance()
                else:
                    throw(InvalidFunctionParameterDeclaration(self.current_token.start,self.current_token.end,self.current_token.value))
        

        self.advance()#move past ')'
        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidFunctionDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))

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
            throw(EmptyFunction(self.current_token.start,self.current_token.end,self.current_token.value))
        

        function = Function(name,params,body,self)
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

    
    """
    #Based on the current position, read the current line and identify a global variable
    """
    def createGlobal(self):
        isFinal = False
        if(self.current_token.value == "final"):
            isFinal = True
            self.advance()
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))
        id = self.current_token.value
        self.advance()
        if(self.current_token.tok == T_EOL):
            #endline
            self.globals[int(isFinal)].append( {id:0} )
            self.advance()
            return

        if(self.current_token.tok != "="):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))

        self.advance()

        #value
        if(self.current_token.tok == T_INT or self.current_token.tok == T_FLOAT or self.current_token.tok == T_STRING or self.current_token.tok == T_BOOLEAN):
            self.globals[int(isFinal)].append({id:self.current_token.value})
            self.advance()
            return

        #not constant value, other identifier

        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))

        for catagory in self.globals:
            for glob in catagory:
                for g in glob:
                    if g == self.current_token.value:
                        self.globals[int(isFinal)].append({id:catagory[glob][g]})
                        self.advance() #EOL
                        self.advance()
                        return
        throw(UndefinedVariable(self.current_token.start,self.current_token.end,self.current_token.value))
        

    """ 
    #Step to the next token
     """
    def advance(self):
        self.ct_idx+=1
        if self.ct_idx < len(self.tokens):
            self.current_token = self.tokens[self.ct_idx]
        else:
            self.current_token = Token(T_EOF)




