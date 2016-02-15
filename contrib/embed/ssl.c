/* ------------------------------------------------------------ *
 * file:        sslconnect.c                                    *
 * purpose:     Example code for building a SSL connection and  *
 *              retrieving the server certificate               *
 * author:      06/12/2012 Frank4DD                             *
 *                                                              *
 * compile:     gcc -o sslconnect sslconnect.c -lssl -lcrypto   *
 * ------------------------------------------------------------ */

#include "ssl.h"

//struct ssl_s {
//	BIO *certbio: NULL,
//	BIO *outbio: NULL,
//	X509 *cert: NULL,
//	X509_NAME *certname: NULL,
//	SSL_CTX *ctx: NULL,
//	SSL *ssl: NULL,
//};

int create_ssl_socket(char dest_url[]) {

	BIO *certbio = NULL;
	BIO *outbio = NULL;
	X509 *cert = NULL;
	X509_NAME *certname = NULL;
	const SSL_METHOD *method;
	SSL_CTX *ctx;
	SSL *ssl;
	int server = 0;
	int ret, i;
	/* ---------------------------------------------------------- *
	 * These function calls initialize openssl for correct work.  *
	 * ---------------------------------------------------------- */
	OpenSSL_add_all_algorithms();
	ERR_load_BIO_strings();
	ERR_load_crypto_strings();
	SSL_load_error_strings();
	/* ---------------------------------------------------------- *
	 * Create the Input/Output BIO's.                             *
	 * ---------------------------------------------------------- */
	certbio = BIO_new(BIO_s_file());
	outbio = BIO_new_fp(stdout, BIO_NOCLOSE);
	/* ---------------------------------------------------------- *
	 * initialize SSL library and register algorithms             *
	 * ---------------------------------------------------------- */
	if (SSL_library_init() < 0) {
		BIO_printf(outbio, "Could not initialize the OpenSSL library !\n");
		return 1;
	}
	/* ---------------------------------------------------------- *
	 * Set SSLv2 client hello, also announce SSLv3 and TLSv1      *
	 * ---------------------------------------------------------- */
	method = SSLv23_client_method();
	/* ---------------------------------------------------------- *
	 * Try to create a new SSL context                            *
	 * ---------------------------------------------------------- */
	if ((ctx = SSL_CTX_new(method)) == NULL) {
		BIO_printf(outbio, "Unable to create a new SSL context structure.\n");
	}
	/* ---------------------------------------------------------- *
	 * Disabling SSLv2 will leave v3 and TSLv1 for negotiation    *
	 * ---------------------------------------------------------- */
	SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv2);
	/* ---------------------------------------------------------- *
	 * Create new SSL connection state object                     *
	 * ---------------------------------------------------------- */
	ssl = SSL_new(ctx);
	/* ---------------------------------------------------------- *
	 * Make the underlying TCP socket connection                  *
	 * ---------------------------------------------------------- */

	server = create_socket(dest_url, outbio);
	if (server == 0) {
		printf("Cannot create socket: %s", dest_url);
		return 1;
	}
	/* ---------------------------------------------------------- *
	 * Attach the SSL session to the socket descriptor            *
	 * ---------------------------------------------------------- */
	if (0 == SSL_set_fd(ssl, server)) {
		BIO_printf(outbio, "Error: attach session fail");
		return 1;
	}
	/* ---------------------------------------------------------- *
	 * Try to SSL-connect here, returns 1 for success             *
	 * ---------------------------------------------------------- */
	int status = SSL_connect(ssl);
	if (status != 0) {
		printf("Error: SSL connect fail code: %i", status);
		BIO_printf(outbio, "Error: Could not build a SSL session to: %s.\n",
				dest_url);
		return 1;

	}

	BIO_printf(outbio, "Successfully enabled SSL/TLS session to: %s.\n",
			dest_url);

