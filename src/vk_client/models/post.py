import attr
import arrow
from more_itertools import one
from cached_property import cached_property
from vk_client import config, errors
from vk_client.enums import LikableType
from vk_client.utils import exhausted, flattened
from vk_client.models.base import Model, ModelManager
from vk_client.models.mixins import AuthoredMixin, LikableMixin, OwnedMixin


@attr.s
class Post(
    Model,
    AuthoredMixin,
    LikableMixin,
    OwnedMixin
):
    _likable_type = LikableType.POST

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def text(self):
        return self._data["text"]

    @property
    def comments_count(self):
        return self._data["comments"]["count"]

    def get_comments(self):
        return self._vk.Comment.from_post(self)

    @property
    def reposts_count(self):
        return self._data["reposts"]["count"]

    @cached_property
    def _data(self):
        response = self._vk.api.wall.getById(posts=self.full_id)
        try:
            return one(response)
        except ValueError:
            raise errors.NotFound(self)


@attr.s
class PostManager(ModelManager):

    _model = Post

    @flattened()
    @exhausted(step=config.WALL_CHUNK_SIZE_MAX)
    def from_owner(self, owner, offset, count):
        return [
            self(
                id=item["id"],
                author_id=item["from_id"],
                owner_id=item["owner_id"]
            )
            for item in self._vk.api.wall.get(
                owner_id=owner.id,
                offset=offset,
                count=count
            )["items"]
        ]

    def from_comment(self, comment):
        return self(
            id=comment.post_id,
            author_id=comment.post_author_id,
            owner_id=comment.owner_id
        )

    @flattened()
    @exhausted(step=config.FAVE_CHUNK_SIZE_MAX)
    def get_liked(self, offset, count):
        return [
            self(
                id=item["id"],
                author_id=item["from_id"],
                owner_id=item["owner_id"]
            )
            for item in self._vk.api.fave.getPosts(
                offset=offset,
                count=count
            )["items"]
        ]
