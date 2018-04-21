import attr
import arrow
from more_itertools import one
from cached_property import cached_property
from vk_client import config
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.models._base import Model, model_manager
from vk_client.models._mixins import AuthoredMixin, LikableMixin, OwnedMixin


@attr.s
class Post(
    Model,
    AuthoredMixin,
    LikableMixin,
    OwnedMixin
):
    LIKABLE_TYPE = LikableType.POST

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def text(self):
        return self._data["text"]

    def get_comments(self):
        return self._vk.Comment.from_post(self)

    @cached_property
    def _data(self):
        response = self._vk.api.wall.getById(posts=self.full_id)
        return one(response)


@attr.s
class PostManager(model_manager(Post)):

    def from_owner(self, owner):
        response = self._vk.api.wall.get(owner_id=owner.id, count=1)
        chunks = offset_range(0, response["count"], config.WALL_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.wall.get(
                owner_id=owner.id,
                offset=offset,
                count=chunk_size
            )
            for item in response["items"]:
                yield self(
                    id=item["id"],
                    author_id=item["from_id"],
                    owner_id=item["owner_id"]
                )

    def from_comment(self, comment):
        return self(
            id=comment.post_id,
            author_id=comment.post_author_id,
            owner_id=comment.owner_id
        )

    def get_liked(self):
        response = self._vk.api.fave.getPosts(count=1)
        chunks = offset_range(0, response["count"], config.FAVE_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.fave.getPosts(
                offset=offset,
                count=chunk_size
            )
            for item in response["items"]:
                yield self(
                    id=item["id"],
                    author_id=item["from_id"],
                    owner_id=item["owner_id"]
                )
