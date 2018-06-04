import attr
from vk_client import validators, errors


@attr.s
class AuthoredMixin(object):

    id = attr.ib(validator=validators.positive)
    author_id = attr.ib(validator=validators.not_zero)

    @property
    def author_is_user(self):
        return self.author_id > 0

    @property
    def author_is_group(self):
        return self.author_id < 0

    @property
    def author(self):
        if self.author_is_user:
            return self._vk.User(id=self.author_id)
        elif self.author_is_group:
            return self._vk.Group(id=self.author_id)
        else:
            raise errors.Unreachable


@attr.s
class LikableMixin(object):

    _likable_type = NotImplemented

    id = attr.ib(validator=validators.positive)
    owner_id = attr.ib(validator=validators.not_zero)

    @property
    def likes_count(self):
        return self._data["likes"]["count"]

    @property
    def can_like(self):
        return not self.is_liked

    @property
    def is_liked(self):
        return bool(self._data["likes"]["user_likes"])

    def like(self):
        if self.can_like:
            self._vk.api.likes.add(
                type=self._likable_type.value,
                owner_id=self.owner_id,
                item_id=self.id
            )
            del self._data

    def unlike(self):
        if self.is_liked:
            self._vk.api.likes.delete(
                type=self._likable_type.value,
                owner_id=self.owner_id,
                item_id=self.id
            )
            del self._data


@attr.s
class OwnedMixin(object):

    id = attr.ib(validator=validators.positive)
    owner_id = attr.ib(validator=validators.not_zero)

    @property
    def full_id(self):
        return "{self.owner_id}_{self.id}".format(self=self)

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
