
%ifndef IO_SYS
%define IO_SYS

%macro sasmMacroFunc 0.nolist ;func for debug
    %push sasmMacroFunc
    call %$sasmMacro
    jmp %$sasmMacroE
    %$sasmMacro:
    jmp %%after_data
section .data
    %$sasmRetAddr dq 0
section .text
    %%after_data:
    push rbx
    mov rbx, qword[rsp + 8]
    mov qword[%$sasmRetAddr], rbx
    mov rbx, qword[rsp]
    mov qword[rsp + 8], rbx
    pop rbx
    pop rbx
%endmacro

%macro sasmMacroFuncE 0.nolist ;exit
    push qword[%$sasmRetAddr]
    ret
    %$sasmMacroE:
    %pop
%endmacro

%macro CEXTERN 1.nolist
    extern %1
%endmacro
%define CMAIN main

CEXTERN printf
CEXTERN scanf
CEXTERN putchar
CEXTERN fgets
CEXTERN puts
CEXTERN fputs
CEXTERN fflush
CEXTERN get_stdin
CEXTERN get_stdout

CEXTERN malloc
CEXTERN free
CEXTERN realloc

; Make stack be 16 bytes aligned and reserve 32 byte space for parameters
%macro ALIGN_STACK 0.nolist
    enter 0, 0
    sub rsp, 32
    and rsp, 0xfffffffffffffff0
%endmacro

%macro UNALIGN_STACK 0.nolist
    leave
%endmacro

%macro FFLUSH_STDOUT 0.nolist
    ALIGN_STACK
    call get_stdout
    mov rcx, rax
    call fflush
    UNALIGN_STACK
%endmacro

%macro IS_GPR 1.nolist
    %push IS_GPR
    %assign %$is_reg 0
    %assign %$reg_size 1
    %ifidni %1, ah
        %assign %$is_reg 1
    %elifidni %1, al
        %assign %$is_reg 1
    %elifidni %1, bl
        %assign %$is_reg 1
    %elifidni %1, bh
        %assign %$is_reg 1
    %elifidni %1, cl
        %assign %$is_reg 1
    %elifidni %1, ch
        %assign %$is_reg 1
    %elifidni %1, dl
        %assign %$is_reg 1
    %elifidni %1, dh
        %assign %$is_reg 1
    %elifidni %1, spl
        %assign %$is_reg 1
    %elifidni %1, bpl
        %assign %$is_reg 1
    %elifidni %1, dil
        %assign %$is_reg 1
    %elifidni %1, sil
        %assign %$is_reg 1
    %elifidni %1, ax
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, bx
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, cx
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, dx
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, sp
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, bp
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, si
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, di
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, eax
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, ebx
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, ecx
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, edx
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, esp
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, ebp
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, esi
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, edi
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, rax
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rbx
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rcx
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rdx
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rsp
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rbp
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rsi
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, rdi
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r8
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r9
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r10
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r11
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r12
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r13
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r14
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r15
        %assign %$is_reg 1
        %assign %$reg_size 8
    %elifidni %1, r8d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r9d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r10d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r11d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r12d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r13d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r14d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r15d
        %assign %$is_reg 1
        %assign %$reg_size 4
    %elifidni %1, r8w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r9w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r10w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r11w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r12w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r13w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r14w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r15w
        %assign %$is_reg 1
        %assign %$reg_size 2
    %elifidni %1, r8b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r9b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r10b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r11b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r12b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r13b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r14b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %elifidni %1, r15b
        %assign %$is_reg 1
        %assign %$reg_size 1
    %endif
%endmacro

%macro PRINT_STRING 1.nolist
    sasmMacroFunc
    IS_GPR %1
    %if %$is_reg = 1
        %error "Register as parameter is not supported"
    %endif
    %pop
%ifid %1
; variable
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    call get_stdout
    mov rcx, %1
    mov rdx, rax
%elifstr %1
; string literal
    jmp %%after_str
section .data
    %%str db %1, 0
section .text
    %%after_str:
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    call get_stdout
    mov rcx, %%str
    mov rdx, rax
%else
; address expression
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rdi
    lea rdi, %1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    call get_stdout
    mov rcx, rdi
    mov rdx, rax
    mov rdi, qword[%%tmp]
%endif
    call fputs
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq
    sasmMacroFuncE
%endmacro

