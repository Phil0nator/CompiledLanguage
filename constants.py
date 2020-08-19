#Tokens:

T_NUMBERS = "0123456789"
T_INT = "INT"
T_FLOAT = "FLOAT"
T_BOOLEAN = "BOOL"

T_PLUS = "+"
T_MINUS = "-"
T_MUL = "*"
T_DIV = "/"
T_NOT = "!"
T_AMPERSAND = "&"
T_PIPE = "|"
T_LT = "<"
T_GT = ">"
T_OPENP = "("#(
T_CLOSEP = ")"#)
T_OSCOPE = "{" #{
T_CLSCOPE = "}" #}
T_EXPRESSION = "EXPRESSION"
T_OPENLINDEX = "["
T_CLSLINDEX = "]"
T_ID = "ID"
T_ALLOC = "ALLOCATOR"
T_CONSTVAR  ="CONST"
T_VAR = "VAR"
T_COMMA = ","
T_STRING = "STR"
T_KEYWORD = "KEYWORD"
T_EOF = "EOF"
T_COLON = ":"
T_EOL = "EOL"

#MULTICHAR

TM_AND = "&&"
TM_OR = "||"
TM_LE = "<="
TM_GE = ">="
TM_LBITSHIFT = "<<"
TM_RBITSHIFT = ">>"
TM_PTRVAL = "->"
TM_PLUSEQ = "+="
TM_PP = "++"




TM_ALL = "&|><=-!"



#ID
ID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"



#ESCAPE


ESCAPE_CHARS = {

    "n":"\n",
    "t":"\t",
    "\"":"\"",
    "\\":"\\"



}

#Keywords

KEYWORDS = ["if", "struct", "class", "while", "for", "var", "final", "function", "true", "false", "null", "nullptr", "return", "new", "__asm", "__c"]



top_stub = """
"""+"""%"""+"""include "io64.inc"




section .data
&&DATA&&


section .bss
&&BSS&&


section .text
global CMAIN


&&FDEF&&





CMAIN:
mov rbp, rsp
xor rax, rax
&&TEXT&&

ret


"""

parameter_registers = ["r9","r10","r11"]
return_register = "r8"

int_allocator = 32
int_allocator_ref = "DWORD"
int_allocator_glob = "resb 4"



allocator_table = {
    "int" : int_allocator,
    "g_int" : int_allocator_glob,
    "int*" : int_allocator_ref


}
def define_global(name):
    return name+": resb 0x4\n"

def value_of_global(name):
    return "["+name+"]"

def allocate(amt):
    return """
push rbp
mov rbp, rsp
sub rsp, """+hex(amt)+"\n"

def place_value(ptr, value):
    return """mov DWORD [rbp-"""+hex(ptr)+"""], """+hex(value)

def place_value_from_reg(ptr, reg):
    if(reg.startswith("e")):
        return """mov DWORD [rbp-"""+hex(ptr)+"""], %s"""%reg
    return ("""mov rcx, %s"""%reg)+"\nmov DWORD [rbp-"+hex(ptr)+"], ecx"

def load_value_toreg(ptr,reg):
    return """
mov %s, DWORD [rbp-%s]\n
    """%(reg,hex(ptr))

def correct_mov(regdest, regsource):
    if(regdest.startswith("e") and regsource.startswith("e")):
        return "mov %s,%s"%(regdest,regsource)
    if(regdest.startswith("e") and regsource.startswith("r")):
        if(regsource[1] in "189"):
            return "mov rcx, %s \nmov %s, ecx"%(regsource, regdest)
        else:
            return "mov %s,%s"%(regdest,regsource.replace("r","e"))
    
    if(regdest.startswith("r") and regsource.startswith("e")):
        return "mov %s,%s"%(regdest, regsource.replace("e","r") )
    
    
    return "mov %s,%s"%(regdest,regdest)

