import attr
from vk_client import config, validators, errors
from vk_client.enums import LikableType
from vk_client.utils import offset_range
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
            raise errors.Unreachable

    def like(self):
        self._vk.api.likes.add(
            type=LikableType.POST.value,
            owner_id=self.owner_id,
            item_id=self.id
        )

    def unlike(self):
        self._vk.api.likes.delete(
            type=LikableType.POST.value,
            owner_id=self.owner_id,
            item_id=self.id
        )


@attr.s
class PostManager(entity_manager(Post)):

    def count_liked(self):
        response = self._vk.api.fave.getPosts(count=1)
        return response["count"]

    def get_liked(self, count=config.FAVE_CHUNK_SIZE_DEFAULT):
        chunks = offset_range(0, count, config.FAVE_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.fave.getPosts(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self._vk.Post(
                    id=item["id"],
                    owner_id=item["owner_id"]
                )
