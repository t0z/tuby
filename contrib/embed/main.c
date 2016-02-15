/** Documentation
 *
 * https://docs.python.org/2/c-api/
 */
#include <stdlib.h>
#include <Python.h>
#include "const.h"
#include "text.h"

int main(int argc, char *argv[])
{
	DLOG("INIT");
	char *output = txt_init("foo\0");
	//txt_concat(output, "bar");
	//printf("out: %s", output);
	//http_get("127.0.0.1", 5000, "_", output, HTTP_CONTENT_MAXSIZE);
	return 1;
	/*Py_SetProgramName("tuby");
	Py_InitializeEx(1); // skip signal handler registration
	PySys_SetArgvEx(argc, argv, 0);
	int count = 0;
	int stop = 0;
	char pythonScript[] =
		"import bz2, base64\n"\
		"script = bz2.decompress(base64.b64decode(\""\
		"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"\
		"\"))\n"\
		"exec(script)";
	printf("pythonScript: %s", pythonScript);
	int result = PyRun_SimpleString(pythonScript);
	Py_Finalize();
	*/
	free(output);
}

