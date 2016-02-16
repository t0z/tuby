#include "text.h"

int txt_size(TEXT txt) {
	if (NULL == txt) {
		return 0;
	}
	return strlen(txt) * sizeof(char);
}

TEXT txt_init(TEXT src) {
	size_t len = txt_size(src);
	if (len > TXT_MAX_SIZE) {
		ELOG("text: cannot init txt, src too large: %i", len);
		return NULL;
	}
	TEXT txt = malloc(len + 1);
	if (NULL == txt) {
		ELOG("txt_init: Malloc fail");
		return NULL;
	}
	strncpy(txt, src, len);
	txt[len] = '\0';
	return txt;
}

int txt_free(TEXT txt) {
	if (NULL != txt) {
		free(txt);
		txt = NULL;
		return E_SUCCESS;
	}
	return E_ERROR;
}

int txt_cat(TEXT txt, TEXT src) {
	if (NULL == src) {
		ELOG("text: src is NULL, nothing to copy");
		return -1;
	}
	size_t size_src = txt_size(src);
	if (size_src < 1) {
		ELOG("text: src is empty nothing to copy");
		return -1;
	}
	if (NULL == txt) {
		ELOG("text: destination txt is NULL");
		return -1;
	}
	size_t size_txt = txt_size(txt);
	size_t size_total = size_txt + size_src;
	TEXT newtxt = realloc(txt, size_total + 1);
	if (NULL == newtxt) {
		ELOG("text: realloc fail!");
		return -1;
	}
	txt = newtxt;
	strncat(txt, src, size_src);
	txt[size_total] = '\0';
	return size_total;
}
