#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from npuzzle import *

def try_error(file_name, error_code):
    parser = Parser()
    with open(file_name) as input_file:
        try:
            lines = input_file.readlines()
            if not len(lines):
                parser.push("")
            for line in lines:
                parser.push(line)
        except error_code:
            return True
        except:
            return False
        try:
            parser.build()
            solver = Solver(parser.numpize())
        except error_code:
            return True
        except Exception as e:
            return False
        return False

def parse_array(file_name):
    parser = Parser()
    with open(file_name) as input_file:
        lines = input_file.readlines()
        for line in lines:
            parser.push(line)
        parser.build()
        return parser.numpize()

class TestSolving(unittest.TestCase):

#    def test_solvable(self):
#        for i in range(1, 6):
#            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/s_{}.puz'.format(i))) as input_file:
#                parse = Parser()
#                while parse.push(input_file.readline()):
#                    pass
#                solver = Solver(None)
#                is_solved = solver.solve(parse)
#                self.assertTrue(is_solved and solver.n_moves < 155)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_1.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_2.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_3.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_4.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_5.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_6.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_7.puz'), NotSolvable)
        self.assertTrue(res)
