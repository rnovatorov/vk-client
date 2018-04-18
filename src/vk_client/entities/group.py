import attr
from vk_client import validators
from vk_client.entities._base import Entity, entity_manager


@attr.s
class Group(Entity):

    id = attr.ib(validator=validators.negative)


@attr.s
class GroupManager(entity_manager(Group)):
    pass
