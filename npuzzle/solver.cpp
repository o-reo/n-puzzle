#include <Python.h>
#include <iostream>

static PyObject *CppSolver(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    std::cout << "plop" << std::endl;
    return Py_BuildValue("i", sts);
}