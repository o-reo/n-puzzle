#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npuzzle import *
import argparse
import time


def get_args():

    search = ["greedy", "uniform"]
    heuristic = ["manhattan", "euclidian", "hamming", "linear_conflict"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--heuristic", "-H", type=str, help="heuristic to use", default="manhattan")
    parser.add_argument("--search", "-s", type=str, help="search to use", default="uniform")
    args = parser.parse_args()
    
    if args.search not in search:
        raise InvalidSearch 
    if args.heuristic not in heuristic:
        raise InvalidHeuristic
    return args

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
    a = solver.solve()
    b2 = time.time()
    print(b2-b1)
    print("coups a faire : {}".format(a[0][1]))
    print("nombre coups a faire : {}".format(len(a[0][1])))
    print("nombre etat ouvert en meme temps max : {}".format(a[1]))
    print("nombre etat ouvert : {}".format(a[2]))
