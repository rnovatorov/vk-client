import attr
from vk_client import validators, errors


def make_likable_mixin(likable_type):

    @attr.s
    class LikableMixin(object):

        id = attr.ib(validator=validators.positive)
        owner_id = attr.ib(validator=validators.not_zero)

        def like(self):
            self._vk.api.likes.add(
                type=likable_type.value,
                owner_id=self.owner_id,
                item_id=self.id
            )

        def unlike(self):
            self._vk.api.likes.delete(
                type=likable_type.value,
                owner_id=self.owner_id,
                item_id=self.id
            )

    return LikableMixin


@attr.s
class OwnedMixin(object):

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
            raise errors.Unreachable
