#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest
import numpy as np

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
        except error_code:
            return True
        except Exception as e:
            return False
        return False

def try_ok(file_name):
    parser = Parser()
    with open(file_name) as input_file:
        lines = input_file.readlines()
        for line in lines:
            parser.push(line)
        return parser.build()

class TestParsing(unittest.TestCase):

    def test_parsing_empty(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_0.puz'), EmptyLine)
        self.assertTrue(res)

    def test_parsing_nosize(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_1.puz'), SizeNotFound)
        self.assertTrue(res)

    def test_parsing_toosmall(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_2.puz'), SizeTooSmall)
        self.assertTrue(res)

    def test_parsing_nosize2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_3.puz'), SizeNotFound)
        self.assertTrue(res)

    def test_parsing_wrongcolumns(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_4.puz'), WrongColumnCount)
        self.assertTrue(res)

    def test_parsing_wrongcolumns2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_5.puz'), WrongNumbering)
        self.assertTrue(res)

    def test_parsing_nosize3(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_6.puz'), NotAnInteger)
        self.assertTrue(res)

    def test_parsing_toosmall2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_7.puz'), SizeTooSmall)
        self.assertTrue(res)

    def test_parsing_badinput(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_8.puz'), WrongColumnCount)
        self.assertTrue(res)

    def test_parsing_badinput2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_9.puz'), WrongColumnCount)
        self.assertTrue(res)

    def test_parsing_notinteger(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_10.puz'), NotAnInteger)
        self.assertTrue(res)

    def test_parsing_WrongIntegerList(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_11.puz'), WrongNumbering)
        self.assertTrue(res)

    def test_parsing_nozero(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_12.puz'), WrongNumbering)
        self.assertTrue(res)

    def test_parsing_ok_1(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_1.puz'))
        self.assertTrue(np.all(res == np.array([0, 7, 8, 2, 5, 4, 6, 3, 1])))

    def test_parsing_ok_2(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_2.puz'))
        self.assertTrue(np.all(res == np.array([0, 3, 4, 1, 2, 5, 6, 7, 8])))

    def test_parsing_ok_3(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_3.puz'))
        self.assertTrue(np.all(res == np.array([4, 3, 2, 1, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])))

    def test_parsing_ok_4(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_4.puz'))
        self.assertTrue(np.all(res == np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])))

    def test_parsing_ok_5(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_5.puz'))
        self.assertTrue(np.all(res == np.array([4, 1, 2, 3, 5, 0, 6, 7, 8])))
