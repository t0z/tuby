#include "embed.h"

int load_module(int argc, char *argv[]) {
	PyObject *pName, *pModule, *pDict, *pFunc; //*pValue;

	if (argc < 3) {
		printf("Usage: exe_name python_source function_name\n");
		return 1;
	}

	printf("+ pName: %s\n", argv[1]);
	printf("+ pFunc: %s\n", argv[2]);

	// Initialize the Python Interpreter
	Py_Initialize();

	// Build the name object
	if (NULL == (pName = PyString_FromString(argv[1]))) {
		printf("Error: Fail to load name object\n");
		return 1;
	}
	// Load the module object
	if (NULL == (pModule = PyImport_Import(pName))) {
		printf("Error: Fail to load module: %s\n", argv[1]);
		Py_DECREF(pName);
		return 2;
	}
	// pDict is a borrowed reference
	if (NULL == (pDict = PyModule_GetDict(pModule))) {
		printf("Fail acquiring dictionary ref.\n");
		Py_DECREF(pModule);
		Py_DECREF(pName);
		return 3;
	}
	// pFunc is also a borrowed reference
	if (NULL == (pFunc = PyDict_GetItemString(pDict, argv[2]))) {
		printf("Fail acquiring function ref. %s\n", argv[2]);
		Py_DECREF(pDict);
		Py_DECREF(pModule);
		Py_DECREF(pName);
		return 4;
	}

	if (PyCallable_Check(pFunc)) {
		PyObject_CallObject(pFunc, NULL);
	} else {
		PyErr_Print();
	}
	// Clean up
	Py_DECREF(pModule);
	Py_DECREF(pName);

	// Finish the Python Interpreter
	Py_Finalize();

	return 0;
}
