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
    def __init__(self, puzzle):
        """
            Score computation examples    
            self._score_max(self._solution, self._hamming)
            self._score_sum(self._puzzle, self._hamming)
            self._score_sum(self._puzzle, self._linear_conflict)
        """
        self._puzzle = puzzle.copy()
        self._size = puzzle.shape[0]
        self._size2 = self._size ** 2
        # Compute desired state
        self._solution = self._snail()
        # Check if puzzle if solvable
        self._solvable()
        # open set is the heap of investigated states
        self._open_set = []
        # closed is a simple list
        self._closed_set = []
        # placeholder
        self._heuristic = self._hamming

    def _solvable(self):
        puz_cpy = self._puzzle.copy()
        nbr_permutation = 0
        for i in range(self._size2):
            wsx, wsy = map(lambda x: x[0], np.where(self._solution == i))
            wpx, wpy = map(lambda x: x[0], np.where(puz_cpy == i))
            if not i:
                parity_zero = (abs(wsx - wpx) + abs(wsy - wpy)) % 2
            if (wsx == wpx and wsy == wpy):
                continue
            else:
                tmp = puz_cpy[wsx][wsy]
                puz_cpy[wsx][wsy] = puz_cpy[wpx][wpy]
                puz_cpy[wpx][wpy] = tmp
                nbr_permutation += 1
        parity_permutation = nbr_permutation % 2
        if (parity_zero != parity_permutation):
            raise NotSolvable

    def _snail(self):
        """
        Generate a snail matrix that is the desired solution
        """
        snail = np.zeros((self._size, self._size))
        x, y = 0, 0
        dx, dy = 0, 1
        for i in range(1, self._size2):
            snail[x, y] = i
            # rotate when out of bounds or already filled
            if x + dx < 0 or x + dx >= self._size or y + dy < 0 or y + dy >= self._size or snail[x+dx, y+dy] != 0:
                dx, dy = dy, -dx
            x, y = x + dx, y + dy
        return snail

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
        scores = np.zeros(self._size2)
        for i in range(self._size2):
            x, y = int(i / self._size), i % self._size
            target_coords = self._target(array[x, y])
            if (array[x, y] != 0):
                scores[i] = method(array, target_coords, (x, y))
        return scores

    def _score_max(self, array):
        return self._get_scores(array, self._heuristic).max()

    def _score_sum(self, array):
        return self._get_scores(array, self._heuristic).sum()

    def _slide_left(self, array):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(array == 0))
        new_arr = array.copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy - 1] = new_arr[wx, wy - 1], new_arr[wx, wy]
        return (self._score_sum(new_arr), new_arr)

    def _slide_right(self, array):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(array == 0))
        new_arr = array.copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy + 1] = new_arr[wx, wy + 1], new_arr[wx, wy]
        return (self._score_sum(new_arr), new_arr)

    def _slide_up(self, array):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(array == 0))
        new_arr = array.copy()
        new_arr[wx, wy], new_arr[wx - 1,
                                 wy] = new_arr[wx - 1, wy], new_arr[wx, wy]
        return (self._score_sum(new_arr), new_arr)

    def _slide_down(self, array):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(array == 0))
        new_arr = array.copy()
        new_arr[wx, wy], new_arr[wx + 1,
                                 wy] = new_arr[wx + 1, wy], new_arr[wx, wy]
        return (self._score_sum(new_arr), new_arr)

    def solve(self, args):
        # open set is the heap of investigated states
        heapq.heappush(
            self._open_set, (self._score_sum(self._puzzle), self._puzzle))
        # closed is a simple list
        #self._closed_set = []
        return False
