from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("ecmc_hard_spheres_for_johannes", ["ecmc_hard_spheres_for_johannes.pyx"])]

setup(
  name = 'ecmc_hard_spheres_for_johannes_main',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

#python ecmc_hard_spheres_for_johannes_setup.py build_ext --inplace 
