
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
mov ebx, DWORD [rbp-0x4]
mov rcx, r9
add ebx, ecx
mov DWORD [rbp-0x4], ebx

mov ecx, DWORD [rbp-0x4]

    
mov r8, rcx


leave
ret

nothingfunction:

push rbp
mov rbp, rsp
sub rsp, 0x8


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


leave
ret







CMAIN:
mov rbp, rsp
xor rax, rax
mov DWORD [__beans], 0x20
mov DWORD [bruhman], 0x64
call m

ret


