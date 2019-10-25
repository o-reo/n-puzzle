#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import heapq
from .faster_functions import fast_manhattan, fast_linear_conflict, fast_euclidian, fast_hamming, fast_get_score

from .exception import NotSolvable, InvalidHeuristic

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
        self._heuristic = self._dispatch(args)
        self._algo = self._astar if not args or args.algorithm == 'astar' else self._ida
        self._search = False if not args or args.search == "greedy" else True
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
        for i in range(1, self._size):
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
            wsx = map(lambda x: x[0], np.where(self._solution == i))
            wpx = map(lambda x: x[0], np.where(puz_cpy == i))
            if not i:
                parity_zero = (abs(wsx - wpx) + abs(wsy - wpy)) % 2
            if wsx == wpx and wsy == wpy:
                continue
            else:
                tmp = puz_cpy[wsx][wsy]
                puz_cpy[wsx][wsy] = puz_cpy[wpx][wpy]
                puz_cpy[wpx][wpy] = tmp
                nbr_permutation += 1
        parity_permutation = nbr_permutation % 2
        if parity_zero != parity_permutation:
            raise NotSolvable

    def _dispatch(self, args):
        if not args or not args.heuristic:
            self._fast_heuristic = fast_manhattan
            return self._manhattan
        heuristic = args.heuristic
        if heuristic == "euclidian":
            self._fast_heuristic = fast_euclidian
            return self._euclidian
        if heuristic == "manhattan":
            self._fast_heuristic = fast_manhattan
            return self._manhattan
        if heuristic == "hamming":
            self._fast_heuristic = fast_hamming
            return self._hamming
        if heuristic == "linear_conflict":
            self._fast_heuristic = fast_linear_conflict
            return self._linear_conflict
        raise InvalidHeuristic

    def _compute_targets(self):
        self._targets.append(-1)
        for i in range(1, self._size2):
            wx = np.where(self._solution == i)[0]
            self._targets.append((wx // self._size, wx % self._size))

    # Heuristics
    def _euclidian(self, array, target, coords):
        return np.sqrt((target[0] - coords[0]) ** 2 + (target[1] - coords[1]) ** 2)

    def _manhattan(self, array, target, coords):
        return fast_manhattan(target, coords)

    def _hamming(self, array, target, coords):
        return target != coords

    def _linear_conflict(self, array, target, coords):
        return fast_linear_conflict(array, self._targets, target, coords)

    def _get_score(self, array):
        score = 0
        for i in range(self._size):
            for j in range(self._size):
                target = self._targets[array[i, j]]
                if (array[i, j]) and (i, j) != target:
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
        return (fast_get_score(new_arr, self._targets, self._fast_heuristic) + node[3] * self._search, node[1] + [0], new_arr, node[3] + 1)

    def _slide_up(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx - 1,
                                 wy] = new_arr[wx - 1, wy], new_arr[wx, wy]
        return (fast_get_score(new_arr, self._targets,  self._fast_heuristic) + node[3] * self._search, node[1] + [1], new_arr, node[3] + 1)

    def _slide_right(self, node):
        """
            return tuple (score, new_puzzle)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx,
                                 wy + 1] = new_arr[wx, wy + 1], new_arr[wx, wy]
        return (fast_get_score(new_arr, self._targets,  self._fast_heuristic) + node[3] * self._search, node[1] + [2], new_arr, node[3] + 1)

    def _slide_down(self, node):
        """
            return tuple (score, moves, new_puzzle, number of moves)
        """
        wx, wy = self._get_zero(node[2])
        new_arr = node[2].copy()
        new_arr[wx, wy], new_arr[wx + 1,
                                 wy] = new_arr[wx + 1, wy], new_arr[wx, wy]
        return (fast_get_score(new_arr, self._targets,  self._fast_heuristic) + node[3] * self._search, node[1] + [3], new_arr, node[3] + 1)

    def _astar(self, heap):
        max_state = 0
        while len(heap) != 0:
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

    def _ida(self, heap):
        max_state = 0
        depth_heap = None
        depth = fast_get_score(self._puzzle, self._targets, self._fast_heuristic)
        while True:
            min_cost = 10000
            del depth_heap
            depth_heap = heap.copy()
            while len(depth_heap):
                max_state = max(max_state, len(depth_heap))
                node = heapq.heappop(depth_heap)
                if np.all(self._solution == node[2]):
                    return (node, max_state, len(depth_heap))
                if node[0] > depth:
                    min_cost = node[0] if node[0] < min_cost else min_cost
                    continue
                wx, wy = self._get_zero(node[2])
                if (wy > 0):
                    heapq.heappush(depth_heap, self._slide_left(node))
                if (wy < self._size - 1):
                    heapq.heappush(depth_heap, self._slide_right(node))
                if (wx > 0):
                    heapq.heappush(depth_heap, self._slide_up(node))
                if (wx < self._size - 1):
                    heapq.heappush(depth_heap, self._slide_down(node))
            depth += 1
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
        print(puz)
        for move in solution[0][1]:
            print(self._directions[move])
            puz = self.slide(puz, move)
            print(puz)

    def solve(self):
        self._solvable()
        exit(1)
        # open set is the heap of investigated states
        heapq.heappush(self._open_set, (self._get_score(
            self._puzzle), [], self._puzzle, 0))
        # a = self._astar(self._open_set)
        a = self._algo(self._open_set)
        return a
