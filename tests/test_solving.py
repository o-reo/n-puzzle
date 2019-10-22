#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from npuzzle import Parser, Solver

def parse_array(file_name):
    parser = Parser()
    with open(file_name) as input_file:
        lines = input_file.readlines()
        for line in lines:
            parser.push(line)
        parser.build()
        return parser.numpize()

class TestSolving(unittest.TestCase):

    def test_target(self):
        arr = parse_array(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_2.puz'))
        solver = Solver(arr)

    def test_solvable(self):
        for i in range(1, 6):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/s_{}.puz'.format(i))) as input_file:
                parse = Parser()
                while parse.push(input_file.readline()):
                    pass
                solver = Solver(None)
                is_solved = solver.solve(parse)
                self.assertTrue(is_solved and solver.n_moves < 155)

    def test_unsolvable(self):
        for i in range(1, 6):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_{}.puz'.format(i))) as input_file:
                parse = Parser()
                while parse.push(input_file.readline()):
                    pass
                solver = Solver(None)
                is_solved = solver.solve(parse)
                self.assertFalse(is_solved)