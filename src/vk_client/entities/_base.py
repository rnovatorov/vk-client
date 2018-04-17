import attr


@attr.s
class Entity(object):

    _vk = attr.ib(repr=False)


def entity_manager(entity_class=None):

    @attr.s
    class EntityManager(object):

        _vk = attr.ib(repr=False)

        if entity_class is not None:
            def __call__(self, *args, **kwargs):
                return entity_class(self._vk, *args, **kwargs)

    return EntityManager