%macro NEWLINE 0.nolist
    PRINT_STRING `\n`
%endmacro

; size baseformatletter ("d", "u", "x") varname (%%fmt)
%macro ___MAKE_FORMAT_STR 3.nolist
    jmp %%after_fmt
    %if %1 = 1
        %strcat fmts "%hh" %2
    %elif %1 = 2
        %strcat fmts "%h" %2
    %elif %1 = 4
        %strcat fmts "%" %2
    %elif %1 = 8
        %strcat fmts "%ll" %2
    %else
        %error "Expected numeric constant 1, 2, 4 or 8 as 1st argument"
    %endif
    %3 db fmts, 0
    %%after_fmt:
%endmacro

; size data baseformatletter ("d", "u", "x") signextendinst (movzx, movsx)
%macro ___PRINT_NUM_COMMON 4.nolist
    ___MAKE_FORMAT_STR %1, %3, %%fmt
    IS_GPR %2
%if %$is_reg = 1
; register
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rax    
    %if %$reg_size = 1
        %4 rax, %2
    %elif %$reg_size = 2
        %4 rax, %2
    %elif %$reg_size = 4
        movsx rax, %2
        %ifidni %4, movzx
            pushfq
            shl rax, 32
            shr rax, 32
            popfq
        %endif
    %else ; %$reg_size = 8
        mov rax, %2
    %endif
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    mov rdx, rax
%elifid %2
; variable (hope so)
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    %if %1 = 1
        %4 rax, byte [%2]
    %elif %1 = 2
        %4 rax, word [%2]
    %elif %1 = 4
        movsx rax, dword [%2]
        %ifidni %4, movzx
            pushfq
            shl rax, 32
            shr rax, 32
            popfq
        %endif
    %else ; %1 = 8
        mov rax, qword [%2]
    %endif
    mov rdx, rax
    ALIGN_STACK
%elifnum %2
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %2
    ALIGN_STACK
%elifstr %2
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %2
    ALIGN_STACK
%else
; may be, address expression?
jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rax
    %if %1 = 1
        %4 rax, byte %2
    %elif %1 = 2
        %4 rax, word %2
    %elif %1 = 4
        movsx rax, dword %2
        %ifidni %4, movzx
            pushfq
            shl rax, 32
            shr rax, 32
            popfq
        %endif
    %else ; %1 = 8
        mov rax, qword %2
    %endif
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    mov rdx, rax
%endif
    mov rcx, %%fmt
    call printf
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq 
    %pop ; IS_REG    
%endmacro

%macro PRINT_DEC 2.nolist
    sasmMacroFunc
    ___PRINT_NUM_COMMON %1, %2, "d", movsx
    sasmMacroFuncE
%endmacro

%macro PRINT_UDEC 2.nolist
    sasmMacroFunc
    ___PRINT_NUM_COMMON %1, %2, "u", movzx
    sasmMacroFuncE
%endmacro

%macro PRINT_HEX 2.nolist
    sasmMacroFunc
    ___PRINT_NUM_COMMON %1, %2, "x", movzx
    sasmMacroFuncE
%endmacro

%macro PRINT_CHAR 1.nolist
    sasmMacroFunc
    IS_GPR %1
%if %$is_reg = 1
; register
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rax    
    %if %$reg_size = 1
        movzx rax, %1
    %elif %$reg_size = 2
        movzx rax, %1
    %elif %$reg_size = 4
        movsx rax, %1
        pushfq
        shl rax, 32
        shr rax, 32
        popfq
    %else ; %$reg_size = 8
        mov rax, %1
    %endif
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    and rax, 0xff
    mov rcx, rax
    ALIGN_STACK
%elifid %1
; variable (hope so)
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    movzx rax, byte [%1]
    mov rcx, rax
    ALIGN_STACK
%elifnum %1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rcx, %1
    and rcx, 0xff
    ALIGN_STACK
%elifstr %1
; string select only 1st byte
%substr tstr %1 1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rcx, tstr
    ALIGN_STACK
%else
; may be, address expression?
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rax
    movzx rax, byte %1
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rcx, rax
    ALIGN_STACK
%endif
    call putchar
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq
    %pop ; IS_REG
    sasmMacroFuncE
%endmacro


; size data baseformatletter ("d", "u", "x") signextendinst (movzx, movsx)
%macro ___GET_NUM_COMMON 4.nolist
    ___MAKE_FORMAT_STR %1, %3, %%fmt        
    jmp %%after_data
