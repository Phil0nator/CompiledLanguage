
%include "io64.inc"




section .data
    &&DATA&&


section .bss
    beans : resb 4
	joe : resb 4
	bruhman : resb 4
	


section .text
global CMAIN
CMAIN:
    mov rbp, rsp
    xor rax, rax
    &&TEXT&&


