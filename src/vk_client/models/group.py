import attr
from more_itertools import one
from cached_property import cached_property
from vk_client import config, errors, validators
from vk_client.utils import exhausted, flattened
from vk_client.models.base import Model, ModelManager


@attr.s
class Group(Model):

    id = attr.ib(validator=validators.negative)

    @property
    def name(self):
        return self._data["name"]

    @property
    def screen_name(self):
        return self._data["screen_name"]

    def get_posts(self):
        return self._vk.Post.from_owner(self)

    @cached_property
    def _data(self):
        response = self._vk.api.groups.getById(group_id=-self.id)
        try:
            return one(response)
        except ValueError:
            raise errors.NotFound(self)


@attr.s
class GroupManager(ModelManager):

    _model_class = Group

    @flattened()
    @exhausted(step=config.SEARCH_CHUNK_SIZE)
    def from_search(self, q, offset, count):
        return [
            self(
                id=-item["id"]
            )
            for item in self._vk.api.groups.search(
                offset=offset,
                count=count,
                q=q
            )["items"]
        ]

    @flattened()
    @exhausted(step=config.SEARCH_CHUNK_SIZE)
    def from_user(self, user, offset, count):
        return [
            self(
                id=-item
            )
            for item in self._vk.api.groups.get(
                user_id=user.id,
                offset=offset,
                count=count
            )["items"]
        ]
