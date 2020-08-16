import os
import sys
from preprocessor import *
from constants import *



#global variables are defined in the .bss section of the assembly
def handle_globals(data,cc,_bss):
    lines = isolate_global(data.replace("\n",""))
    print(lines)
    for i in range(len(lines)):
        line = lines[i]
        allocator = line.split(" ")[0]
        allocate_space = allocator_table["g_"+allocator]
        name = line.split(" ")[1]
        _bss+=name+" : "+allocate_space+"\n\t"
    return _bss





#function used to isolate lines describing global variables
def isolate_global(data):
    out = []
    lines = data.split(";")
    for line in lines:
        if("{" in line):
            break
        out.append(line)
    return out




def main(file_to_compile):
    

    data = ""
    
    asm = ""+top_stub
    _data = ""
    _text = ""
    _bss = ""



    cc = {}
    cc["DEF"] = {}
    cc["GL_VAR"] = []
    

    with open(file_to_compile, "rb") as f:
        data = f.read().decode()

    data = pre_process(data,cc)
    _bss = handle_globals(data,cc,_bss)
    asm = asm.replace("&&BSS&&",_bss)







    with open("out.asm", "wb") as f:
        f.write(asm.encode())
    
if( __name__ == "__main__"):
    main(sys.argv[1])
