#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import *

if __name__ == "__main__":
    parser = Parser()
    line = None
    while (True):
        try:
            line = input()
            parser.push(line)
        except EOFError:
            break
    parser.build()
    solver = Solver(parser.numpize())
