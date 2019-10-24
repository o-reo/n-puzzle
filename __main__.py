#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import Parser, Solver
from gui import PuzzleInterface
import argparse
import cProfile
import sys
import arcade

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--heuristic", "-H", type=str,
                        help="heuristic to use", default="manhattan")
    parser.add_argument("--search", "-s", type=str,
                        help="heuristic to use", default="greedy")
    parser.add_argument("--profiling", "-p",
                        help="profiling functions", action="store_true")
    parser.add_argument("--display", "-d",
                        help="curses user interface", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
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
    if args.display:
        puz_ui = PuzzleInterface()
        puz_ui.setup(solver, a)
        arcade.run()
    else:
        print("Coups : {}".format(len(a[0][1])))
        print("Etats simultanés : {}".format(a[1]))
        print("Etats ouverts : {}".format(a[2]))
        solver.print_solution(a)
