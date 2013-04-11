from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import globals


ext_modules = [
    Extension(name, [name + '.py']) for name in (
        'blocks', 'cameras', 'controllers', 'crafting', 'entity', 'globals', 'gui', 'inventory', 'items',
        'manager', 'model', 'nature', 'player', 'savingsystem', 'sounds', 'terrain', 'world',
    )
]

setup(
    name=globals.APP_NAME,
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
