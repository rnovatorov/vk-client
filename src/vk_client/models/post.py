import arrow
import more_itertools as mit
import cached_property
from vk_client import config, enums, errors, utils, validators
from vk_client.models import _base, _mixins


class Post(
    _base.Model,
    _mixins.Authored,
    _mixins.Likable
):
    _likable_type = enums.LikableType.POST

    def __init__(self, vk, id, author_id, owner_id):
        assert validators.positive(id)
        assert validators.not_zero(author_id)
        assert validators.not_zero(owner_id)

        super(Post, self).__init__(vk)

        self._id = id
        self._author_id = author_id
        self._owner_id = owner_id

    def __hash__(self):
        return hash(self.full_id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.full_id == self.full_id

        return NotImplemented

    def __repr__(self):
        return "Post({})".format(self.full_id)

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

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.wall.getById(posts=self.full_id)
        try:
            return mit.one(response)
        except ValueError:
            raise errors.NotFound(self)


class PostManager(_base.ModelManager):

    _model = Post

    @utils.flattened()
    @utils.exhausted(step=config.WALL_CHUNK_SIZE_MAX)
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

    @utils.flattened()
    @utils.exhausted(step=config.FAVE_CHUNK_SIZE_MAX)
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
