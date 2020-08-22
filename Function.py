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

        self.allocationCounter = 8
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
        self.allocationCounter+=8



    def buildFunctionCall(self, id):
        fn_name = id
        #first push the parameter registers in use:
        for i in range(len(self.params)):
            pass
            ###########self.addline("push %s"%parameter_registers[i])

        #collect parameters
        params = []

        if(self.current_token.tok == T_CLOSEP): #No parameters
            pass
            
        else:
            self.evaluateExpression(reg=parameter_registers[len(params)])
            params.append(parameter_registers[len(params)])
            while self.current_token.tok != T_CLOSEP and self.current_token.tok != "->" and self.current_token.tok != T_EOL:
                if(self.current_token.tok == T_COMMA):
                    self.advance()
                    self.evaluateExpression(reg=parameter_registers[len(params)])
                    params.append(parameter_registers[len(params)])
                elif(self.current_token.tok == T_ID):
                    self.evaluateExpression(reg=parameter_registers[len(params)])
                    params.append(parameter_registers[len(params)])
                elif (self.current_token.tok == T_INT or self.current_token.tok == T_FLOAT):
                    self.evaluateExpression(reg=parameter_registers[len(params)])
                    params.append(parameter_registers[len(params)])
                else:
                    throw(InvalidParameter(self.current_token.start,self.current_token.end,self.current_token.value))

        #params are filled
        self.addline("call "+fn_name)
        
        if(len(params) == 0):
            for i in range(len(self.params)):
                pass
                ##########self.addline("pop %s"%parameter_registers[len(self.params)-(i+1)])
            
            

        if(self.current_token.tok == ")"):
            self.advance()#move past ')'
        
        
        if(self.current_token.tok == "->"): #use return value
            self.advance()
            if(self.current_token.tok != T_ID):
                throw(InvalidFunctionReturnDestination(self.current_token.start,self.current_token.end,self.current_token.value))

            if(self.compiler.globalExists( self.current_token.value ) ):
                self.addline("mov %s,r8"% value_of_global(self.current_token.value, self.compiler) )
            else:
                self.addline(place_value_from_reg(self.getDeclarationByID(self.current_token.value).offset, "r8"))
        for i in range(len(self.params)):
            pass
            #########self.addline("pop %s"%(parameter_registers[len(self.params)-(i+1)]))
        
        self.advance() # end the line

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
        elif (self.current_token.tok == "++"):
            self.advance()
            self.addline(load_value_toreg(self.getDeclarationByID(id).offset,"rax"))
            self.addline("inc rax")
            self.addline(place_value_from_reg(self.getDeclarationByID(id).offset, "rax"))
        elif (self.current_token.tok == "--"):
            self.advance()
            self.addline(load_value_toreg(self.getDeclarationByID(id).offset,"rax"))
            self.addline("dec rax")
            self.addline(place_value_from_reg(self.getDeclarationByID(id).offset, "rax"))
        elif (self.current_token.tok == T_OPENP):
            self.advance()
            self.buildFunctionCall(id)
        else:
            print(self.current_token)
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


    TEST: removed parameter registers by pre-allocating them as declarations at the begining of a function


    """
    def evaluateExpression(self, decl=None, reg=None, glob=None):
        expr = [] #holds the expression
        
        
        """

        #determine the contents of the expression:
        """
        while self.current_token.tok != None and self.current_token.tok != T_EOL and self.current_token.tok != T_CLOSEP:
            if(self.current_token.tok in T_EOL+T_COMMA): break
            
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

            elif(self.current_token.tok in "++--/*&!|%"):

                expr.append(self.current_token.tok)
                self.advance()
            elif(self.current_token.tok == T_OPENP):
                self.advance()
                self.evaluateExpression(reg="rdi")
                expr.append("rdi")
            else:
                print(self.current_token)

                throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))
            #max expression size
            
        if(self.current_token.tok in T_CLOSEP+T_COMMA+T_EOL):
            self.advance()
            

        if(reg == None): 
       
            if(len(expr) == 1):
                if(isinstance(expr[0], Declaration )):
                    self.addline("mov rbx, QWORD [rbp-"+hex(expr[0].offset)+"]")
                elif(isinstance(expr[0], int)):
                    self.addline("mov rbx, "+hex(expr[0]))
                elif (self.compiler.globalExists( expr[0])):
                    self.addline("mov %s, %s"%("rbx",value_of_global(expr[0], self.compiler  )))
                
                elif (expr[0] == "rdi"):
                    self.addline("mov rbx, rdi")
                else:
                    print(self.current_token)
                    throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))
                if(decl is not None): self.addline("mov QWORD [rbp-"+hex(decl.offset)+"], rbx")
                elif (reg is not None): self.addline(correct_mov(reg,"rbx"))
                else: self.addline("mov %s, rbx"%value_of_global(glob, self.compiler))
                return
        else:
            
            if(len(expr) == 1):

                if(isinstance(expr[0], Declaration )):
                    self.addline(("mov %s, QWORD [rbp-"%reg)+hex(expr[0].offset)+"]")
                elif(isinstance(expr[0], int)):
                    self.addline(("mov %s, "%reg)+hex(expr[0]))
                elif (expr[0] == "rdi"):
                    self.addline("mov %s, rdi"%reg)
                elif (self.compiler.globalExists( expr[0])):
                    self.addline("mov %s, %s"%(reg,value_of_global(expr[0], self.compiler  )))
                else:
                    print(self.current_token)
                    throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))
                return
        

        _reg = "rbx"
        if(str(expr[0]) in "*/"):
            _reg="rax"

        """

        #Create assembly for the move
        """
        if(isinstance(expr[0], Declaration )):
            self.addline(("mov %s, QWORD [rbp-"+hex(expr[0].offset)+"]")%_reg)
        elif(isinstance(expr[0], int)):
            self.addline(("mov %s, "+hex(expr[0]))%_reg)
        elif (self.compiler.globalExists( expr[0])):
            self.addline("mov %s, %s"%(_reg,value_of_global(expr[0], self.compiler)))
        
        

        if(len(expr) == 2):
            if(expr[1] == "++"):
                self.addline("inc %s"%_reg)
            elif(expr[1] == "--"):
                self.addline("dec %s"%_reg)
            if(_reg != "rbx"):
                self.addline("mov rbx, %s"%_reg)
            if(decl is not None): self.addline("mov QWORD [rbp-%s], %s"%(hex(decl.offset), "rbx"))
            elif (reg is not None): 
                self.addline(correct_mov(reg,"rbx"))
            else: self.addline("mov %s,%s"%(value_of_global(glob, self.compiler), "rbx"))
            return


        #move operand b into rcx reguardless
        if(isinstance(expr[2], Declaration )):
            self.addline("mov rcx, QWORD [rbp-"+hex(expr[2].offset)+"]")
        elif(isinstance(expr[2], int)):
            self.addline("mov rcx, "+hex(expr[2]))
        elif (self.compiler.globalExists( expr[2])):
            self.addline("mov %s, %s"%("rcx",value_of_global(expr[2], self.compiler)))
        
        elif (expr[2] == "rdi"):
            self.addline("mov rcx, rdi")
        else:

            throw(InvalidExpressionComponent(self.current_token.start,self.current_token.end,self.current_token.value))












        """
        #Create assembly for the math, and the re-deposit
        """
        #perform arithmatic, and move result into decl
        outputreg = "rbx"
        if(expr[1] == "+"):
            self.addline("add rbx, rcx")
        elif(expr[1] == "-"):
            self.addline("sub rbx, rcx")
        elif(expr[1] == "*"):
            self.addline("imul rcx")
            outputreg = "rax"
        elif(expr[1] == "/"):
            self.addline("xor rdx, rdx")
            self.addline("idiv rcx")
            outputreg = "rax"

        if(decl is not None): self.addline("mov QWORD [rbp-%s], %s"%(hex(decl.offset), outputreg))
        elif (reg is not None): 
            self.addline(correct_mov(reg,outputreg))
        else: self.addline("mov %s,%s"%(value_of_global(glob, self.compiler), outputreg))













    



    def buildVariableDeclaration(self):
        self.advance()
        if(self.current_token.tok != T_ID):
            throw(InvalidVariableDeclarator(self.current_token.start,self.current_token.end,self.current_token.value))
            
        id = self.current_token.value
        if(self.getDeclarationByID(id) != None):
            throw(VariableReDeclaration(self.current_token.start,self.current_token.end,self.current_token.value))
        self.advance()
        if(self.current_token.tok == T_EOL): #variable declaration without assignment
            self.appendDeclaration(id)
            
            self.addline(place_value_from_reg(self.declarations[len(self.declarations)-1].offset, "0x0"))
            #self.advance()
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
        self.evaluateExpression(reg="r8")
        






    def buildAsmBlock(self):
        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidASMBlock(self.current_token.start,self.current_token.end,self.current_token.value))

        self.advance()
        if(self.current_token.tok != T_STRING):
            throw(InvalidASMBlock(self.current_token.start,self.current_token.end,self.current_token.value))
        self.addline(self.current_token.value)
        self.advance()
        if(self.current_token.tok != T_CLSCOPE):
            throw(InvalidASMBlock(self.current_token.start,self.current_token.end,self.current_token.value))
        self.advance()


    def buildForBlock(self):
        if(self.current_token.tok != T_OPENP):
            throw(InvalidForBlockInit(self.current_token.start,self.current_token.end,self.current_token.value))
        
        self.advance()
        if(self.current_token.tok != T_KEYWORD or self.current_token.value != "var"):
            throw(InvalidForBlockInit(self.current_token.start,self.current_token.end,self.current_token.value))

        
        


        self.buildVariableDeclaration() #determine incrementor
        decl = self.declarations[len(self.declarations)-1]
        self.addline("__"+self.name+"__flp"+hex(decl.offset)+":")

        beginidx = len(self.bodytext) #anything added after this point, and before doCompilations will go at the end of the loop's asm
        
        self.appendDeclaration("__%s__flp_maxnum%s"%(self.name,hex(decl.offset)))
        maxdecl = self.declarations[len(self.declarations)-1]
        if(self.current_token.tok == ";"):
            self.advance()

        self.evaluateExpression(decl=maxdecl)
        self.addline("; FIRST")

        
        #self.evaluateExpression(decl=decl)
        print(self.current_token)
        self.buildIDStatement()
        
        self.addline("; POST EXPRESSION")
        self.advance()

        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidForBlockInit(self.current_token.start,self.current_token.end,self.current_token.value))
        self.advance()#move past {


        self.addline(load_value_toreg(maxdecl.offset,"rdi"))
        self.addline(load_value_toreg(decl.offset,"rsi"))

        self.addline("cmp rsi, rdi")
        self.addline("jl %s"%("__"+self.name+"__flp"+hex(decl.offset)))

        header = self.bodytext[beginidx:]
        self.bodytext = self.bodytext[:beginidx]
        print("PRE: "+self.current_token.__repr__())
        self.doCompilations(forblock=True)
        self.advance()
        print("POST :%s"%self.current_token)
        self.addline(header)
        
    def buildCMP(self):
        if(self.current_token.tok != T_OPENP):
            throw(InvalidCMPBlockHeader(self.current_token.start,self.current_token.end,self.current_token.value))
        
        self.advance()

        self.evaluateExpression(reg="r14")
        self.evaluateExpression(reg="r15")
        
        if(self.current_token.tok != T_OSCOPE):
            throw(InvalidCMPBlockHeader(self.current_token.start,self.current_token.end,self.current_token.value))
        endblockname = "__cmpblock__%s__%s"%(self.name,hex(len(self.bodytext)))
        self.addline("cmp r14, r15")
        self.addline("push %s"%endblockname)
        self.advance(   )
        while self.current_token.tok != None and self.current_token.tok != T_CLSCOPE:
            if(self.current_token.tok not in CMP_TOKS):
                throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))
            
            op = CMP_TABLE[self.current_token.tok]
            self.advance()
            if(self.current_token.tok != ":"):throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))
            self.advance()
            if(self.current_token.tok != T_ID):throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))
            id = self.current_token.value
            self.advance()
            if(self.current_token.tok == T_CLSCOPE):break
            if(self.current_token.tok != T_EOL):throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))
            self.addline("%s %s"%(op, id))
            self.advance()

        self.advance()
        self.addline("add rsp, 0x8")
        self.addline("%s:"%endblockname)

        if(self.current_token.tok != "->"): return
        self.advance()

        if(self.current_token.tok != T_ID):throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))

        id = self.current_token.value

        decl = self.getDeclarationByID(id)
        
        self.addline(place_value_from_reg(decl.offset,"r8"))
        
        self.advance()
        
        if(self.current_token.tok != T_EOL):throw(InvalidCMPBlockHeader(self.current_token.start, self.current_token.end, self.current_token.value))
        
        self.advance()






    def buildKeywordStatement(self):

        if(self.current_token.value == "var"):
            self.buildVariableDeclaration()
        elif(self.current_token.value == "return"):
            self.advance()
            self.buildReturnStatement()
        elif(self.current_token.value == "__asm"):
            self.advance()
            self.buildAsmBlock()
        elif(self.current_token.value == "for"):
            self.advance()
            self.buildForBlock()
        elif(self.current_token.value == "cmp"):
            self.advance()
            self.buildCMP()
        else:
            self.advance()









    def compile(self):
        allocationoffset = len(self.params)*8
        for token in self.tokens:
            if(token.tok == T_KEYWORD and token.value == "var"):
                allocationoffset += 8

        self.allocator = allocate(allocationoffset)
        for i in range(len(self.params)):
            self.appendDeclaration(self.params[i])
            self.allocator += place_value_from_reg((i+1)*8,parameter_registers[i])

            
        self.bodytext = "%s%s"%(self.allocator,self.bodytext)
        self.doCompilations()
        self.advance()
        


    def doCompilations(self, forblock=False):
        opens = 0
        while self.current_token != None and self.current_token.tok != T_EOF and self.current_token.tok != T_CLSCOPE:
            if(forblock): print(self.current_token)
            if(self.current_token.tok in T_EOL+T_OPENP+T_OSCOPE+T_CLSCOPE+T_COLON):

                self.advance()
            elif(self.current_token.tok == T_KEYWORD):
                self.buildKeywordStatement()
            elif(self.current_token.tok == T_ID):
                self.buildIDStatement()
            else:
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






