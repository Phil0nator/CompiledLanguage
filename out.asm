
%include "io64.inc"




section .data
joe: db 0xc


section .bss
__beans: resb 0x4
bruhman: resb 0x4



section .text
global CMAIN


bigfunc:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov ebx, 0x24
mov DWORD [rbp-0x4], ebx
mov ebx, 0x24
mov ecx, 0x24
sub ebx, ecx
mov rdi,rbx
mov rax,r9
mov ebx, eax
mov rcx, rdi
sub ebx, ecx
mov rdi,rbx
mov ebx, DWORD [rbp-0x4]
mov rcx, rdi
add ebx, ecx
mov DWORD [rbp-0x4], ebx

mov ecx, DWORD [rbp-0x4]

    
mov r8, rcx
PRINT_DEC 4, r8

leave
ret

nothingfunction:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov ebx, 0x0
mov DWORD [rbp-0x4], ebx
mov ebx, [joe]
mov DWORD [rbp-0x8], ebx


leave
ret

getNumber:

push rbp
mov rbp, rsp
sub rsp, 0x0
mov r8,0x24


leave
ret

m:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov ebx, 0x1
mov DWORD [rbp-0x4], ebx
mov r9, 24
call bigfunc

leave
ret







CMAIN:
mov rbp, rsp
xor rax, rax
mov DWORD [__beans], 0x20
mov DWORD [bruhman], 0x64
call m

ret


