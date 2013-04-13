# Imports, sorted alphabetically.

# Python packages
from Cython.Distutils import build_ext
from distutils.core import setup
from distutils.extension import Extension

# Third-party packages
# Nothing for now...

# Modules from this project
import globals as G


ext_modules = [
    Extension(name, [name + '.py']) for name in (
        'blocks', 'cameras', 'controllers', 'crafting', 'entity', 'gui', 'inventory', 'items',
        'manager', 'model', 'nature', 'player', 'savingsystem', 'sounds', 'terrain', 'world',
    )
]

setup(
    name=G.APP_NAME,
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
