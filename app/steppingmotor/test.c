#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXCHAR 256
#define MAXCOM 16

void getargs(int *argc, char **argv, char *buf)
{
    int n = 0;
    int charcnt = 0;
    *argc = 0;
    char c;
    int prev = 1;
    do {
        c = buf[n];
        if (n == MAXCHAR - 1) {
            break;
        }
        if (c == EOF) {
            printf("\n");
            exit(0);
        }
        if (*argc > MAXCOM - 2) {
            break;
        }

        if ('!' <= c && c <= '~') {
            argv[*argc][charcnt++] = c;
            prev = 0;
        } else if (prev != 1 && (c == ' ' || c == '\t' || c == '\n')) {
            prev = 1;
            argv[*argc][charcnt] = '\0';
            charcnt = 0;
            *argc += 1;
        }
    } while (buf[n++] != '\n');

    argv[*argc][charcnt] = '\0';
}

int main()
{
    int ac = 0;
    char ** argv;
    argv = malloc(sizeof (char *) * 16);
    int i;
    for (i = 0; i < 16; i++) {
        argv[i] = malloc(sizeof(char)* 256);
    }

    char buf = "p 1000";
    getargs(&ac, av, buf)

    printf()
    return 0;
}
