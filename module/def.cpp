#include <Python.h>
#include <iostream>
#include "solver.h"
#include <vector>
#include <cmath>

static PyObject *puzzlesolver(PyObject *self, PyObject *args)
{
    PyObject *array;
    std::vector<std::vector<int>> puzzle;

    PyArg_ParseTuple(args, "O!", &PyList_Type, &array);
    int size2 = PyList_Size(array);
    int size = static_cast<int>(sqrt(size2));
    int line = 0;
    for (int i = 0; i < size2; i++)
    {
        if (i % size == 0)
        {
            puzzle.push_back(std::vector<int>());
            line = i / size;
        }
        PyObject *itemx = PyList_GetItem(array, i);
        puzzle[line].push_back(_PyLong_AsInt(itemx));
    }
    Solver sol(puzzle);
    auto res = sol.solve();
    auto moves = std::get<1>(res);
    std::cout << moves.size() << std::endl;
    // for (int i= 0; i < moves.size(); i++){
    //     std::cout << moves[i] << std::endl;
    // }
    return Py_BuildValue("i", 0);
}

static PyMethodDef module_methods[] = {
    {"puzzlesolver", puzzlesolver, METH_VARARGS, "Solves an npuzzle"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef PuzzleModule = {
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