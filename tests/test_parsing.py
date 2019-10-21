#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from npuzzle import Parser, Solver

class TestParsing(unittest.TestCase):

    def test_parsing_ko(self):
        for i in range(1, 6):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ko_{}.puz'.format(i))) as input_file:
                parse = Parser()
                try:
                    while parse.push(input_file.readline()):
                        pass
                except:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)

    def test_parsing_ok(self):
        for i in range(1, 6):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'puzzles/ok_{}.puz'.format(i))) as input_file:
                parse = Parser()
                try:
                    while parse.push(input_file.readline()):
                        pass
                except:
                    self.assertTrue(False)
                else:
                    self.assertTrue(True)
