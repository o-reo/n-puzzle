#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .exception import *

class Parser:

    def __init__(self):
        self.size = -1
        self.array = []

    def get_size(self, line):
        if len(line.split()) != 1:
            raise SizeNotFound
        if line.isdigit():
            self.size = int(line)
        else:
            raise NotAnInteger

    def get_puzzle(self, line):
        nbr_integer = 0
        integers = line.split()
        if len(integers) != self.size:
            raise WrongColumnCount
        for integer in integers:
            if not integer.isdigit():
                raise NotAnInteger
            else:
                self.array.append(int(integer))

    def push(self, line):
        if not line:
            raise EmptyLine
        line = line.strip()
        line = line.split('#')[0]
        # this line is a comment or is empty
        if not line:
            return
        # size must be parsed
        if self.size == -1:
            self.get_size(line)
        else:
            # parse a puzzle line
            self.get_puzzle(line)

    def build(self):
        if self.size == -1:
            raise SizeNotFound
        if self.size < 3:
            raise SizeTooSmall
        if len(self.array) != self.size ** 2:
            raise WrongLineCount
        check = list(range(0, self.size ** 2))
        sorted_arr = self.array.copy()
        sorted_arr.sort()
        if sorted_arr != check:
            raise WrongNumbering
        return self.array