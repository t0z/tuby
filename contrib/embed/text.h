#ifndef __STRING_H__
#define __STRING_H__

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "const.h"

typedef char *TEXT;
typedef TEXT PTEXT;

int txt_free(TEXT txt);
TEXT txt_init(TEXT src);
TEXT txt_concat(PTEXT txt, TEXT src);
int txt_size(TEXT txt);

#endif
