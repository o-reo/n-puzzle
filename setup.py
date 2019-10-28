from distutils.core import setup
from distutils.extension import Extension
import numpy as np

extensions = [
    Extension("puzzlesolver", sources = ["module/def.cpp", "module/solver.cpp"], include_dirs = ["module/"], extra_compile_args=["-std=c++1z"]),    
]

setup(
    name = "npuzzle",
    ext_modules=extensions,

)
