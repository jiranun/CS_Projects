from distutils.core import setup
from Cython.Build import cythonize
import numpy


setup(
    name='Utilities for Kernel-based Objec Tracking',
    ext_modules=cythonize("kotutilities.pyx"),
    include_dirs=[numpy.get_include()]
)
