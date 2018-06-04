import attr
from more_itertools import one
from cached_property import cached_property
from vk_client import config, errors, validators
from vk_client.utils import exhausted, flattened
from vk_client.models.base import Model, ModelManager


@attr.s
class User(Model):

    id = attr.ib(validator=validators.positive)

    @property
    def first_name(self):
        return self._data["first_name"]

    @property
    def last_name(self):
        return self._data["last_name"]

    def get_posts(self):
        return self._vk.Post.from_owner(self)

    def get_groups(self):
        return self._vk.Group.from_user(self)

    @cached_property
    def _data(self):
        response = self._vk.api.users.get(user_ids=self.id)
        try:
            return one(response)
        except ValueError:
            raise errors.NotFound(self)


@attr.s
class UserManager(ModelManager):

    _model = User

    @flattened()
    @exhausted(step=config.FAVE_CHUNK_SIZE_MAX)
    def from_search(self, q, offset, count):
        return [
            self(
                id=item["id"]
            )
            for item in self._vk.api.users.search(
                offset=offset,
                count=count,
                q=q
            )["items"]
        ]

    def from_screen_name(self, screen_name):
        response = self._vk.api.users.get(user_ids=screen_name)
        try:
            return self(
                id=one(response)["id"]
            )
        except ValueError:
            raise errors.NotFound(self)
