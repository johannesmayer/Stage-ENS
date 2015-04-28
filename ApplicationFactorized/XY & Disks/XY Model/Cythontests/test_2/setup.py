from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


ext_modules = [Extension("cluster_functions", ["cluster_functions.pyx"],include_dirs=[numpy.get_include()])]

setup(
  name = 'cluster_functions',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

#python ecmc_hard_spheres_for_johannes_setup.py build_ext --inplace 
