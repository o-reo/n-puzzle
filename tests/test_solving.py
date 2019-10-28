#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest
import numpy as np
import time
import subprocess

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
            solver.solve()
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

    def test_slide(self):
        res = parse_array(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/s_1.puz'))
        sol = Solver(res)
        res = sol._slide_left([0, [], res, 0, 0])
        self.assertTrue(np.array_equal(res[2], np.array([[7, 8, 3], [4, 1, 5], [2, 0, 6]])))
        res = sol._slide_up([0, [], res[2], 0, 0])
        self.assertTrue(np.array_equal(res[2], np.array([[7, 8, 3], [4, 0, 5], [2, 1, 6]])))

    def test_unsolvable(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_1.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_2.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable3(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_3.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable4(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_4.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable5(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_5.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable6(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_6.puz'), NotSolvable)
        self.assertTrue(res)

    def test_unsolvable7(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/u_7.puz'), NotSolvable)
        self.assertTrue(res)

    def test_solvable_stored(self):
        print()
        tot_time, tot_max_state, tot_state, tot_move = 0, 0, 0, 0
        for i in range(1, 100):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/s_{}.puz'.format(i))) as input_file:
                parser = Parser()
                lines = input_file.readlines()
                for line in lines:
                    parser.push(line)
                actual_time = time.time()
                solver = Solver(parser.numpize())
                temp = solver.solve()
                end_time = time.time()
            tot_move += len(temp[0][1])
            tot_max_state += temp[1]
            tot_state += temp[2]
            tot_time += (end_time - actual_time)
        print("On stored puzzle :")
        print("Average move", tot_move / 99)
        print("Average time spent :", tot_time / 99)
        print("Average state opened:", tot_state / 99)
        print("Average max state opened:", tot_max_state / 99)

    def test_solvable_random(self):
        print()
        tot_time, tot_max_state, tot_state, tot_move = 0, 0, 0, 0
        for i in range(1, 100):
            lines = subprocess.check_output(['/usr/bin/python', 'resources/res_npuzzle-gen.py', '-s', '3']).decode('utf-8')
            lines = [line if line else '#' for line in lines.split('\n')]
            parser = Parser()
            for line in lines:
                parser.push(line)
            actual_time = time.time()
            solver = Solver(parser.numpize())
            temp = solver.solve()
            end_time = time.time()
            tot_move += len(temp[0][1])
            tot_max_state += temp[1]
            tot_state += temp[2]
            print(end_time - actual_time)
            tot_time += (end_time - actual_time)
        print("On random puzzle :")
        print("Average move", tot_move / 99)
        print("Average time spent :", tot_time / 99)
        print("Average state opened:", tot_state / 99)
        print("Average max state opened:", tot_max_state / 99)
