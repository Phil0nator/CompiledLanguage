#Tokens:

T_NUMBERS = "0123456789"
T_INT = "INT"
T_FLOAT = "FLOAT"


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




TM_ALL = "&|><=-()!"



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

KEYWORDS = ["if", "struct", "class", "while", "for", "var", "final", "function", "enum", "true", "false", "null", "nullptr", "return"]



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

scratch_reg_order = ["rdi","r10","r11","r12","r13"]


int_allocator = 32
int_allocator_ref = "DWORD"
int_allocator_glob = "resb 4"



allocator_table = {
    "int" : int_allocator,
    "g_int" : int_allocator_glob,
    "int*" : int_allocator_ref


}



def allocate(amt):
    return """
    push rbp
    mov rbp, rsp
    sub rsp, """+str(amt)+"\n"

def place_value(ptr, value):
    return """mov DWORD [rbp-"""+str(ptr)+"""], """+str(value)

def load_value_toreg(ptr,reg):
    return """
    mov %s, DWORD [rbp-%s]\n
    """%(reg,ptr)