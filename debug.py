# Imports, sorted alphabetically.

# Python packages
import time

# Third-party packages
# Nothing for now...

# Modules from this project
import globals as G


def performance_info(func):
    def inner(*args, **kwargs):
        if not G.DEBUG:
            return func(*args, **kwargs)
        start = time.time()
        out = func(*args, **kwargs)
        print('%s took %f seconds.' % (func.__name__, time.time() - start))
        return out

    return inner
