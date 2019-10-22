#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import Parser, BadInput

if __name__ == "__main__":
    parser = Parser()
    line = None
    while (True):
        try:
            line = input()
            parser.push(line)
        except EOFError:
            break
    print("puzzle : ", parser.build())
