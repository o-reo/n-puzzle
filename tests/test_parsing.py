#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from npuzzle import *

def try_error(file_name, error_code):
    with open(file_name) as input_file:
        parse = Parser()
        try:
            line = input_file.readline()
            while line:
                parse.push(line)
                line = input_file.readline()
            parse.build()
        except error_code:
            return True
        else:
            return False

def try_ok(file_name):
    with open(file_name) as input_file:
        parse = Parser()
        line = input_file.readline()
        while line:
            parse.push(line)
            line = input_file.readline()
        return parse.build()

class TestParsing(unittest.TestCase):

    def test_parsing_empty(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_0.puz'), EmptyFile)
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
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_4.puz'), WrongNumberOfInteger)
        self.assertTrue(res)

    def test_parsing_wrongcolumns(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_5.puz'), DuplicatesFound)
        self.assertTrue(res)

    def test_parsing_nosize3(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_6.puz'), SizeNotFound)
        self.assertTrue(res)

    def test_parsing_toosmall2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_7.puz'), SizeTooSmall)
        self.assertTrue(res)

    def test_parsing_badinput(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_8.puz'), BadInput)
        self.assertTrue(res)

    def test_parsing_badinput2(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_9.puz'), BadInput)
        self.assertTrue(res)

    def test_parsing_notinteger(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_10.puz'), NotIntegerFound)
        self.assertTrue(res)

    def test_parsing_WrongIntegerList(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_11.puz'), WrongIntegerList)
        self.assertTrue(res)

    def test_parsing_NoZero(self):
        res = try_error(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_12.puz'), ZeroNotFound)
        self.assertTrue(res)

    def test_parsing_ok_1(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_1.puz'))
        self.assertEqual(res, [0, 7, 8, 2, 5, 4, 6, 3, 1])

    def test_parsing_ok_2(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_2.puz'))
        self.assertEqual(res, [0, 3, 4, 1, 2, 5, 6, 7, 8])

    def test_parsing_ok_3(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_3.puz'))
        self.assertEqual(res, [4, 3, 2, 1, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

    def test_parsing_ok_4(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_4.puz'))
        self.assertEqual(res, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

    def test_parsing_ok_5(self):
        res = try_ok(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_5.puz'))
        self.assertEqual(res, [4, 1, 2, 3, 5, 0, 6, 7, 8])