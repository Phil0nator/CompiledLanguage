
%ifndef IO_SYS
%define IO_SYS
%assign sasmMacroCount 0

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
CEXTERN realloc
CEXTERN calloc
CEXTERN free
CEXTERN strlen
CEXTERN strcat

; Make stack be 16 bytes aligned
%macro ALIGN_STACK 0.nolist
    enter 0, 0
    and rsp, 0xfffffffffffffff0
%endmacro

%macro UNALIGN_STACK 0.nolist
    leave
%endmacro

%macro FFLUSH_STDOUT 0.nolist
    ALIGN_STACK
    call get_stdout
    mov rdi, rax
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
    push rsi
    push rdi
    ALIGN_STACK
    call get_stdout
    mov rdi, %1
    mov rsi, rax
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
    push rsi
    push rdi
    ALIGN_STACK
    call get_stdout
    mov rdi, %%str
    mov rsi, rax
%else
; address expression
    jmp %%after_data
section .data
    %%tmp dq 0
section .text
    %%after_data:
    mov qword[%%tmp], rbx
    lea rbx, %1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    push rsi
    push rdi
    ALIGN_STACK
    call get_stdout
    mov rdi, rbx
    mov rsi, rax
    mov rbx, qword[%%tmp]
%endif
    call fputs
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop rdi
    pop rsi
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
    push rsi
    push rdi
    ALIGN_STACK
    mov rsi, rax
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
    push rsi
    push rdi
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
    mov rsi, rax
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
    push rsi
    push rdi
    mov rsi, %2
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
    push rsi
    push rdi
    mov rsi, %2
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
    push rsi
    push rdi
    ALIGN_STACK
    mov rsi, rax
%endif
    mov rdi, %%fmt
    call printf
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop rdi
    pop rsi
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
    push rsi
    push rdi
    and rax, 0xff
    mov rdi, rax
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
    push rsi
    push rdi
    movzx rax, byte [%1]
    mov rdi, rax
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
    push rsi
    push rdi
    mov rdi, %1
    and rdi, 0xff
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
    push rsi
    push rdi
    mov rdi, tstr
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
    push rsi
    push rdi
    mov rdi, rax
    ALIGN_STACK
%endif
    call putchar
    UNALIGN_STACK
    FFLUSH_STDOUT
    pop rdi
    pop rsi
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
    push rsi
    push rdi
    mov rsi, %%read_tmp
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
    push rsi
    push rdi
    mov rsi, %2
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
    push rsi
    push rdi
    ALIGN_STACK
    mov rsi, rax
%endif
    mov rdi, %%fmt
    call scanf
    UNALIGN_STACK
    pop rdi
    pop rsi
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
    push rsi
    push rdi
    mov rsi, %%read_tmp
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
    push rsi
    push rdi
    mov rsi, %1
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
    push rsi
    push rdi
    ALIGN_STACK
    mov rsi, rax
%endif
    mov rdi, %%fmt
    call scanf
    UNALIGN_STACK
    pop rdi
    pop rsi
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
    push rsi
    push rdi
    ;count
    IS_GPR %2
    %if %$is_reg = 1 
        %if %$reg_size = 1
            movzx rsi, %2
        %elif %$reg_size = 2
            movzx rsi, %2
        %elif %$reg_size = 4
            movsx rsi, %2
            pushfq
            shl rsi, 32
            shr rsi, 32
            popfq
        %else ; %$reg_size = 8
            mov rsi, %2
        %endif
    %else
        mov rsi, %2
    %endif
    %pop
    mov rdi, %1
    ALIGN_STACK
    call get_stdin
    mov rdx, rax
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
    mov qword[%%tmp], rbx
    lea rbx, %1
    pushfq
    push rax
    push rcx
    push rdx
    push r8
    push r9
    push r10
    push r11
    push rsi
    push rdi
    ;count
    IS_GPR %2
    %if %$is_reg = 1 
        %if %$reg_size = 1
            movzx rsi, %2
        %elif %$reg_size = 2
            movzx rsi, %2
        %elif %$reg_size = 4
            movsx rsi, %2
            pushfq
            shl rsi, 32
            shr rsi, 32
            popfq
        %else ; %$reg_size = 8
            mov rsi, %2
        %endif
    %else
        mov rsi, %2
    %endif
    %pop
    mov rdi, rbx
    ALIGN_STACK
    call get_stdin
    mov rdx, rax
    mov rbx, qword[%%tmp]
