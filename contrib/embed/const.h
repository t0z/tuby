#ifndef __TUBY_CONST_H__
#define __TUBY_CONST_H__

#define DEBUG
#define HTTP_CONTENT_MAXSIZE 8096

#ifndef E_SUCCESS
#define E_SUCCESS 0
#endif

#ifndef E_ERROR
#define E_ERROR 1
#endif

#ifndef NULL
#define NULL 0
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifdef DEBUG
#define DLOG(msg) printf("[debug] %s\n", msg)
#define ELOG(msg) printf("[error] %s\n", msg)
#else
#define DLOG(msg)
#define ELOG(msg)
#endif

#endif
