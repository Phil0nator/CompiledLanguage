function print_char(char){
    __asm{"
    PRINT_CHAR r9
    NEWLINE
    "}
}
function print_string(string){
    __asm{"
    PRINT_STRING [r9]
    NEWLINE
    "}
}
function print_integer(number){
    __asm{"
    PRINT_DEC 4, r9
    NEWLINE
    "}
}