section .data
    %%read_tmp dq 0
    %%tmp dq 0
section .text
    %%after_data:
    IS_GPR %2
%if %$is_reg = 1
; register
    %ifidni %2, rsp
        %error "Won't read to rsp!" 
    %elifidni %2, esp
        %error "Won't read to esp!" 
    %elifidni %2, sp
        %error "Won't read to sp!"
    %elifidni %2, spl
        %error "Won't read to sp!" 
    %endif
    %if %$reg_size < %1
        %error "Too small register for requested data"
    %endif
; we will have to do postprocessing after scanf
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %%read_tmp
    ALIGN_STACK
%elifid %2
; variable (hope so)
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %2
    ALIGN_STACK
%elifnum %2
    %error "Incorrect parameter (number)"
%elifstr %2
    %error "Incorrect parameter (string)"
%else
; may be, address expression?
    mov qword[%%tmp], rax
    lea rax, %2
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    mov rdx, rax
%endif
    mov rcx, %%fmt
    call scanf
    UNALIGN_STACK
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq
%if %$is_reg = 1
    ; register postprocessing
    %if %$reg_size = %1
        mov %2, [%%read_tmp]
    %else ; extend bytes 1 -> 2, 1 -> 4, 1 -> 8, 2 -> 4, 2 -> 8, 4 -> 8
        %if %1 = 1
            %4 %2, byte [%%read_tmp]
        %elif %1 = 2
            %4 %2, word [%%read_tmp]
        %else ; 4
            movsx %2, dword [%%read_tmp]
            %ifidni %4, movzx
                pushfq
                shl %2, 32
                shr %2, 32
                popfq
            %endif
        %endif
    %endif
%endif
    %pop ; IS_REG
%endmacro

%macro GET_HEX 2.nolist
    sasmMacroFunc
    ___GET_NUM_COMMON %1, %2, "x", movzx
    sasmMacroFuncE
%endmacro

%macro GET_DEC 2.nolist
    sasmMacroFunc
    ___GET_NUM_COMMON %1, %2, "d", movsx
    sasmMacroFuncE
%endmacro

%macro GET_UDEC 2.nolist
    sasmMacroFunc
    ___GET_NUM_COMMON %1, %2, "u", movzx
    sasmMacroFuncE
%endmacro


%macro GET_CHAR 1.nolist
    sasmMacroFunc
    jmp %%after_data
section .data
    %%fmt db "%c", 0
    %%read_tmp db 0
    %%tmp dq 0
section .text
%%after_data:
    IS_GPR %1
%if %$is_reg = 1
; register
    %ifidni %1, rsp
        %error "Won't read to rsp!" 
    %elifidni %1, esp
        %error "Won't read to esp!" 
    %elifidni %1, sp
        %error "Won't read to sp!" 
    %elifidni %1, spl
        %error "Won't read to spl!" 
    %endif
; we will have to do postprocessing after scanf
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %%read_tmp
    ALIGN_STACK
%elifid %1
; variable (hope so)
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    mov rdx, %1
    ALIGN_STACK    
%elifnum %1
    %error "Incorrect parameter (number)"
%elifstr %1
    %error "Incorrect parameter (string)"
%else
; may be, address expression?
    mov qword[%%tmp], rax
    lea rax, %1
    pushfq
    push qword[%%tmp] ;rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ALIGN_STACK
    mov rdx, rax
%endif
    mov rcx, %%fmt
    call scanf
    UNALIGN_STACK
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq
%if %$is_reg = 1
    ; register postprocessing
    %if %$reg_size = 1
        mov %1, byte [%%read_tmp]
    %else ; zero extend bytes 1 -> 2, 1 -> 4, 1 -> 8
        movzx %1, byte [%%read_tmp]
    %endif
%endif
    %pop ; IS_REG
    sasmMacroFuncE
%endmacro

%macro GET_STRING 2.nolist
    sasmMacroFunc
    IS_GPR %1
    %if %$is_reg = 1
        %error "Incorrect 1st parameter (register)"
    %endif    
    %pop ;IS_GPR
    IS_GPR %2    
    %if %$is_reg = 1
        ;
    %elifnum %2
        %if %2 <= 0
            %error "Second parameter must be positive"
        %endif
    %else
        %error "Second parameter must be numeric constant or register"
    %endif
    %pop ;IS_GPR
