#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SizeNotFound(Exception):
    pass

class EmptyLine(Exception):
    pass

class SizeTooSmall(Exception):
    pass

class BadInput(Exception):
    pass

class NotAnInteger(Exception):
    pass

class WrongColumnCount(Exception):
    pass

class WrongNumbering(Exception):
    pass

class WrongLineCount(Exception):
    pass

class NotSolvable(Exception):
    pass

class InvalidHeuristic(Exception):
    pass

class InvalidSearch(Exception):
    pass
