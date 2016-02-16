#ifndef __STRING_H__
#define __STRING_H__

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "const.h"

#define TXT_CHUNK_SIZE 1024
#define TXT_MAX_SIZE 65535

typedef char * TEXT;

int txt_free(TEXT txt);
TEXT txt_init(TEXT src);
int txt_concat(TEXT txt, TEXT src);
int txt_size(TEXT txt);

#endif

