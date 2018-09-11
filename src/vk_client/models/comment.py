import arrow
import more_itertools as mit
import cached_property
from vk_client import config, enums, utils, validators
from vk_client.models import _base, _mixins


class Comment(
    _base.Model,
    _mixins.Authored,
    _mixins.Likable
):
    _likable_type = enums.LikableType.COMMENT

    def __init__(self, vk, id, author_id, owner_id, post_id, post_author_id):
        assert validators.positive(id)
        assert validators.not_zero(author_id)
        assert validators.not_zero(owner_id)
        assert validators.positive(post_id)
        assert validators.not_zero(post_author_id)

        super(Comment, self).__init__(vk)

        self._id = id
        self._author_id = author_id
        self._owner_id = owner_id
        self._post_id = post_id
        self._post_author_id = post_author_id

    def __hash__(self):
        return hash((self.full_id, self._post_id))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                other.full_id == self.full_id
                and
                other._post_id == self._post_id
            )

        return NotImplemented

    def __repr__(self):
        return "Comment({})".format(self.full_id)

    @property
    def post(self):
        return self._vk.Post.from_comment(self)

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def text(self):
        return self._data["text"]

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.wall.getComments(
            owner_id=self._owner_id,
            post_id=self._post_id,
            start_comment_id=self.id,
            need_likes=True,
            count=1
        )
        return mit.one(response["items"])


class CommentManager(_base.ModelManager):

    _model = Comment

    @utils.flattened()
    @utils.exhausted(step=config.WALL_CHUNK_SIZE_MAX)
    def from_post(self, post, offset, count):
        return [
            self(
                id=item["id"],
                author_id=item["from_id"],
                owner_id=post.owner_id,
                post_id=post.id,
                post_author_id=post.author_id
            )
            for item in self._vk.api.wall.getComments(
                owner_id=post.owner_id,
                post_id=post.id,
                offset=offset,
                count=count
            )["items"]
        ]
