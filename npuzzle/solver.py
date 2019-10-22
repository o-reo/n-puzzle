#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
from math import sqrt

from .parser import Parser


class Solver():
    def __init__(self, puzzle):
        """
            Score computation examples    
            self._score_max(self._solution, self._hamming)
            self._score_sum(self._puzzle, self._hamming)
            self._score_sum(self._puzzle, self._linear_conflict)
        """
        self._puzzle = puzzle
        # Compute desired state
        self._solution = self._snail(puzzle.shape[0])
        # open set is the heap of investigated states
        self._open_set = []
        # closed is a simple list
        self._closed_set = []

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
        if coords[1] == target[1]:
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

    def solve(self, args):
        return False
