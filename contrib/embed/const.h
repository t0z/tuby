#ifndef __TUBY_CONST_H__
#define __TUBY_CONST_H__

#define SKIP_PEER_VERIFICATION
//#define DEBUG
#define HTTP_CONTENT_MAXSIZE 8096

#ifndef E_SUCCESS
#define E_SUCCESS 0
#endif

#ifndef E_ERROR
#define E_ERROR 1
#endif

#ifndef NULL
#define NULL 0 //((void *)0)
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif
#ifdef DEBUG
// GCC specific extension for FormatLiteral
#define DLOG(FormatLiteral, ...)  fprintf (stderr, "[debug] %s(%u): " FormatLiteral "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#define ELOG(FormatLiteral, ...)  fprintf (stderr, "[error] %s(%u): " FormatLiteral "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#define WLOG(FormatLiteral, ...)  fprintf (stderr, "[warn_] %s(%u): " FormatLiteral "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#else
#define DLOG(FormatLiteral, ...)
#define ELOG(FormatLiteral, ...)
#define WLOG(FormatLiteral, ...)
#endif

#endif
