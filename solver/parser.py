#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_int(line):
    for char in line:
        if char not in "0123456789":
            return 0
    return 1

class SizeNotFound(Exception):
    pass

class SizeTooSmall(Exception):
    pass

class BadInput(Exception):
    pass

class NotIntegerFound(Exception):
    pass

class WrongNumberOfInteger(Exception):
    pass

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
        line = line.split('#')[0]
        if end:
            if self.size == -1:
                raise SizeNotFound
            if self.size < 3:
                raise SizeTooSmall
            if self.size != self.nbr_line:
                raise BadInput
        if self.size == -1:
            self.get_size(line)
        else:
            self.get_puzzle(line)

if __name__ == "__main__":
    parser = Parser()
    end = False
    while (True):
        try:
            line = input()
        except EOFError:
            end = True 
        parser.push(line, end)
        if parser.size == parser.nbr_line:
            try:
                line = input()
            except EOFError:
                break
            raise BadInput
    print("puzzle : ", parser.array)
    print("size : ", parser.size)
