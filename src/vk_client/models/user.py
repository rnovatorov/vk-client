import attr
from more_itertools import one
from cached_property import cached_property
from vk_client import config, validators
from vk_client.utils import offset_range
from vk_client.models._base import Model, model_manager


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
        return one(response)


@attr.s
class UserManager(model_manager(User)):

    def from_search(self, q):
        response = self._vk.api.users.search(count=1, q=q)
        chunks = offset_range(0, response["count"], config.SEARCH_CHUNK_SIZE)
        for offset, chunk_size in chunks:
            response = self._vk.api.users.search(
                offset=offset,
                count=chunk_size,
                q=q
            )
            for item in response["items"]:
                yield self(
                    id=item["id"]
                )
