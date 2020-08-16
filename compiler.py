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

def function(ret, name, params, body):
    return {"ret":ret,"name":name,"params":params,"body":body}

def isolate_functions(data,cc):
    iso = data.split("){")
    lines = data.split(";")
    out = []
    for line in lines:
        if( "){" in line):
            header = line
            line = line.strip()
            ret = line.split(" ")[0]
            name = line.split(" ")[1][0:line.split(" ")[1].find("(")]
            params = line[line.find("("):line.find(")")].split(",")
            dfstart = data.find(line)
            body = data[dfstart:data.find("}",dfstart)]
            out.append( function(ret,name,params,body) )

    return out



def parse_function(f):
    out = f["name"]+":\n"
    body = f["body"]
    body = body.split("{")[1]
    body = body.strip()
    lines = body.split(";")
    

    variables = {}

    allocation_size = 0
    post_alloc =""
    for i in range(len(lines)):
        line = lines[i]
        if(line.startswith("int")):
            allocation_size+=allocator_table["int"]
            variables[line.split(" ")[1]] = (i+1)*allocator_table["int"]
        elif("=" in line):
            for var in variables:
                if var in line:
                    post_alloc+=place_value(variables[var], line.split(" = ")[1])
    
    out+=allocate(allocation_size)+"\n"
    out+=post_alloc
    out+="\n\tleave\n\tret"



    return out



def main(file_to_compile):
    

    data = ""
    functions = []

    asm = ""+top_stub
    _data = ""
    _text = "call main"
    _bss = ""
    _fdef = ""


    cc = {}
    cc["DEF"] = {}
    cc["GL_VAR"] = []
    

    with open(file_to_compile, "rb") as f:
        data = f.read().decode()

    data = pre_process(data,cc)
    _bss = handle_globals(data,cc,_bss)
    asm = asm.replace("&&BSS&&",_bss)
    asm = asm.replace("&&DATA&&","")

    functions = isolate_functions(data,cc)
    print(functions)

    for function in functions:
        _fdef+=parse_function(function)+"\n\n"

    asm = asm.replace("&&FDEF&&", _fdef)

    asm = asm.replace("&&TEXT&&", _text)


    with open("out.asm", "wb") as f:
        f.write(asm.encode())
    
if( __name__ == "__main__"):
    main(sys.argv[1])
