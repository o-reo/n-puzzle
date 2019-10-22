#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
from math import sqrt

from .parser import Parser

class Solver():
    def __init__(self, puzzle):
        self.n_moves = 0
        self.puzzle = puzzle
        self.solution = self._snail(puzzle.shape[0])
        self._score_max(self.solution, self._hamming)
        self._score_sum(self.puzzle, self._hamming)

    def _snail(self, size):
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

    def _target(self, num_piece):
        wx, wy = map(lambda x : x[0], np.where(self.solution == num_piece))
        return wx, wy

    def _euclidian(self, x, y):
        return sqrt(x ** 2 + y ** 2)

    def _manhattan(self, x, y):
        return abs(x) + abs(y)

    def _hamming(self, x, y):
        return x != 0 and y != 0

    def _get_scores(self, array, method):
        size = array.shape[0]
        scores = np.zeros(size ** 2)
        for i in range(size ** 2):
            x, y = int(i / size), i % size
            target_coords = self._target(array[x, y])
            scores[i] = method(target_coords[0] - x, target_coords[1] - y)
        return scores

    def _score_max(self, array, method):
        return self._get_scores(array, method).max()

    def _score_sum(self, array, method):
        return self._get_scores(array, method).sum()
    
    def solve(self, args):
        return False
