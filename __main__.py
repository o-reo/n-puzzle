#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src import Parser
from module import puzzlesolver
import argparse
import cProfile

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", "-a", type=str,
                        help="algorithm to use", default="astar")
    parser.add_argument("--heuristic", "-H", type=str,
                        help="heuristic to use", default="linear_conflict")
    parser.add_argument("--search", "-s", type=str,
                        help="heuristic to use", default="uniform")
    parser.add_argument("--image", "-i", type=str,
                        help="image to use for the user interface", default=None)
    parser.add_argument("--display", "-d",
                        help="curses user interface", action="store_true")
    return parser.parse_args()

def print_stats(sol):
    print("Coups : {}".format(len(sol[0][1])))
    print("Etats simultanés : {}".format(sol[1]))
    print("Etats ouverts : {}".format(sol[2]))

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
    array = parser.build()
    solution = puzzlesolver(array)
    print(solution)
    # if args.display:
    #     import arcade
    #     from gui import PuzzleInterface
    #     puz_ui = PuzzleInterface()
    #     puz_ui.setup(solution, args.image)
    #     arcade.run()
    #     exit()
    # else:
        # print_stats(a)
