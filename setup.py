from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(['npuzzle/faster_functions.pyx'], annotate=True),        # enables generation of the html annotation file
)
