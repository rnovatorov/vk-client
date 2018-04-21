import attr
from six.moves import range
from itertools import count
from more_itertools import chunked


@attr.s
class PartialSelf(object):

    receiver = attr.ib()

    def __get__(self, instance, owner):
        return self.receiver(instance)


def count_to(start=0, stop=float("inf"), step=1):
    counter = count(start, step)
    for n in counter:
        if n < stop:
            yield n
        else:
            raise StopIteration


def offset_range(start, stop, step):
    chunks = chunked(range(start, stop), step)
    for i, chunk in enumerate(chunks):
        yield i * step, len(chunk)
