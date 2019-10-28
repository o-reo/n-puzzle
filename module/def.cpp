#include <Python.h>
#include <iostream>
#include "solver.h"

static PyObject *puzzlesolver(PyObject *self, PyObject *args)
{
    PyObject *array;

    PyArg_ParseTuple(args, "O!", &PyList_Type, &array);
    return Py_BuildValue("i", 0);
}

static PyMethodDef module_methods[] = {
    {"puzzlesolver", puzzlesolver, METH_VARARGS, "Solves an npuzzle"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef PuzzleModule= {
    PyModuleDef_HEAD_INIT,
    "puzzlesolver",
    "npuzzle solver", 
    -1,
    module_methods,
};

PyMODINIT_FUNC PyInit_puzzlesolver(void)
{
    return PyModule_Create(&PuzzleModule);
}