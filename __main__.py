#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import Parser, BadInput, EmptyFile

if __name__ == "__main__":
    parser = Parser()
    end = False
    line = None
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