%endif
    call fgets
    UNALIGN_STACK
    pop rdi
    pop rsi
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
STRING_CONSTANT_1: db `The number of commandline arguments is: %u`, 0
STRING_CONSTANT_2: db ``, 0
STRING_CONSTANT_3: db `Hello World`, 0
STRING_CONSTANT_4: db `A string for testing purposes`, 0
STRING_CONSTANT_5: db `, and this has been appended.`, 0
__isincluded__MEMORY_: dd 0x8726



section .bss
bruhman: resb 0x4



section .text
global CMAIN


print_char:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx

    PRINT_CHAR r9
    NEWLINE
    


leave
ret

print_string:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx

    PRINT_STRING [r9]
    NEWLINE
    


leave
ret

print_integer:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx

    PRINT_DEC 4, r9
    NEWLINE
    


leave
ret

printformat:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx

    
    push rax
    push rcx
    mov     rdi, r9                ; set 1st parameter (format)
    mov     rsi, r10                 ; set 2nd parameter (current_number)
    xor     rax, rax                ; because printf is varargs

    ; Stack is already aligned because we pushed three 8 byte registers
    call    printf                  ; printf(format, current_number)

    pop     rcx                     ; restore caller-save register
    pop     rax                     ; restore caller-save register
    
    


leave
ret

print_two_formats:

push rbp
mov rbp, rsp
sub rsp, 0xc
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx
mov rcx, r11
mov DWORD [rbp-0xc], ecx

    
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
    
    


leave
ret

exit:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx

    
    
    mov eax, 1  ; 1 = exit system call
    mov rdi, r9 ; r9 = exit code given in parameter
    int 0x80    ; interrupt
    
    


leave
ret

Array:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov rcx, r9
mov DWORD [rbp-0x4], ecx
push r9
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call alloc
mov rcx, r8
mov DWORD [rbp-0x8], ecx

pop r9
mov ebx, DWORD [rbp-0x8]
mov r8,rbx


leave
ret

putValue:

push rbp
mov rbp, rsp
sub rsp, 0xc
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx
mov rcx, r11
mov DWORD [rbp-0xc], ecx

    mov rax, r11
    mov DWORD [r9+r10], eax  
    


leave
ret

getValue:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx

    
    mov eax, DWORD [r9+r10]
    mov r8, rax
    
    


leave
ret

strAppend:

push rbp
mov rbp, rsp
sub rsp, 0x18
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx
push r9
push r10
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call strlen
mov rcx, r8
mov DWORD [rbp-0xc], ecx

pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x8]
mov r9,rbx
call strlen
mov rcx, r8
mov DWORD [rbp-0x10], ecx

pop r10
pop r9
mov ebx, DWORD [rbp-0xc]
mov ecx, DWORD [rbp-0x10]
add ebx, ecx
mov DWORD [rbp-0x14], ebx
push r9
push r10
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
mov ebx, DWORD [rbp-0x14]
mov r10,rbx
call reallocate
mov rcx, r8
mov DWORD [rbp-0x18], ecx

pop r10
pop r9

    mov rdi, r8 ;reallocated
    mov rsi, r10;strb
    call strcat 
    sub rsp, 4
    mov r8, rax
    


leave
ret

alloc:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx


   xor r11, r11
   xor r12, r12
   mov rdi, r9
   call malloc
   xor r11, r11
   xor r12, r12
   add rsp, 4
   test rax, rax ; check for error

   mov byte[rax+r9], 0x0

   mov r8, rax





leave
ret

strcpy:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx

        
        xor r8, r8
        xor rax, rax
        _strcpy_top_loop:
        mov ax, word [r10 + r8]
        cmp ax, 0
        je _strcpy_end_loop
        mov word [r9+r8],ax
        inc r8
        jmp _strcpy_top_loop
        _strcpy_end_loop  :
    
    
    


leave
ret

strlen:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx

    
    xor r8,r8
    _strlen_top_loop:
    mov ax, word[r9+r8]
    cmp ax,0
    je _strlen_end_loop
    inc r8
    jmp _strlen_top_loop
    
    _strlen_end_loop:
    