%ifid %1
; variable (hope so)
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ;count
    IS_GPR %2
    %if %$is_reg = 1 
        %if %$reg_size = 1
            movzx rdx, %2
        %elif %$reg_size = 2
            movzx rdx, %2
        %elif %$reg_size = 4
            movsx rdx, %2
            pushfq
            shl rdx, 32
            shr rdx, 32
            popfq
        %else ; %$reg_size = 8
            mov rdx, %2
        %endif
    %else
        mov rdx, %2
    %endif
    %pop
    mov rcx, %1
    ALIGN_STACK
    call get_stdin
    mov r8, rax
%elifnum %1
    %error "Incorrect 1st parameter (number)"
%elifstr %1
    %error "Incorrect 1st parameter (string)"
%else
; may be, address expression?
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
%%after_data:
    mov qword[%%tmp], rdi
    lea rdi, %1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    ;count
    IS_GPR %2
    %if %$is_reg = 1 
        %if %$reg_size = 1
            movzx rdx, %2
        %elif %$reg_size = 2
            movzx rdx, %2
        %elif %$reg_size = 4
            movsx rdx, %2
            pushfq
            shl rdx, 32
            shr rdx, 32
            popfq
        %else ; %$reg_size = 8
            mov rdx, %2
        %endif
    %else
        mov rdx, %2
    %endif
    %pop
    mov rcx, rdi
    ALIGN_STACK
    call get_stdin
    mov r8, rax
    mov rdi, qword[%%tmp]
%endif
    call fgets
    UNALIGN_STACK
    pop r11
    pop r10
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rax
    popfq
    sasmMacroFuncE
%endmacro
%endif


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;
;PROGRAM START
;
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


section .data
STRING_CONSTANT_0: db `Memory error encountered`, 0
STRING_CONSTANT_1: db `%g`, 0
STRING_CONSTANT_2: db `True`, 0
STRING_CONSTANT_3: db `False`, 0
STRING_CONSTANT_4: db `\n`, 0
STRING_CONSTANT_5: db `Hello World!`, 0
__FLT_STANDARD_1: dq __float32__(1.0)
__BOOL_STANDARD_TRUE: dq -0x1
__BOOL_STANDARD_FALSE: dq 0x0
__isincluded__MEMORY_: dq 0x96c6
__PRINTFFLOAT: db `%g`, 0
__PRINTTRUE: db `True`, 0
__PRINTFALSE: db `False`, 0
endl: db `\n`, 0
FLT_STANDARD_ZERO: dq __float32__(0.0)
isFloat: dq 0x1



section .bss
__expstack_int0: resb 0x8
__expstack_flt0: resb 0x8
__expstack_int1: resb 0x8
__expstack_flt1: resb 0x8
__expstack_int2: resb 0x8
__expstack_flt2: resb 0x8
__expstack_int3: resb 0x8
__expstack_flt3: resb 0x8
__expstack_int4: resb 0x8
__expstack_flt4: resb 0x8
__expstack_int5: resb 0x8
__expstack_flt5: resb 0x8
__expstack_int6: resb 0x8
__expstack_flt6: resb 0x8
__expstack_int7: resb 0x8
__expstack_flt7: resb 0x8
__expstack_int8: resb 0x8
__expstack_flt8: resb 0x8
__expstack_int9: resb 0x8
__expstack_flt9: resb 0x8
__expstack_int10: resb 0x8
__expstack_flt10: resb 0x8
__expstack_int11: resb 0x8
__expstack_flt11: resb 0x8
__expstack_int12: resb 0x8
__expstack_flt12: resb 0x8
__expstack_int13: resb 0x8
__expstack_flt13: resb 0x8
__expstack_int14: resb 0x8
__expstack_flt14: resb 0x8
__expstack_int15: resb 0x8
__expstack_flt15: resb 0x8
__expstack_int16: resb 0x8
__expstack_flt16: resb 0x8
__expstack_int17: resb 0x8
__expstack_flt17: resb 0x8
__expstack_int18: resb 0x8
__expstack_flt18: resb 0x8
__expstack_int19: resb 0x8
__expstack_flt19: resb 0x8
__expstack_int20: resb 0x8
__expstack_flt20: resb 0x8
__expstack_int21: resb 0x8
__expstack_flt21: resb 0x8
__expstack_int22: resb 0x8
__expstack_flt22: resb 0x8
__expstack_int23: resb 0x8
__expstack_flt23: resb 0x8
__expstack_int24: resb 0x8
__expstack_flt24: resb 0x8
__expstack_int25: resb 0x8
__expstack_flt25: resb 0x8
__expstack_int26: resb 0x8
__expstack_flt26: resb 0x8
__expstack_int27: resb 0x8
__expstack_flt27: resb 0x8
__expstack_int28: resb 0x8
__expstack_flt28: resb 0x8
__expstack_int29: resb 0x8
__expstack_flt29: resb 0x8
__expstack_int30: resb 0x8
__expstack_flt30: resb 0x8
__expstack_int31: resb 0x8
__expstack_flt31: resb 0x8
bruhman: resb 0x8



