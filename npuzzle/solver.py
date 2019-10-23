#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
from math import sqrt
import heapq

from .exception import *
from .parser import Parser


class Solver():
    def __init__(self, puzzle, args):
        """
            Score computation examples    
            self._score_max(self._solution, self._hamming)
            self._score_sum(self._puzzle, self._hamming)
            self._score_sum(self._puzzle, self._linear_conflict)
        """
        self._puzzle = puzzle
        # Compute desired state
        self._solution = self._snail(puzzle.shape[0])
        # Get heuristic
        self._heuristic = self.dispatch(args)
        # open set is the heap of investigated states
        self._open_set = []
        # closed is a simple list
        self._closed_set = set()

    def _snail(self, size):
        """
        Generate a snail matrix that is the desired solution
        """
        snail = np.zeros((size, size))
        x, y = 0, 0
        dx, dy = 0, 1
        for i in range(1, size ** 2):
            snail[x, y] = i
            # rotate when out of bounds or already filled
            if x + dx < 0 or x + dx >= size or y + dy < 0 or y + dy >= size or snail[x+dx, y+dy] != 0:
                dx, dy = dy, -dx
            x, y = x + dx, y + dy
        return snail

    def _solvable(self, size):
        nbr_permutation = 0
        for i in range(size ** 2):
            wsx, wsy = map(lambda x: x[0], np.where(self._solution == i))
            wpx, wpy = map(lambda x: x[0], np.where(self._puzzle == i))
            if not i:
                parity_zero = (abs(wsx - wpx) + abs(wsy - wpy)) % 2
            if (wsx == wpx and wsy == wpy):
                continue
            else:
                tmp = self._puzzle[wsx][wsy]
                self._puzzle[wsx][wsy] = self._puzzle[wpx][wpy]
                self._puzzle[wpx][wpy] = tmp
                nbr_permutation += 1
        parity_permutation = nbr_permutation % 2
        if (parity_zero != parity_permutation):
            raise NotSolvable

    def _dispatch(self, heuristic):
        if heuristic == euclidian:
            return self._euclidian
        if heuristic == manhattan:
            return self._manhattan
        if heuristic == hamming:
            return self._hamming
        if heuristic == linear_conflict:
            return self._linear_conflict

    def _target(self, num_piece):
        """
        Get the desired slot coordinates
        """
        wx, wy = map(lambda x: x[0], np.where(self._solution == num_piece))
        return wx, wy

    # Heuristics
    def _euclidian(self, array, target, coords):
        return sqrt((target[0] - coords[0]) ** 2 + (target[1] - coords[1]) ** 2)

    def _manhattan(self, array, target, coords):
        return abs(target[0] - coords[0]) + abs(target[1] - coords[1])
     
    def _hamming(self, array, target, coords):
        return target != coords

    def _linear_conflict(self, array, target, coords):
        score = self._manhattan(array, target, coords)
        add = 0
        if coords[0] == target[0]:
            direction = 2 * (target[1] > coords[1]) - 1
            for x in range(coords[1] + direction, target[1] + direction):
                if array[coords[0], x] != 0 and self._target(array[coords[0], x])[0] == target[0]:
                    add = 1
        elif coords[1] == target[1]:
            direction = 2 * (target[1] > coords[1]) - 1
            for x in range(coords[0] + direction, target[0]):
                if array[x, coords[1]] != 0 and self._target(array[x, coords[1]])[1] == target[1]:
                    add = 1
        return score + add
    # --

    def _get_scores(self, array, method):
        size = array.shape[0]
        scores = np.zeros(size ** 2)
        for i in range(size ** 2):
            x, y = int(i / size), i % size
            target_coords = self._target(array[x, y])
            if (array[x, y] != 0):
                scores[i] = method(array, target_coords, (x, y))
        return scores

    def _score_max(self, array, method):
        return self._get_scores(array, method).max()

    def _score_sum(self, array, method):
        return self._get_scores(array, method).sum()

    def _astar(self, heap):
        M = 0
        tot = 0
        while (len(heap)):
            M = max(M, len(heap))
            tot += 1
            node = heapq.heappop(heap)
            if np.equal(self._snails, node[1]):
                return (M, nbr)
                break
            a = len(self._close)
            self._close.add(node[1])
            if (a == len(self._close))
                continue
            wx, wy = map(lambda x: x[0], np.where(node[1] == 0))
            if (wx > 0):
                heapq.heappush(self._open_set, self._slide_left(node))
            if (wx < self._size - 1):
                heapq.heappush(self._open_set, self._slide_right(node))
            if (wy > 0):
                heapq.heappush(self._open_set, self._slide_up(node))
            if (wy < self._size - 1):
                heapq.heappush(self._open_set, self._slide_down(node))
        else:
            raise NotSolvable 

            
        

    def solve(self, args):
        self._solvable()
        # open set is the heap of investigated states
        heapq.heappush(self._open_set, (self.score_sum(self._manhattan), self._puzzle, 0, []))
        self._astar(heapq.heapify(self._open_set))
        # closed is a simple list
        #self._closed_set = []
        return False
