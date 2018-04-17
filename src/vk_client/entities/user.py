import attr
from vk_client.entities._base import Entity, entity_manager


@attr.s
class User(Entity):

    id = attr.ib()


@attr.s
class UserManager(entity_manager(User)):
    pass
