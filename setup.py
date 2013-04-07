from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from globals import APP_NAME


ext_modules = [
    Extension("world", ["world.py"]),
]

setup(
    name=APP_NAME,
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
