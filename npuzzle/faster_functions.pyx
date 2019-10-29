cimport cython
import numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_manhattan(array, targets, (int, int) target, (int, int) coords):
    return abs(target[0] - coords[0]) + abs(target[1] - coords[1])

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_euclidian(array, targets, (int, int) target, (int, int) coords):
    return np.sqrt((target[0] - coords[0]) ** 2 + (target[1] - coords[1]) ** 2)

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_hamming(array, targets, (int, int) target, (int, int) coords):
        return target != coords

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_linear_conflict(long [:, ::1] array, targets, (int, int) target, (int, int) coords):
    cdef int score
    cdef int direction
    cdef int x

    score = fast_manhattan(None, None, target, coords)
    if coords[0] == target[0]:
        direction = 2 * (target[1] > coords[1]) - 1
        for x in range(coords[1] + direction, target[1]):
            if targets[array[coords[0], x]][0] == target[0]:
               return score + 2
    elif coords[1] == target[1]:
        direction = 2 * (target[0] > coords[0]) - 1
        for x in range(coords[0] + direction, target[0]):
            if targets[array[x, coords[1]]][1] == target[1]:
                return score + 2
    return score

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_get_score(array, targets, heuristic):
    cdef int score
    cdef (int, int) target
    cdef (int, int) index
    cdef long[:, ::1] narray

    score = 0
    narray = array
    it = np.nditer(array, flags=['multi_index'])
    while not it.finished:
        index = it.multi_index
        target = targets[narray[index[0], index[1]]]
        if narray[index[0], index[1]] != 0 and index != target:
            score += heuristic(narray, targets, target,
                                    index)
        it.iternext()
    return score
