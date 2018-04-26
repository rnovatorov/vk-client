import attr
import arrow
from more_itertools import one
from cached_property import cached_property
from vk_client import config, validators
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.models.base import Model, model_manager
from vk_client.models.mixins import AuthoredMixin, LikableMixin, OwnedMixin


@attr.s
class Comment(
    Model,
    AuthoredMixin,
    LikableMixin,
    OwnedMixin
):
    LIKABLE_TYPE = LikableType.COMMENT

    post_id = attr.ib(validator=validators.positive)
    post_author_id = attr.ib(validator=validators.not_zero)

    @property
    def post(self):
        return self._vk.Post.from_comment(self)

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def text(self):
        return self._data["text"]

    @cached_property
    def _data(self):
        response = self._vk.api.wall.getComments(
            owner_id=self.owner_id,
            post_id=self.post_id,
            start_comment_id=self.id,
            need_likes=True,
            count=1
        )
        return one(response["items"])


@attr.s
class CommentManager(model_manager(Comment)):

    def from_post(self, post):
        response = self._vk.api.wall.getComments(
            owner_id=post.owner_id,
            post_id=post.id,
            count=1
        )
        chunks = offset_range(0, response["count"], config.WALL_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.wall.getComments(
                owner_id=post.owner_id,
                post_id=post.id,
                offset=offset,
                count=chunk_size
            )
            for item in response["items"]:
                yield self(
                    id=item["id"],
                    author_id=item["from_id"],
                    owner_id=post.owner_id,
                    post_id=post.id,
                    post_author_id=post.author_id
                )
