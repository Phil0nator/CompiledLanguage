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
    sub rsp, """+str(amt)

def place_value(ptr, value):
    return """mov DWORD [rbp-"""+str(ptr)+"""], """+str(value)