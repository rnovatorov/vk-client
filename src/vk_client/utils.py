from six.moves import range
from functools import wraps
from itertools import count
from more_itertools import chunked


def with_offset(step=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **fkwargs):
            init_offset = fkwargs.pop("offset", 0)
            for offset in count(start=init_offset, step=step):
                rv = func(*args, offset=offset, step=step, **fkwargs)
                if rv:
                    for i in rv:
                        yield i
                else:
                    raise StopIteration
        return wrapper
    return decorator


def offset_range(start, stop, step):
    chunks = chunked(range(start, stop), step)
    for i, chunk in enumerate(chunks):
        yield i * step, len(chunk)