leave
ret

memerror:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx
push r9
mov ebx, STRING_CONSTANT_0
mov r9,rbx
call print_string
pop r9
push r9
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call exit
pop r9


leave
ret

destroy:

push rbp
mov rbp, rsp
sub rsp, 0x4
mov rcx, r9
mov DWORD [rbp-0x4], ecx


    mov rdi, r9
    call free
    sub rsp, 4




leave
ret

reallocate:

push rbp
mov rbp, rsp
sub rsp, 0x8
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx

        
        mov rdi, r9
        mov rsi, r10
        call realloc
        add rsp, 4
        mov r8, rax
        
        
        


leave
ret

string:

push rbp
mov rbp, rsp
sub rsp, 0xc
mov rcx, r9
mov DWORD [rbp-0x4], ecx
push r9
mov ebx, DWORD [rbp-0x4]
mov r9,rbx
call strlen
mov rcx, r8
mov DWORD [rbp-0xc], ecx

pop r9
mov ebx, DWORD [rbp-0xc]
mov ecx, 0x1
add ebx, ecx
mov DWORD [rbp-0xc], ebx
push r9
mov ebx, DWORD [rbp-0xc]
mov r9,rbx
call Array
mov rcx, r8
mov DWORD [rbp-0x8], ecx

pop r9
push r9
mov ebx, DWORD [rbp-0x8]
mov r9,rbx
mov ebx, DWORD [rbp-0x4]
mov r10,rbx
call strcpy
pop r9
mov ebx, DWORD [rbp-0x8]
mov r8,rbx


leave
ret

m:

push rbp
mov rbp, rsp
sub rsp, 0x18
mov rcx, r9
mov DWORD [rbp-0x4], ecx
mov rcx, r10
mov DWORD [rbp-0x8], ecx
push r9
push r10
mov ebx, STRING_CONSTANT_1
mov r9,rbx
mov ebx, DWORD [rbp-0x8]
mov r10,rbx
call printformat
pop r10
pop r9
push r9
push r10
mov ebx, STRING_CONSTANT_2
mov r9,rbx
call print_string
pop r10
pop r9
mov ebx, 0x6a
mov DWORD [rbp-0xc], ebx
push r9
push r10
mov ebx, DWORD [rbp-0xc]
mov r9,rbx
call print_integer
pop r10
pop r9
mov ebx, DWORD [rbp-0xc]
mov ecx, 0x6
add ebx, ecx
mov DWORD [rbp-0xc], ebx
push r9
push r10
mov ebx, DWORD [rbp-0xc]
mov r9,rbx
call print_integer
pop r10
pop r9
push r9
push r10
mov ebx, STRING_CONSTANT_3
mov r9,rbx
call print_string
pop r10
pop r9
push r9
push r10
mov ebx, STRING_CONSTANT_4
mov r9,rbx
call string
mov rcx, r8
mov DWORD [rbp-0x10], ecx

pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x10]
mov r9,rbx
call print_string
pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x10]
mov r9,rbx
mov ebx, STRING_CONSTANT_5
mov r10,rbx
call strAppend
mov rcx, r8
mov DWORD [rbp-0x10], ecx

pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x10]
mov r9,rbx
call print_string
pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x10]
mov r9,rbx
call destroy
pop r10
pop r9
__m__flp0x18:
mov ebx, DWORD [rbp-0x18]
mov DWORD [rbp-0x14], ebx
push r9
push r10
mov ebx, DWORD [rbp-0x14]
mov r9,rbx
call print_integer
pop r10
pop r9
push r9
push r10
mov ebx, DWORD [rbp-0x14]
mov r9,rbx
call print_integer
pop r10
pop r9
mov ebx, 0xa
mov DWORD [rbp-0x1c], ebx
mov ebx, DWORD [rbp-0x18]
inc ebx
mov DWORD [rbp-0x18], ebx

mov edi, DWORD [rbp-0x1c]

    

mov esi, DWORD [rbp-0x18]

    
cmp rsi, rdi
jl __m__flp0x18



leave
ret







CMAIN:
mov rbp, rsp
xor rax, rax


mov r9, rsi     ;commandline args
mov r10, rdi
mov DWORD [bruhman], 0x64
call m
NEWLINE
ret


