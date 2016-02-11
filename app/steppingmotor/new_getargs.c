#include <stdio.h>

getargs(int *ac, char *av[], char *p)
{
    *ac = 0;
    av[0] = NULL;

    for (;;) {
        while(isblank(*p))
            p++;
        if (*p == '\0')
            return;
        av[(*ac)++] = p;
        while (*p && !isblank(*p))
            p++;
        if (*p == '\0')
            return;
        *p++ = '\0';
    }
}
