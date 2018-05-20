from functools import wraps
from itertools import count
from six.moves import range
from more_itertools import chunked, flatten, make_decorator


flattened = make_decorator(flatten)


def exhausted(step=1):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = kwargs.pop("offset", 0)
            counter = count(start=start, step=step)

            def generator():
                offset = next(counter)
                return func(*args, offset=offset, count=step, **kwargs)

            return iter(generator, [])

        return wrapper

    return decorator


def offset_range(start, stop, step):
    chunks = chunked(range(start, stop), step)
    for i, chunk in enumerate(chunks):
        yield i * step, len(chunk)
