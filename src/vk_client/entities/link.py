import attr
from vk_client.entities._base import Entity, entity_manager


@attr.s
class Link(Entity):

    id = attr.ib()
    url = attr.ib()
    title = attr.ib()
    description = attr.ib()
    photo_50 = attr.ib()
    photo_100 = attr.ib()
    photo_200 = attr.ib()


@attr.s
class LinkManager(entity_manager(Link)):
    pass
