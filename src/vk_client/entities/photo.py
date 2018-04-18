import attr
from vk_client import validators
from vk_client.entities._base import Entity, entity_manager


@attr.s
class Photo(Entity):

    id = attr.ib(validator=validators.positive)
    owner_id = attr.ib(validator=validators.not_zero)


@attr.s
class PhotoManager(entity_manager(Photo)):
    pass
