import os
import sys
from preprocessor import *
from constants import *
import time

from errors import *

from Location import *

from Token import *

from Lexer import *

from Declaration import *

from Function import *

from Compiler import *




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
    
    #print(tokens)

    compiler = Compiler(tokens)
    compiler.fill_info()

    asm = top_stub
    asm = asm.replace("&&FDEF&&", compiler._fdef)
    asm = asm.replace("&&TEXT&&", compiler.main) #m replaces the actual main function for naming purposes
    asm = asm.replace("&&BSS&&", compiler._bss)
    asm = asm.replace("&&DATA&&", compiler._data)

    

    with open("out.asm", "wb") as f:
        f.write(asm.encode())
        print(asm)

    ############################################
    # All tokens -> global variables
    #       define global vars in bss, finals in .data
    # Remaining tokens -> functions
    #    for each function:
    #       
    #       determine the total allocation space for function
    #       
    #       lines that start with keyword
    #           if: cmp
    #           var: allocator
    #           while: cmp
    #           for: cmp
    #           call: fn
    #           label: name
    #           jump: label
    #
    #       lines that start with id
    #           
    #           variable assignment
    #
    #
    #       Expressions:    
    #
    #           Only two term expressions allowed (excluding function calls)
    #
    #       return:
    #           value returned by the function will be pushed
    #
    #       Function parameters will be passed through : r9-r15. 
    #           Before calling these will be pushed, and after they will be poped
    #       Functions using a return value will return to the register: r8
    #
    #
    #
    #############################################

    
    

    
    
if( __name__ == "__main__"):
    main(sys.argv[1])
