cimport cython
import numpy as np
cimport numpy as np
cimport libc.stdlib
from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_manhattan(long [:, ::1] array, np.ndarray[unsigned char, ndim=2] targets, np.ndarray[unsigned char, ndim=1] target, int coordx, int coordy):
    return libc.stdlib.abs(target[0] - coordx) + libc.stdlib.abs(target[1] - coordy)

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_euclidian(long [:, ::1] array, np.ndarray[unsigned char, ndim=2] targets, np.ndarray[unsigned char, ndim=1] target, int coordx, int coordy):
    return sqrt((target[0] - coordx) ** 2 + (target[1] - coordy) ** 2)

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_hamming(long [:, ::1] array, np.ndarray[unsigned char, ndim=2] targets, np.ndarray[unsigned char, ndim=1] target, int coordx, int coordy):
        return target[0] != coordx and target[1] != coordy

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_linear_conflict(long [:, ::1] array, np.ndarray[unsigned char, ndim=2] targets, np.ndarray[unsigned char, ndim=1] target, int coordx, int coordy):
    cdef int score
    cdef int direction
    cdef int x

    score = fast_manhattan(None, None, target, coordx, coordy)
    if coordx == target[0]:
        direction = 2 * (target[1] > coordy) - 1
        for x in range(coordy + direction, target[1]):
            if targets[array[coordx, x]][0] == target[0]:
               return score + 2
    elif coordy == target[1]:
        direction = 2 * (target[0] > coordx) - 1
        for x in range(coordx + direction, target[0]):
            if targets[array[x, coordy]][1] == target[1]:
                return score + 2
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_get_score(long [:, ::1] array, np.ndarray[unsigned char, ndim=2] targets, heuristic):
    cdef int score
    cdef np.ndarray[unsigned char, ndim=1] target
    cdef int x
    cdef int y
    cdef long val
    cdef int size
    cdef (int, int) index

    score = 0
    size = array.shape[0]
    for x in range(0, size):
        for y in range(0, size):
            val = array[x, y]
            target = targets[val]
            if val != 0 and x != target[0] and y != target[1]:
                score += heuristic(array, targets, target, x, y)
    # score = 0
    # it = np.nditer(array, flags=['multi_index'])
    # while not it.finished:
    #     index = it.multi_index
    #     target = targets[array[index[0], index[1]]]
    #     if array[index[0], index[1]] != 0 and index[0] != target[0] and index[1] != target[1]:
    #         score += heuristic(array, targets, target,
    #                                 index[0], index[1])
    #     it.iternext()
    return score
