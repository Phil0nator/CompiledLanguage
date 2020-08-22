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
T_EQUALS = "="

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




TM_ALL = "%&|><=-!+/"
CMP_TOKS = ["==","!=",">=", "<=", "<", ">"]
CMP_TABLE = {
    "==" : "je",
    "!=" : "jne",
    ">=" : "jge",
    "<=" : "jle",
    "<"  : "jl",
    ">"  : "jg"
}

#ID
ID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_."



#ESCAPE


ESCAPE_CHARS = {

    "n":"\\n",
    "t":"\\t",
    "\"":" \\\" ",
    "\\":"\\"



}

#Keywords

KEYWORDS = ["if", "struct", "class", "while", "for", "var", "final", "function", "true", "false", \
            "null", "nullptr", "return", "new", "__asm", "__c", "#include", "#define", "#ifdef", "#ifndef", "#else", "#endif", \
            "constructor", "cmp", "float"]



top_stub = """
&&IO64&&

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;
;PROGRAM START
;
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


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


mov r9, rsi     ;commandline args
mov r10, rdi
&&TEXT&&
NEWLINE
ret


"""


C_ASSEMBLE_LINK_RUN = "nasm -felf64 out.asm && gcc \"include/macro.c\" -Wimplicit-function-declaration out.o -no-pie  && ./a.out"
C_ASSEMBLE = "nasm -felf64 out.asm"

C_LINK = "gcc \"include/macro.c\" -Wimplicit-function-declaration out.o -no-pie -o **OUT**"


def updateCommands(inp,outp):
    global C_ASSEMBLE, C_LINK
    C_ASSEMBLE = C_ASSEMBLE.replace("out.asm","%s.asm"%outp)
    
    C_LINK = C_LINK.replace("out.o","\""+outp+".o"+"\"").replace("**OUT**",outp)

    return [C_ASSEMBLE, C_LINK, "./%s"%"\""+outp+".o"+"\""]
with open("include/io64.inc", "rb") as f:
    top_stub =top_stub.replace("&&IO64&&",f.read().decode())




parameter_registers = ["r9","r10","r11","r12","r13","r14","r15"]
return_register = "r8"

int_allocator = 32
int_allocator_ref = "QWORD"
int_allocator_glob = "resb 8"



allocator_table = {
    "int" : int_allocator,
    "g_int" : int_allocator_glob,
    "int*" : int_allocator_ref


}
def define_global(name):
    return name+": resb 0x8\n"

def value_of_global(name, comp):
    if(comp.globalIsString(name)):
        return name
    return "["+name+"]"


def allocate(amt):
    return """
push rbp
mov rbp, rsp
sub rsp, """+hex(amt)+"\n"

def place_value(ptr, value):
    return """mov QWORD [rbp-"""+hex(ptr)+"""], """+hex(value)

def place_value_from_reg(ptr, reg):
    if(reg.startswith("e")):
        return """mov QWORD [rbp-"""+hex(ptr)+"""], %s\n"""%reg
    return ("""mov rcx, %s"""%reg)+"\nmov QWORD [rbp-"+hex(ptr)+"], rcx\n"

def load_value_toreg(ptr,reg):
    return """
mov %s, QWORD [rbp-%s]\n
    """%(reg,hex(ptr))

def correct_mov(regdest, regsource):
    return "mov %s,%s"%(regdest,regsource)

