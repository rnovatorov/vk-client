import more_itertools as mit
import cached_property
from vk_client import config, errors, utils, validators
from vk_client.models import _base, _mixins


class User(
    _base.Model,
    _mixins.HasId
):
    def __init__(self, vk, id):
        assert validators.positive(id)

        super(User, self).__init__(vk)

        self._id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.id == self.id

        return NotImplemented

    def __repr__(self):
        return "User({})".format(self.id)

    @property
    def first_name(self):
        return self._data["first_name"]

    @property
    def last_name(self):
        return self._data["last_name"]

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_posts(self):
        return self._vk.Post.from_owner(self)

    def get_groups(self):
        return self._vk.Group.from_user(self)

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.users.get(user_ids=self.id)
        try:
            return mit.one(response)
        except ValueError:
            raise errors.NotFound(self)


class UserManager(_base.ModelManager):

    _model = User

    @property
    def current(self):
        response = self._vk.api.users.get()
        return self(
            id=mit.one(response)["id"]
        )

    @utils.flattened()
    @utils.exhausted(step=config.FAVE_CHUNK_SIZE_MAX)
    def from_search(self, q, offset, count):
        return [
            self(
                id=item["id"]
            )
            for item in self._vk.api.users.search(
                offset=offset,
                count=count,
                q=q
            )["items"]
        ]

    def from_screen_name(self, screen_name):
        response = self._vk.api.users.get(user_ids=screen_name)
        try:
            return self(
                id=mit.one(response)["id"]
            )
        except ValueError:
            raise errors.NotFound(self)
