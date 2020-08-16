
%include "io64.inc"




section .data
    


section .bss
    beans : resb 4
	joe : resb 4
	bruhman : resb 4
	


section .text
global CMAIN


main:

    push rbp
    mov rbp, rsp
    sub rsp, 32
mov DWORD [rbp-32], 36
	leave
	ret







CMAIN:
    mov rbp, rsp
    xor rax, rax
    call main

    ret


