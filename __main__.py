#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import *
import argparse
import time
import cProfile
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--heuristic", "-H", type=str, help="heuristic to use", default="manhattan")
    parser.add_argument("--search", "-s", type=str, help="heuristic to use", default="greedy")
    parser.add_argument("--profiling", "-p", help="profiling functions", action="store_true")

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
    if args.profiling:
    # PROFILING
        def solving():
            print(solver.solve())
        cProfile.run('solving()', sort='tottime')
        sys.exit()
    a = solver.solve()
    b2 = time.time()
    print(b2-b1)
    print("coups a faire : {}".format(a[0][1]))
    print("nombre coups a faire : {}".format(len(a[0][1])))
    print("nombre etat ouvert en meme temps max : {}".format(a[1]))
    print("nombre etat ouvert : {}".format(a[2]))

    