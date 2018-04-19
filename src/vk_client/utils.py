import attr
from six.moves import range
from more_itertools import chunked


@attr.s
class PartialSelf(object):

    receiver = attr.ib()

    def __get__(self, instance, owner):
        return self.receiver(instance)


def offset_range(start, stop, step):
    chunks = chunked(range(start, stop), step)
    for i, chunk in enumerate(chunks):
        yield i * step, len(chunk)
