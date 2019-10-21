#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exception import *

def is_int(line):
    for char in line:
        if char not in "0123456789":
            return 0
    return 1

class Parser:

    def __init__(self):
        self.size = -1
        self.nbr_line = 0
        self.array = []

    def get_size(self, line):
        if (len(line) and is_int(line)):
            self.size = int(line)

    def get_puzzle(self, line):
        nbr_integer = 0
        integers = line.split()
        if len(integers) != self.size:
            raise BadInput 
        if integers[0]:
            raise ZeroNotFound
        for integer in integers:
            if not is_int(integer):
                raise NotIntegerFound
            else:
                self.array.append(integer)
                nbr_integer += 1
        if (nbr_integer != self.size):
            raise WrongNumberOfInteger
        self.nbr_line += 1

    def push(self, line, end = False):
        if not line:
            raise EmptyFile
        line = line.split('#')[0]
        if end:
            if self.size == -1:
                raise SizeNotFound
            if self.size < 3:
                raise SizeTooSmall
            if self.size != self.nbr_line:
                raise BadInput
            for index in range(len(check[1:])):
                if check[index + 1] == check[index]:
                    raise DuplicatesFound
                if check[index + 1] != check[index] + 1:
                    raise WrongIntegerList
            return
        if self.size == -1:
            self.get_size(line)
        else:
            self.get_puzzle(line)
