#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import *
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--heuristic", "-H", type=str, help="heuristic to use", default="manhattan")

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
    a = solver.solve()
    print("coups a faire : {}".format(a[0][1]))
    print("nombre coups a faire : {}".format(len(a[0][1])))
    print("nombre etat ouvert max : {}".format(a[1]))
    print("nombre etat ouvert : {}".format(a[2]))
    print(a)
