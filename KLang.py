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

import argparse as arg

__fileinput__ = ""
__fileoutput__ = ""
__tonasm__ = False
__autorun__ = False


def main():
    
    global cc
    data = ""

    


    
    cc["DEF"] = []
    cc["GL_VAR"] = []
    cc["FILES"] = [__fileinput__]

    

    with open(__fileinput__, "rb") as f:
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
    asm = asm.replace("&&TEXT&&", compiler.main) 
    asm = asm.replace("&&BSS&&", compiler._bss)
    asm = asm.replace("&&DATA&&", compiler._data)

    

    with open("%s.asm"%__fileoutput__, "wb") as f:
        f.write(asm.encode())
    commands = updateCommands(__fileinput__, __fileoutput__)
    os.system(commands[0] + " && " + commands[1])
    os.remove(__fileoutput__+".o")

    if(not __tonasm__):
        os.remove("%s.asm"%__fileoutput__)


    if(__autorun__):
        os.system("./%s"%__fileoutput__)

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



def handleArgs():
    global __fileinput__,__fileoutput__,__tonasm__,__autorun__
    parser = arg.ArgumentParser(description='Compile .smpl programs into either nasm assembly, or directly to an executable.')
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-nasm", action="store_true", default=False)
    parser.add_argument("-r", action="store_true", default=False)
    args = parser.parse_args()
    __fileinput__=args.input
    __fileoutput__=args.output
    __tonasm__=args.nasm
    __autorun__=args.r
if( __name__ == "__main__"):
    handleArgs()

    main()
