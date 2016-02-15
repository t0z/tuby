#include "http.h"
#ifdef __linux__

//void * xmalloc(size_t size)
//{
//	void *value = malloc(size);
//	if (0 == value) {
//		fatal("virtual memory exhausted");
//	}
//}

int http_get(const char *addr, const int port, const char *path, char *content, const int content_maxsize)
{
	int socket_desc;
	BIO *outbio = NULL;
	struct sockaddr_in server;
	size_t str_maxsize = 1024;
	char message[str_maxsize + 1];
	char fmt_message[] = "GET %s HTTP/1.1\n\n\r";
	size_t count = snprintf(message, str_maxsize, fmt_message, path);
	message[str_maxsize] = '\0';
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1)
	{
		printf("Could not create socket\n");
		return 1;
	}
	server.sin_addr.s_addr = inet_addr(addr);
	server.sin_family = AF_INET;
	server.sin_port = htons( port );
	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
	{
		puts("connect error");
		return 1;
	}
	if(send(socket_desc , message , strlen(message) , 0) < 0)
	{
		puts("Send failed\n");
		return 1;
	}
	puts("Data Send\n");
	size_t buffer_size = 1;
	char buffer[buffer_size];
	//Receive a reply from the server
	size_t recv_size = 0;
	size_t recv_total = 0;
	int INBODY = 0;
	char last_char = ' ';
	char curchar[1] = "\0";
	int count_carriage = 0;
	int count_newline = 0;
	TEXT current = txt_init("");
	curchar[1] = '\0';
	while((recv_size = recv(socket_desc, curchar , 1, 0)) > 0) {
		if (curchar[0] == '\n') {
			count_newline += 1;
			if (INBODY) {
				txt_concat(current, curchar);
			} else {
				if (count_carriage == 1 && count_newline == 2) {
					INBODY = 1;
				} else {
					printf("header: %s\n", current);
				}
				txt_free(current);
				current = txt_init("");
			}
		} else if (curchar[0] == '\r') {
			count_carriage +=1;
		} else {
			count_carriage = 0;
			count_newline = 0;
			txt_concat(current, curchar);
		}
		recv_total += recv_size;
	}
	content = txt_init(current);
	txt_free(current);
	printf("Reply received: total: %i\n", (int)recv_total);
	return E_SUCCESS;
}

#endif
