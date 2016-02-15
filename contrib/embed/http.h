#ifndef __TUBY_HTTP_H__
#define __TUBY_HTTP_H__

#include <stdio.h>
#include <string.h>    //strlen
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr

#include "const.h"
#include "ssl.h"

int http_get(const char *addr, int const port, const char *path, char *content,
		const int content_maxsize);

#endif
