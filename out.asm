
%include "io64.inc"




section .data
STRING_CONSTANT_0: db "Hello World", 0



section .bss
bruhman: resb 0x4



section .text
global CMAIN


print_char:

push rbp
mov rbp, rsp
sub rsp, 0x0

    PRINT_CHAR r9
    NEWLINE
    


leave
ret

print_string:

push rbp
mov rbp, rsp
sub rsp, 0x0

    PRINT_STRING [r9]
    NEWLINE
    


leave
ret

print_integer:

push rbp
mov rbp, rsp
sub rsp, 0x0

    PRINT_DEC 4, r9
    NEWLINE
    


leave
ret

m:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov ebx, 0x6a
mov DWORD [rbp-0x4], ebx
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call print_integer
mov ebx, DWORD [rbp-0x4]
mov ecx, 0x6
add ebx, ecx
mov DWORD [rbp-0x4], ebx
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call print_integer
mov ebx, STRING_CONSTANT_0
mov r9,rbx
call print_string


leave
ret







CMAIN:
mov rbp, rsp
xor rax, rax
mov DWORD [bruhman], 0x64
call m

ret


