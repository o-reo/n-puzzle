from distutils.core import setup
from distutils.extension import Extension
import numpy as np

extensions = [
    Extension("puzzlesolver", sources = ["module/def.cpp"], include_dirs = []),    
]

setup(
    name = "npuzzle",
    ext_modules=extensions,
)
