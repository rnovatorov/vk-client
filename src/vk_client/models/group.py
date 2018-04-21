import attr
from more_itertools import one
from cached_property import cached_property
from vk_client import config, validators
from vk_client.utils import offset_range
from vk_client.models._base import Model, model_manager


@attr.s
class Group(Model):

    id = attr.ib(validator=validators.negative)

    @property
    def name(self):
        return self._data["name"]

    @property
    def screen_name(self):
        return self._data["screen_name"]

    @property
    def posts(self):
        return self._vk.Post.from_owner(self)

    @cached_property
    def _data(self):
        response = self._vk.api.groups.getById(group_id=-self.id)
        return one(response)


@attr.s
class GroupManager(model_manager(Group)):

    def from_search(self, q):
        response = self._vk.api.groups.search(count=1, q=q)
        chunks = offset_range(0, response["count"], config.SEARCH_CHUNK_SIZE)
        for offset, chunk_size in chunks:
            response = self._vk.api.groups.search(
                offset=offset,
                count=chunk_size,
                q=q
            )
            for item in response["items"]:
                yield self(
                    id=-item["id"]
                )

    def from_user(self, user):
        response = self._vk.api.groups.get(user_id=user.id, count=1)
        chunks = offset_range(0, response["count"], config.SEARCH_CHUNK_SIZE)
        for offset, chunk_size in chunks:
            response = self._vk.api.groups.get(
                user_id=user.id,
                offset=offset,
                count=chunk_size
            )
            for item in response["items"]:
                yield self(
                    id=-item
                )
