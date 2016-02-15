#include "text.h"

int txt_size(TEXT txt) {
	if (0 == txt) {
		return 0;
	}
	return strlen(txt) * sizeof(char);
}

TEXT txt_init(TEXT src) {
	size_t len = txt_size(src);
	TEXT txt = malloc(len + 1);
	if (NULL == txt) {
		ELOG("txt_init: Malloc fail\n");
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

TEXT txt_concat(TEXT txt, TEXT src) {
	if (NULL == src) {
		ELOG("src is NULL, nothing to copy");
		return NULL;
	}
	size_t size_src = txt_size(src);
	if (size_src < 1) {
		ELOG("Nothing to copy");
		return NULL;
	}
	if (NULL == txt) {
		if (NULL == (txt = txt_init(src))) {
			ELOG("txt_init fail!");
			return NULL;
		}
	} else {
		size_t size_txt = txt_size(txt);
		size_t size_total = size_txt + size_src;
		TEXT new_txt = realloc(txt, size_total);
		if (NULL == new_txt) {
			ELOG("Malloc/Realloc fail!");
			return NULL;
		}
		txt = new_txt;
		strncat(txt, src, size_src);
		txt[size_total] = '\0';
		return txt;
	}
	return NULL;
}
