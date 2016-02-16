#include "http.h"

void http_init(void) {
	curl_global_init(CURL_GLOBAL_ALL);
}

void http_end(void) {
	curl_global_cleanup();
}

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb,
		void *userp) {
	size_t realsize = size * nmemb;
	struct MemoryStruct *mem = (struct MemoryStruct *) userp;

	mem->memory = realloc(mem->memory, mem->size + realsize + 1);
	if (mem->memory == NULL) {
		/* out of memory! */
		printf("not enough memory (realloc returned NULL)\n");
		return 0;
	}

	memcpy(&(mem->memory[mem->size]), contents, realsize);
	mem->size += realsize;
	mem->memory[mem->size] = 0;

	return realsize;
}

int http_post(TEXT url, TEXT data, TEXT *body) {
	DLOG("http POST %s === %s", url, data);
	CURL *curl;
	CURLcode res;
	struct MemoryStruct chunk;

	/* will be grown as needed by the realloc above */
	chunk.memory = malloc(1);
	if (NULL == chunk.memory) {
		ELOG("curl: failed to init memory");
		return 1;
	}
	chunk.size = 0; /* no data at this point */
	/* get a curl handle */
	curl = curl_easy_init();
	if (!curl) {
		ELOG("curl: fail to initialize");
		free(chunk.memory);
		return CURLE_FAILED_INIT;
	}
//#ifdef SKIP_PEER_VERIFICATION
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
//#endif
//#ifdef SKIP_HOSTNAME_VERIFICATION
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
//#endif
	/* First set the URL that is about to receive our POST. This URL can
	 just as well be a https:// URL if that is what should receive the
	 data. */
	curl_easy_setopt(curl, CURLOPT_URL, url);
	/* Switch on full protocol/debug output while testing */
	curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
	/* disable progress meter, set to 0L to enable and disable debug output */
	curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
	/* send all data to this function  */
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
	/* we pass our 'chunk' struct to the callback function */
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *) &chunk);
	/* some servers don't like requests that are made without a user-agent
	 field, so we provide one */
	curl_easy_setopt(curl, CURLOPT_USERAGENT, "libcurl-agent/1.0");
	/* Now specify the POST data */
	curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
	/* Perform the request, res will get the return code */
	res = curl_easy_perform(curl);
	/* Check for errors */
	if (res != CURLE_OK) {
		fprintf(stderr, "curl_easy_perform() failed: %s\n",
				curl_easy_strerror(res));
		free(chunk.memory);
		curl_easy_cleanup(curl);
		return res;
	}
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, data);
	curl_easy_cleanup(curl);
	*body = chunk.memory;
	return CURLE_OK;
}
