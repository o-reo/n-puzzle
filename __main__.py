#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import *
import argparse
import time
import cProfile

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--heuristic", "-H", type=str, help="heuristic to use", default="manhattan")
    parser.add_argument("--search", "-s", type=str, help="heuristic to use", default="greedy")

    return parser.parse_args()

if __name__ == "__main__":
    b1 = time.time()
    args = get_args()
    parser = Parser()
    line = None
    while (True):
        try:
            line = input()
            parser.push(line)
        except EOFError:
            break
    parser.build()
    solver = Solver(parser.numpize(), args)
    # cProfile.run("solver.solve()")
    print(solver.solve())