//	char message[] = "GET /_ HTTP/1.1\r\r\n";
//	if (send(server, message, strlen(message), 0) < 0) {
//		puts("Send failed\n");
//		return 1;
//	}
//
//	puts("Data Send\n");
//	int max = 65535;
//	TEXT content = "";
//	//Receive a reply from the server
//	if (recv(server, content, max, 0) < 0) {
//		puts("recv failed");
//	}
//	puts("Reply received\n");
//	return ssl;
	/* ---------------------------------------------------------- *
	 * Get the remote certificate into the X509 structure         *
	 * ---------------------------------------------------------- */
	cert = SSL_get_peer_certificate(ssl);
	if (cert == NULL)
		BIO_printf(outbio, "Error: Could not get a certificate from: %s.\n",
				dest_url);
	else
		BIO_printf(outbio, "Retrieved the server's certificate from: %s.\n",
				dest_url);

	/* ---------------------------------------------------------- *
	 * extract various certificate information                    *
	 * -----------------------------------------------------------*/
	certname = X509_NAME_new();
	certname = X509_get_subject_name(cert);

	/* ---------------------------------------------------------- *
	 * display the cert subject here                              *
	 * -----------------------------------------------------------*/
	BIO_printf(outbio, "Displaying the certificate subject data:\n");
	X509_NAME_print_ex(outbio, certname, 0, 0);
	BIO_printf(outbio, "\n");

	/* ---------------------------------------------------------- *
	 * Free the structures we don't need anymore                  *
	 * -----------------------------------------------------------*/
	SSL_free(ssl);
	close(server);
	X509_free(cert);
	SSL_CTX_free(ctx);
	BIO_printf(outbio, "Finished SSL/TLS connection with server: %s.\n",
			dest_url);
	return (0);
}

/* ---------------------------------------------------------- *
 * create_socket() creates the socket & TCP-connect to server *
 * ---------------------------------------------------------- */
int create_socket(char url_str[], BIO *out) {
	printf("create_socket: %s\n", url_str);
	int sockfd;
	char hostname[256] = "";
	char portnum[6] = "443";
	char proto[6] = "";
	char *tmp_ptr = NULL;
	int port;
	struct hostent *host;
	struct sockaddr_in dest_addr;

	/* ---------------------------------------------------------- *
	 * Remove the final / from url_str, if there is one           *
	 * ---------------------------------------------------------- */
	if (url_str[strlen(url_str)] == '/')
		url_str[strlen(url_str)] = '\0';

	/* ---------------------------------------------------------- *
	 * the first : ends the protocol string, i.e. http            *
	 * ---------------------------------------------------------- */
	strncpy(proto, url_str, (strchr(url_str, ':') - url_str));

	/* ---------------------------------------------------------- *
	 * the hostname starts after the "://" part                   *
	 * ---------------------------------------------------------- */
	strncpy(hostname, strstr(url_str, "://") + 3, sizeof(hostname));
	/* ---------------------------------------------------------- *
	 * if the hostname contains a colon :, we got a port number   *
	 * ---------------------------------------------------------- */
	if (strchr(hostname, ':')) {
		tmp_ptr = strchr(hostname, ':');
		/* the last : starts the port number, if avail, i.e. 8443 */
		strncpy(portnum, tmp_ptr + 1, sizeof(portnum));
		*tmp_ptr = '\0';
	}

	port = atoi(portnum);
	if ((host = gethostbyname(hostname)) == NULL) {
		BIO_printf(out, "Error: Cannot resolve hostname %s.\n", hostname);
		abort();
	}
	/* ---------------------------------------------------------- *
	 * create the basic TCP socket                                *
	 * ---------------------------------------------------------- */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(port);
	dest_addr.sin_addr.s_addr = *(long*) (host->h_addr);

	/* ---------------------------------------------------------- *
	 * Zeroing the rest of the struct                             *
	 * ---------------------------------------------------------- */
	memset(&(dest_addr.sin_zero), '\0', 8);

	tmp_ptr = inet_ntoa(dest_addr.sin_addr);

	/* ---------------------------------------------------------- *
	 * Try to make the host connect here                          *
	 * ---------------------------------------------------------- */
	if (connect(sockfd, (struct sockaddr *) &dest_addr, sizeof(struct sockaddr))
			== -1) {
		BIO_printf(out, "Error: Cannot connect to host %s [%s] on port %d.\n",
				hostname, tmp_ptr, port);
		return 0;
	}
	return sockfd;
}
