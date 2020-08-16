
%include "io64.inc"




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


