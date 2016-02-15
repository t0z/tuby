#include "text.h"

TEXT txt_init(TEXT src) {
	printf("txt ini");
	int txtlen = strlen(src) * sizeof(char);
	printf("txtlen: %i", txtlen);
	TEXT txt = (TEXT)malloc(txtlen + 1);
	strncpy(txt, txtlen, src);
	//txt[txtlen] = '\0';
	return src;
}

int txt_concat(TEXT txt, TEXT src)
{
	DLOG("TXT_CONCAT");
	if (NULL == src) {
		ELOG("src is NULL, nothing to copy");
		return E_ERROR;
	}
	int size = strlen(src);
	DLOG("str_concat");
	if (NULL == src || strlen(src) < 1) {
		ELOG("Nothing to copy");
		return E_ERROR;
	}
	if (NULL == txt) {
		DLOG("need malloc");
		txt = txt_init(src);
	} else {
		DLOG("need realloc");
	}
	if (NULL == txt) {
		ELOG("Malloc/Realloc fail!");
		return E_ERROR;
	}
	return E_SUCCESS;

}
