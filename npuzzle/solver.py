#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import heapq

from .exception import NotSolvable, InvalidHeuristic
from .parser import Parser


class Solver():
    def __init__(self, puzzle, args = None):
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
        self._dispatch(args)
        self._search = 0 if args is not None and args.search == "greedy" else 1
        # open set is the heap of investigated states
        self._open_set = []
        # closed is a simple list
        self._closed_set = set()
        # compute desired locations of the pieces
        self._targets = []
        self._compute_targets()
        # to print directions
        self._directions = ['left', 'up', 'right', 'down']

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
        if args is None:
            self._heuristic = self._linear_conflict
            return
        heuristic = args.heuristic
        if heuristic == "euclidian":
            self._heuristic = self._euclidian
        elif heuristic == "manhattan":
             self._heuristic = self._manhattan
        elif heuristic == "hamming":
            self._heuristic = self._hamming
        elif heuristic == "linear_conflict":
            self._heuristic = self._linear_conflict

    def _compute_targets(self):
        self._targets.append((-1, -1))
        for i in range(1, self._size2):
            wx, wy = map(lambda x: int(x[0]), np.where(self._solution == i))
            self._targets.append((wx, wy))

    # Heuristics
    def _euclidian(self, array, target, coords):
        return np.sqrt((target[0] - coords[0]) ** 2 + (target[1] - coords[1]) ** 2)

    def _manhattan(self, array, target, coords):
        return abs(target[0] - coords[0]) + abs(target[1] - coords[1])

    def _hamming(self, array, target, coords):
        return target != coords

    def _linear_conflict(self, array, target, coords):
        score = self._manhattan(array, target, coords)
        if coords[0] == target[0]:
            direction = 2 * (target[1] < coords[1]) - 1
            for x in range(coords[1] + direction, target[1]):
                if self._targets[array[coords[0], x]][0] == target[0]:
                    return score + 1
        elif coords[1] == target[1]:
            direction = 2 * (target[0] < coords[0]) - 1
            for x in range(coords[0] + direction, target[0]):
                if self._targets[array[x, coords[1]]][1] == target[1]:
                    return score + 1
        return score

    def _get_score(self, array):
        score = 0
        for i in range(self._size):
            for j in range(self._size):
                target = self._targets[array[i, j]]
                if array[i, j] != 0 and (i, j) != target:
                    score += self._heuristic(array, target,
                                             (i, j))
        return score

    def _get_zero(self, array):
        return [e[0] for e in np.where(array == 0)]

    def _slide_left(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy - 1] = new_arr[wx, wy - 1], new_arr[wx, wy]
        return (self._get_score(new_arr) + node[3] * self._search, node[1] + [0], new_arr, node[3] + 1)

    def _slide_up(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx - 1,
                                 wy] = new_arr[wx - 1, wy], new_arr[wx, wy]
        return (self._get_score(new_arr) + node[3] * self._search, node[1] + [1], new_arr, node[3] + 1)

    def _slide_right(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy + 1] = new_arr[wx, wy + 1], new_arr[wx, wy]
        return (self._get_score(new_arr) + node[3] * self._search, node[1] + [2], new_arr, node[3] + 1)

    def _slide_down(self, node):
        """
            return tuple (score, moves, new_puzzle, number of moves)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx + 1,
                                 wy] = new_arr[wx + 1, wy], new_arr[wx, wy]
        return (self._get_score(new_arr) + node[3] * self._search, node[1] + [3], new_arr, node[3] + 1)

    def _astar(self, heap):
        max_state = 0
        while len(heap):
            max_state = max(max_state, len(heap))
            node = heapq.heappop(heap)
            if np.all(self._solution == node[2]):
                return (node, max_state, len(heap) + len(self._closed_set))
            a = len(self._closed_set)
            self._closed_set.add(node[2].tostring())
            if a == len(self._closed_set):
                continue
            wx, wy = self._get_zero(node[2])
            if (wy > 0):
                heapq.heappush(self._open_set, self._slide_left(node))
            if (wy < self._size - 1):
                heapq.heappush(self._open_set, self._slide_right(node))
            if (wx > 0):
                heapq.heappush(self._open_set, self._slide_up(node))
            if (wx < self._size - 1):
                heapq.heappush(self._open_set, self._slide_down(node))
        else:
            raise NotSolvable

    def slide(self, puzzle, direction):
        puz = None
        if direction == 0:
            _, _, puz, _ = self._slide_left((0, [], puzzle, 0))
        if direction == 1:
            _, _, puz, _ = self._slide_up((0, [], puzzle, 0))
        if direction == 2:
            _, _, puz, _ = self._slide_right((0, [], puzzle, 0))
        if direction == 3:
            _, _, puz, _ = self._slide_down((0, [], puzzle, 0))
        return puz

    def print_solution(self, solution):
        puz = self._puzzle.copy()
        for move in solution[0][1]:
            print(self._directions[move])
            puz = self.slide(puz, move)
            print(puz)

    def solve(self):
        self._solvable()
        # open set is the heap of investigated states
        heapq.heappush(self._open_set, (self._get_score(
            self._puzzle), [], self._puzzle, 0))
        a = self._astar(self._open_set)
        return a
