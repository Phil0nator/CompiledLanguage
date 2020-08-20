#include <stdio.h>
#include <unistd.h>
#include <memory.h>
FILE *get_stdin(void) { return stdin; }
FILE *get_stdout(void) { return stdout; }

