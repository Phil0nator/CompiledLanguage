from constants import *
from errors import *
from Token import *




class Struct:
    def __init__(self, name, body):
        self.name = name
        self.tokens = body

        self.current_token = self.tokens[0]
        self.ct_idx = 0
        self.allocator = "  "
        
    
    
    def compile(self):
        allocationspace = 8
        for t in self.tokens:
            if (t.tok == T_KEYWORD):
                if(t.value == "var"):
                    allocationspace+=8
        #call malloc to create enough space in memory
        self.allocator = """
%s
%s
mov rdi, %s
call malloc
add rsp, 4
test rax, rax ; check for error
mov byte[rax+%s], 0x0
mov r8, rax
leave
ret

        """%(self.name+":",allocate(8),hex(allocationspace),hex(allocationspace))
        return self.allocator    
    
    
    
    
    
    
    
    
    
    
    
    
    def advance(self):
        self.ct_idx += 1
        if self.ct_idx < len(self.tokens):
            self.current_token = self.tokens[self.ct_idx]
        else:
            self.current_token = Token(T_EOF)
    
