from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy

extensions = [
    Extension("faster_functions", ["npuzzle/faster_functions.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=[],
        library_dirs=[]),
]

extensions = [
    Extension("faster_functions", ["npuzzle/faster_functions.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=[],
        library_dirs=[]),
]

setup(
    name = "npuzzle",
    ext_modules=cythonize(extensions, annotate=True, language_level = 3),
)
