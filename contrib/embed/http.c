#include "http.h"
#ifdef __linux__

void * xmalloc(size_t size)
{
	void *value = malloc(size);
	if (0 == value) {
		fatal("virtual memory exhausted");
	}
}

int http_get(const char *addr, const int port, const char *path, char *content, const int content_maxsize)
{
    int socket_desc;
    struct sockaddr_in server;
    char *message = "GET /tuby HTTP/1.1\r\n\r\n";

    printf("GET http://%s:%i/%s\n", addr, port, path);
    //Create socket
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }

    server.sin_addr.s_addr = inet_addr(addr);
    server.sin_family = AF_INET;
    server.sin_port = htons( port );

    //Connect to remote server
    if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        puts("connect error");
        return 1;
    }

    puts("Connected\n");

    //Send some data
    //char *content = (char *)malloc(typeof(content)*1024)
    ;
    //int end = sprintf(message, (sizeof(char) * HTTP_CONTENT_MAXSIZE) - 1, "GET %s HTTP/1.1\r\n\r\n", path);
    //message[end - 1] = '\0';
    printf("Message: %s\n", message);
    if( send(socket_desc , message , strlen(message) , 0) < 0)
    {
        puts("Send failed\n");
        return 1;
    }
    puts("Data Send\n");

    //Receive a reply from the server
    if( recv(socket_desc, content , HTTP_CONTENT_MAXSIZE , 0) < 0)
    {
        puts("recv failed");
    }
    puts("Reply received\n");
    return 0;
}

#endif