section .text
global CMAIN


exit:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
    
    mov rax, 1  ; 1 = exit system call
    mov rdi, r9 ; r9 = exit code given in parameter
    int 0x80    ; interrupt
    
    

__exit__leave_ret_:
leave
ret

doInterrupt:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
        mov rax, r9;
        mov rdi, r10;
        int 0x80
        mov r8, rax

    

__doInterrupt__leave_ret_:
leave
ret

Array:

push rbp
mov rbp, rsp
sub rsp, 0x18
mov QWORD [rbp-0x8], r9
mov QWORD [rbp-0x10], 0x0

mov rax, QWORD [rbp-0x8]
mov rcx, 0x8
imul rcx
mov r9,rax
call alloc
mov QWORD [rbp-0x10], r8

mov r8, QWORD [rbp-0x10]
cvtsi2ss xmm8,r8
jmp __Array__leave_ret_

__Array__leave_ret_:
leave
ret

putValue:

push rbp
mov rbp, rsp
sub rsp, 0x8

    mov rax, r11
    mov QWORD [r9+r10], rax  
    

__putValue__leave_ret_:
leave
ret

getValue:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
    mov rax, QWORD [r9+r10]
    mov r8, rax
    
    

__getValue__leave_ret_:
leave
ret

alloc:

push rbp
mov rbp, rsp
sub rsp, 0x8

   ALIGN_STACK
   xor r11, r11
   xor r12, r12
   mov rdi, r9
   call malloc
   xor r11, r11
   xor r12, r12
   test rax, rax ; check for error

   mov byte[rax+rdi], 0x0

   mov r8, rax
   UNALIGN_STACK



__alloc__leave_ret_:
leave
ret

memerror:

push rbp
mov rbp, rsp
sub rsp, 0x10
mov QWORD [rbp-0x8], r9
mov r9, STRING_CONSTANT_0
call print_string
mov r9, QWORD [rbp-0x8]
call exit

__memerror__leave_ret_:
leave
ret

destroy:

push rbp
mov rbp, rsp
sub rsp, 0x8

    ALIGN_STACK
    mov rdi, r9
    
    call free
    xor r10, r10
    xor r11, r11 ;gc
    xor r12, r12
    UNALIGN_STACK



__destroy__leave_ret_:
leave
ret

reallocate:

push rbp
mov rbp, rsp
sub rsp, 0x8

        
        ALIGN_STACK
        mov rdi, r9
        mov rsi, r10
        xor r10, r10
        xor r11, r11 ;gc
        xor r12, r12
        call realloc

        test rax, rax
        xor r10, r10
        xor r11, r11 ;gc
        xor r12, r12
        mov r8, rax
        UNALIGN_STACK
        
        

__reallocate__leave_ret_:
leave
ret

print_bool:

push rbp
mov rbp, rsp
sub rsp, 0x8

    cmp r9, -1
    je __pb_istrue
    PRINT_STRING __PRINTFALSE
    leave
    ret
    __pb_istrue:
    PRINT_STRING __PRINTTRUE
    leave
    ret

    

__print_bool__leave_ret_:
leave
ret

print_char:

push rbp
mov rbp, rsp
sub rsp, 0x8

    PRINT_CHAR r9
    NEWLINE
    

__print_char__leave_ret_:
leave
ret

print_string:

push rbp
mov rbp, rsp
sub rsp, 0x8

    PRINT_STRING [r9]
    NEWLINE
    

__print_string__leave_ret_:
leave
ret

print_integer:

