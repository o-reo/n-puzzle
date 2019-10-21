#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import unittest

PY_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PY_DIR)

from solver.parser import Parser
from solver.solver import Solver

class TestPerformance(unittest.TestCase):

    def test_solvable(self):
        for i in range(1, 6):
            with open('tests/puzzles/{}.puz'.format(i)) as input_file:
                puz = Parser()
                while puz.push(input_file.readline()):
                    pass
                solver = Solver(None)
                is_solved = solver.solve(puz)
                self.assertTrue(is_solved and solver.n_moves < 155)

    def test_unsolvable(self):
        for i in range(1, 6):
            with open('tests/puzzles/u_{}.puz'.format(i)) as input_file:
                puz = Parser()
                while puz.push(input_file.readline()):
                    pass
                solver = Solver(None)
                is_solved = solver.solve(puz)
                self.assertFalse(is_solved)

if __name__ == '__main__':
    unittest.main()