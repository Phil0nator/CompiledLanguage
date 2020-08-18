from Declaration import *
from Token import *
from errors import *
from constants import *

class Function:
    def __init__(self,name,params,tokens, compiler):
        self.tokens = tokens
        self.name = name
        if(name == "main"):
            self.name = "m"
        self.params = params
        self.compiler = compiler

        
        self.header = self.name+":"
        self.allocator = ""
        self.closer = "\nleave\nret\n"
        self.bodytext = ""

        self.allocationCounter = 4 
        self.declarations = []


        self.current_token = self.tokens[0]
        self.ct_idx = 0
    """
    #add a line to the body of a function's assembly
    """
    def addline(self, line):
        self.bodytext+=("%s\n"%line)
    """
    #add a new variable declaration, and increment stack ptr
    """
    def appendDeclaration(self, name):
        self.declarations.append(Declaration(name,self.allocationCounter))
        self.allocationCounter+=4










    """
    #Construct a statement that starts with a T_ID (based on current position)
    """
    def buildIDStatement(self):
        id = self.current_token.value
        self.advance()
        if(self.current_token.tok == "="):
            self.advance()
            self.evaluateExpression(decl=self.getDeclarationByID(id))
            return

        elif (self.current_token.tok == T_OPENP):
            pass
        else:
            throw(InvalidVariableAssignment(self.current_token.start,self.current_token.end,self.current_token.value))




    """
    #Get the variable declaration based on the variable name
    """
    def getDeclarationByID(self, name):
        for decl in self.declarations:
            if decl.name == name : return decl
        for p in self.params:
            if p == name : return parameter_registers[self.params.index(p)]
        return None




    """
    #Based on current position, generate assembly to: evaluate an expression, and place its final result into the variable described by decl 
    """
    def evaluateExpression(self, decl=None, reg=None, glob=None):
        expr = [] #holds the expression
        
        
        """

        #determine the contents of the expression:
        """
        while self.current_token.tok != None and self.current_token.tok != T_EOL and self.current_token.tok != T_CLOSEP:
            if(self.current_token.tok == T_EOL): break
            
            if(self.current_token.tok == T_INT or self.current_token == T_FLOAT or self.current_token.tok == T_BOOLEAN):
                expr.append(self.current_token.value)
                self.advance()

            elif(self.current_token.tok == T_ID):
                #accounting for global variables/local through ID
                if(not self.compiler.globalExists(self.current_token.value)):
                    expr.append(self.getDeclarationByID(self.current_token.value))
                    self.advance()
                else:
                    expr.append(self.current_token.value)
                    self.advance()

            elif(self.current_token.tok in "+-/*&!|%"):

                expr.append(self.current_token.tok)
                self.advance()
            elif(self.current_token.tok == T_OPENP):
                self.advance()
                self.evaluateExpression(reg="rdi")
                expr.append("rdi")
            else:
                throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))
            #max expression size
            
        if(self.current_token.tok == T_CLOSEP):
            self.advance()
        
        if(len(expr) == 1):
            if(isinstance(expr[0], Declaration )):
                self.addline("mov ebx, DWORD [rbp-"+hex(expr[0].offset)+"]")
            elif(isinstance(expr[0], int)):
                self.addline("mov ebx, "+hex(expr[0]))
            elif (self.compiler.globalExists( expr[0])):
                self.addline("mov %s, %s"%("ebx",value_of_global(expr[0])))
            elif (expr[0] == "rdi"):
                self.addline("mov ebx, rdi")
            else:
                throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))
            if(decl is not None): self.addline("mov DWORD [rbp-"+hex(decl.offset)+"], ebx")
            elif (reg is not None): self.addline("mov %s, ebx"%reg)
            else: self.addline("mov %s, ebx"%value_of_global(glob))
            return


        _reg = "ebx"
        if(str(expr[0]) in "*/"):
            _reg="eax"

        """

        #Create assembly for the move
        """
        if(isinstance(expr[0], Declaration )):
            self.addline(("mov %s, DWORD [rbp-"+hex(expr[0].offset)+"]")%_reg)
        elif(isinstance(expr[0], int)):
            self.addline(("mov %s, "+hex(expr[0]))%_reg)
        elif (self.compiler.globalExists( expr[0])):
            self.addline("mov %s, %s"%(_reg,value_of_global(expr[0])))
        elif (expr[0] in parameter_registers):
            self.addline("mov rax,"+expr[0])
            if(_reg=="ebx"):
                self.addline("mov ebx, eax")
        


        #move operand b into rcx reguardless
        if(isinstance(expr[2], Declaration )):
            self.addline("mov ecx, DWORD [rbp-"+hex(expr[2].offset)+"]")
        elif(isinstance(expr[2], int)):
            self.addline("mov ecx, "+hex(expr[2]))
        elif (self.compiler.globalExists( expr[2])):
            self.addline("mov %s, %s"%("ecx",value_of_global(expr[2])))
        elif (expr[2] in parameter_registers):
            self.addline("mov rcx, "+expr[2])
        elif (expr[2] == "rdi"):
            self.addline("mov rcx, rdi")
        else:

            throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))












        """
        #Create assembly for the math, and the re-deposit
        """
        #perform arithmatic, and move result into decl
        outputreg = "ebx"
        if(expr[1] == "+"):
            self.addline("add ebx, ecx")
        elif(expr[1] == "-"):
            self.addline("sub ebx, ecx")
        elif(expr[1] == "*"):
            self.addline("mul ecx")
            outputreg = "eax"
        elif(expr[1] == "/"):
            self.addline("xor edx, edx")
            self.addline("div ecx")
            outputreg = "eax"

        if(decl is not None): self.addline("mov DWORD [rbp-%s], %s"%(hex(decl.offset), outputreg))
        elif (reg is not None): self.addline("mov %s,%s"%(reg, outputreg.replace("e","r")))
        else: self.addline("mov %s,%s"%(value_of_global(glob), outputreg))













    



    def buildVariableDeclaration(self):
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))
            
        id = self.current_token.value
        self.advance()
        if(self.current_token.tok == T_EOL): #variable declaration without assignment
            self.appendDeclaration(id)
            self.advance()
            return
        
        if(self.current_token.tok == "="): #with assignment
            self.advance()
            self.appendDeclaration(id)
            if(not self.compiler.globalExists(id)):
                self.evaluateExpression(decl=self.declarations[len(self.declarations)-1])#evaluate expression, and place it into this declaration
            else:
                self.evaluateExpression(glob=id)

        else: #invalid statement
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))











    def buildReturnStatement(self):
        #current token will already be the return value
        if(self.current_token.tok == T_INT):
            self.addline("mov %s,%s"%(return_register, hex(self.current_token.value)))
            self.advance()
            
        elif (self.current_token.tok == T_ID):
            addr = self.getDeclarationByID(self.current_token.value).offset
            self.addline(load_value_toreg(addr,"ecx")) #use ecx as buffer to maintain correct operation size
            self.addline("mov %s, rcx"%return_register)
            self.advance()
        
        else:
            throw(InvalidExpressionComponent(self.current_token.start, self.current_token.end,self.current_token.value))













    def buildKeywordStatement(self):

        if(self.current_token.value == "var"):
            self.buildVariableDeclaration()
        if(self.current_token.value == "return"):
            self.advance()
            self.buildReturnStatement()

        else:
            self.advance()









    def compile(self):
        allocationoffset = 0
        for token in self.tokens:
            if(token.tok == T_KEYWORD and token.value == "var"):
                allocationoffset += 4

        self.allocator = allocate(allocationoffset)
        self.bodytext = "%s%s"%(self.allocator,self.bodytext)

        while self.current_token != None and self.current_token.tok != T_EOF:
            if(self.current_token.tok in T_EOL+T_OPENP+T_OSCOPE+T_CLSCOPE+T_COLON):
                self.advance()
            elif(self.current_token.tok == T_KEYWORD):
                self.buildKeywordStatement()
            elif(self.current_token.tok == T_ID):
                self.buildIDStatement()
            else:
                print(self.current_token)
                throw(UnkownStatementInitiator(self.current_token.start,self.current_token.end,self.current_token.value))




    def getFinalText(self):
        return self.header+"\n"+self.bodytext+"\n"+self.closer+"\n"

    def advance(self):
        self.ct_idx+=1
        if self.ct_idx < len(self.tokens):
            self.current_token = self.tokens[self.ct_idx]
        else:
            self.current_token = Token(T_EOF)




    def __repr__(self):

        return f'{self.name} ( {self.params} )'