push rbp
mov rbp, rsp
sub rsp, 0x8

    PRINT_DEC 8, r9
    NEWLINE
    

__print_integer__leave_ret_:
leave
ret

print_uint:

push rbp
mov rbp, rsp
sub rsp, 0x8

    PRINT_UDEC 8, r9
    NEWLINE
    

__print_uint__leave_ret_:
leave
ret

printformat:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
    ALIGN_STACK
    mov     rdi, r9                ; set 1st parameter (format)
    mov     rsi, r10                 ; set 2nd parameter (current_number)
    xor     rax, rax                ; because printf is varargs

    ; Stack is already aligned because we pushed three 8 byte registers
    call    printf                  ; printf(format, current_number)

    UNALIGN_STACK                    
    FFLUSH_STDOUT
    

__printformat__leave_ret_:
leave
ret

print_two_formats:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
    push rax
    push rcx
    mov     rdi, r9                ; set 1st parameter (value)
    mov     rsi, r10                 ; set 2nd parameter (fa)
    mov     rdx, r11                ; set 3rd parameter (fb)
    xor     rax, rax                ; because printf is varargs

    ; Stack is already aligned because we pushed three 8 byte registers
    call    printf                  ; printf(format, current_number)

    pop     rcx                     ; restore caller-save register
    pop     rax                     ; restore caller-save register
    FFLUSH_STDOUT
    

__print_two_formats__leave_ret_:
leave
ret

print_three_formats:

push rbp
mov rbp, rsp
sub rsp, 0x8

    
    push rax
    push rcx
    mov     rdi, r9                ; set 1st parameter (value)
    mov     rsi, r10                 ; set 2nd parameter (fa)
    mov     rdx, r11                ; set 3rd parameter (fb)
    mov     rcx, r12
    xor     rax, rax                ; because printf is varargs

    ; Stack is already aligned because we pushed three 8 byte registers
    call    printf                  ; printf(format, current_number)

    pop     rcx                     ; restore caller-save register
    pop     rax                     ; restore caller-save register
    FFLUSH_STDOUT
    

__print_three_formats__leave_ret_:
leave
ret

print_formatfloat:

push rbp
mov rbp, rsp
sub rsp, 0x10
mov QWORD [rbp-0x8], 0x0


    ALIGN_STACK
    mov     rdi, r9                ; set 1st parameter (format)
    cvtps2pd xmm0, xmm1
    mov rax, 1

    call    printf                  ; printf(format, current_number)

    FFLUSH_STDOUT
    ;add rsp, 12
    UNALIGN_STACK
    

__print_formatfloat__leave_ret_:
leave
ret

print_floatln:

push rbp
mov rbp, rsp
sub rsp, 0x10
mov QWORD [rbp-0x8], 0x0




        ALIGN_STACK
        mov     rdi, __PRINTFFLOAT                ; set 1st parameter (format)
        cvtps2pd xmm0, xmm0
        mov rax, 1

        call    printf                  ; printf(format, current_number)

        NEWLINE
        ;add rsp, 12
        UNALIGN_STACK

    

__print_floatln__leave_ret_:
leave
ret

print_float:

push rbp
mov rbp, rsp
sub rsp, 0x10
mov QWORD [rbp-0x8], 0x0



        ALIGN_STACK
        mov     rdi, __PRINTFFLOAT                ; set 1st parameter (format)
        cvtps2pd xmm0, xmm0
        mov rax, 1

        call    printf                  ; printf(format, current_number)

        FFLUSH_STDOUT
        ;add rsp, 12
        UNALIGN_STACK
    

__print_float__leave_ret_:
leave
ret

newline:

push rbp
mov rbp, rsp
sub rsp, 0x8

    NEWLINE
    

__newline__leave_ret_:
leave
ret

m:

push rbp
mov rbp, rsp
sub rsp, 0x20
mov QWORD [rbp-0x8], r9
mov QWORD [rbp-0x10], r10
mov rbx, 0x0
mov QWORD [rbp-0x18], rbx
mov r9, STRING_CONSTANT_5
mov r10, 0x0
call printformat

__m__leave_ret_:
leave
ret







CMAIN:
mov rbp, rsp
xor rax, rax


mov r9, rsi     ;commandline args
mov r10, rdi
align 16
mov QWORD [bruhman], 0x64
call m
NEWLINE
ret

