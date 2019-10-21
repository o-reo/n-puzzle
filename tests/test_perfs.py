#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from solver import Parser

class TestPerformance(unittest.TestCase):

    def test_solvable(self):
        for i in range(1, 6):
            with open('puzzles/{}.puz'.format(i)) as file:
                puz = file.read()
                puz = Parser('puzzles/1.puz')
                is_solved = puz.solve()
                self.assertTrue(is_solved and puz.n_moves < 155)

    def test_unsolvable(self):
        for i in range(1, 6):
            with open('puzzles/{}.puz'.format(i)) as file:
                puz = file.read()
                puz = Parser('puzzles/1.puz')
                self.assertFalse(puz.solve())

if __name__ == '__main__':
    unittest.main()