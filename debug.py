import time

# Modules from this project
import globals


def performance_info(func):
    def inner(*args, **kwargs):
        if not globals.DEBUG:
            return func(*args, **kwargs)
        start = time.time()
        out = func(*args, **kwargs)
        print('%s took %f seconds.' % (func.__name__, time.time() - start))
        return out

    return inner
