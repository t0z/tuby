#ifndef __STRING_H__
#define __STRING_H__

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "const.h"

typedef char* TEXT;

TEXT txt_init(TEXT src);
int txt_concat(TEXT txt, TEXT src);

#endif
