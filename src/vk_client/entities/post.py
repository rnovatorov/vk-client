import attr
import arrow
from more_itertools import one
from cached_property import cached_property
from vk_client import config
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.entities._base import Entity, entity_manager
from vk_client.entities._mixins import AuthoredMixin, LikableMixin, OwnedMixin


@attr.s
class Post(
    Entity,
    AuthoredMixin,
    LikableMixin,
    OwnedMixin
):
    _likable_type = attr.ib(default=LikableType.POST)

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def text(self):
        return self._data["text"]

    def get_comments(self, *args, **kwargs):
        return self._vk.Comment.from_post(self, *args, **kwargs)

    @cached_property
    def _data(self):
        response = self._vk.api.wall.getById(posts=self.full_id)
        return one(response)


@attr.s
class PostManager(entity_manager(Post)):

    def from_comment(self, comment):
        return self(
            id=comment.post_id,
            author_id=comment.post_author_id,
            owner_id=comment.owner_id
        )

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
                yield self(
                    id=item["id"],
                    author_id=item["from_id"],
                    owner_id=item["owner_id"]
                )
