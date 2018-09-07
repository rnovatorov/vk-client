import functools
import itertools
from six import integer_types
from six.moves import range
import more_itertools as mit


flattened = mit.make_decorator(mit.flatten)


def exhausted(step=1):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = kwargs.pop("offset", 0)
            counter = itertools.count(start=start, step=step)

            def generator():
                offset = next(counter)
                return func(*args, offset=offset, count=step, **kwargs)

            return iter(generator, [])

        return wrapper

    return decorator


def offset_range(start, stop, step):
    chunks = mit.chunked(range(start, stop), step)
    for i, chunk in enumerate(chunks):
        yield i * step, len(chunk)


def is_int(value):
    return isinstance(value, integer_types)
