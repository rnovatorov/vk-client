import more_itertools as mit
import cached_property
from vk_client import config, enums, errors, utils, validators
from vk_client.models import _base, _mixins


class Photo(
    _base.Model,
    _mixins.Likable
):
    _likable_type = enums.LikableType.PHOTO

    def __init__(self, vk, id, owner_id):
        assert validators.positive(id)
        assert validators.not_zero(owner_id)

        super(Photo, self).__init__(vk)

        self._id = id
        self._owner_id = owner_id

    def __hash__(self):
        return hash(self.full_id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.full_id == self.full_id

        return NotImplemented

    def __repr__(self):
        return "Photo({})".format(self.full_id)

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.photos.getById(
            photos=self.full_id,
            extended=True
        )
        try:
            return mit.one(response)
        except ValueError:
            raise errors.NotFound(self)


class PhotoManager(_base.ModelManager):

    _model = Photo

    @utils.flattened()
    @utils.exhausted(step=config.FAVE_CHUNK_SIZE_MAX)
    def get_liked(self, offset, count):
        return [
            self(
                id=item["id"],
                owner_id=item["owner_id"]
            )
            for item in self._vk.api.fave.getPhotos(
                offset=offset,
                count=count
            )["items"]
        ]
