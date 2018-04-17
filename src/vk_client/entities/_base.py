import attr


@attr.s
class Entity(object):

    vk = attr.ib(repr=False)


def entity_manager(entity_class):

    @attr.s
    class EntityManager(object):

        vk = attr.ib()

        def __call__(self, *args, **kwargs):
            return entity_class(self.vk, *args, **kwargs)

    return EntityManager
