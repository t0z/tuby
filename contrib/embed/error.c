#include "error.h"

void fatal(const char *msg, int code)
{
	printf("[FATAL] %i %s", code, msg);
	exit(code);
}
