#ifndef __TUBY_HTTP_H__
#define __TUBY_HTTP_H__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "text.h"

#include <curl/curl.h>
#include "text.h"

struct MemoryStruct {
	char *memory;
	size_t size;
};

void http_init(void);
int http_post(TEXT url, TEXT data, TEXT *body);
void http_end(void);

#endif
