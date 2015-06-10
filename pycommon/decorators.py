import functools
import os

def memoize(obj):
    """
    Decorator that caches method calls automagically. Use this decorator on any method and the return values will be
    cached.
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        """ The wrapper function """
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

def chdir(newdir):
    def wrap(func):
        def wrapped_func(*args, **kwargs):
            olddir = os.getcwd()
            try:
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                os.chdir(newdir)
                return func(*args, **kwargs)
            finally:
                os.chdir(olddir)
        return wrapped_func
    return wrap
