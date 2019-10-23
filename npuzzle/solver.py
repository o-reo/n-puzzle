#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
from math import sqrt
import heapq
import asyncio

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
        self._puzzle = puzzle.copy()
        self._size = puzzle.shape[0]
        self._size2 = self._size ** 2
        # Compute desired state
        self._solution = self._snail()
        # Get heuristic
        self._heuristic = self._dispatch(args)
        self._search = 0 if args.search == "greedy" else 1
        # open set is the heap of investigated states
        self._open_set = []
        # closed is a simple list
        self._closed_set = set()

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

    def _dispatch(self, args):
        heuristic = args.heuristic
        if heuristic == "euclidian":
            return self._euclidian
        if heuristic == "manhattan":
            return self._manhattan
        if heuristic == "hamming":
            return self._hamming
        if heuristic == "linear_conflict":
            return self._linear_conflict
        raise InvalidHeuristic

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

    def _slide_left(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(node[2] == 0))
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy - 1] = new_arr[wx, wy - 1], new_arr[wx, wy]
        return (self._score_sum(new_arr) + node[3] * self._search, node[1] + [0], new_arr, node[3] + 1)

    def _slide_right(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(node[2] == 0))
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy + 1] = new_arr[wx, wy + 1], new_arr[wx, wy]
        return (self._score_sum(new_arr) + node[3] * self._search, node[1] + [2], new_arr, node[3] + 1)

    def _slide_up(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(node[2] == 0))
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx - 1,
                                 wy] = new_arr[wx - 1, wy], new_arr[wx, wy]
        return (self._score_sum(new_arr) + node[3] * self._search, node[1] + [1], new_arr, node[3] + 1)

    def _slide_down(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = map(lambda x: x[0], np.where(node[2] == 0))
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx + 1,
                                 wy] = new_arr[wx + 1, wy], new_arr[wx, wy]
        return (self._score_sum(new_arr) + node[3] * self._search, node[1] + [3], new_arr, node[3] + 1)

    async def _slide(self, heap, func, node):
        await 0 if heapq.heappush(heap, func(node)) else 0

    async def _main(self, heap, node):
            wx, wy = map(lambda x: x[0], np.where(node[2] == 0))
            threads = []
            if (wy > 0):
                threads.append(self._slide(heap, self._slide_left, node))
            if (wy < self._size - 1):
                threads.append(self._slide(heap, self._slide_right, node))
            if (wx > 0):
                threads.append(self._slide(heap, self._slide_up, node))
            if (wx < self._size - 1):
                threads.append(self._slide(heap, self._slide_down, node))
            await asyncio.wait(threads)

    def _astar(self, heap):
        max_state = 0
        while len(heap):
            max_state = max(max_state, len(heap))
            node = heapq.heappop(heap)
            if np.array_equal(self._solution, node[2]):
                return (node, max_state, len(heap) + len(self._closed_set))
            a = len(self._closed_set)
            self._closed_set.add(node[2].tostring())
            if a == len(self._closed_set):
                continue
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._main(heap, node))
        else:
            raise NotSolvable 

    def solve(self):
        self._solvable()
        # open set is the heap of investigated states
        heapq.heappush(self._open_set, (self._score_sum(self._puzzle), [], self._puzzle, 0))
        a = self._astar(self._open_set)
        # closed is a simple list
        #self._closed_set = []
        return a
