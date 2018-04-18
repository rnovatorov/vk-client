import attr
from vk_client import validators
from vk_client.entities._base import Entity, entity_manager


@attr.s
class Post(Entity):

    id = attr.ib(validator=validators.positive)
    owner_id = attr.ib(validator=validators.not_zero)

    @property
    def owner_is_user(self):
        return self.owner_id > 0

    @property
    def owner_is_group(self):
        return self.owner_id < 0

    @property
    def owner(self):
        if self.owner_is_user:
            return self._vk.User(id=self.owner_id)
        elif self.owner_is_group:
            return self._vk.Group(id=self.owner_id)
        else:
            raise RuntimeError("Unreachable")


@attr.s
class PostManager(entity_manager(Post)):
    pass
