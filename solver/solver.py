#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

PY_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PY_DIR)

from parser import Parser

class Solver():
    def __init__(self, parser):
        self.n_moves = 0
        pass

    def solve(self, args):
        return False