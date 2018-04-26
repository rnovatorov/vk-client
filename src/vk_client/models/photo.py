import attr
from more_itertools import one
from cached_property import cached_property
from vk_client import config
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.models.base import Model, model_manager
from vk_client.models.mixins import LikableMixin, OwnedMixin


@attr.s
class Photo(
    Model,
    LikableMixin,
    OwnedMixin
):
    LIKABLE_TYPE = LikableType.PHOTO

    @cached_property
    def _data(self):
        response = self._vk.api.photos.getById(
            photos=self.full_id,
            extended=True
        )
        return one(response)


@attr.s
class PhotoManager(model_manager(Photo)):

    def get_liked(self):
        response = self._vk.api.fave.getPhotos(count=1)
        chunks = offset_range(0, response["count"], config.FAVE_CHUNK_SIZE_MAX)
        for offset, chunk_size in chunks:
            response = self._vk.api.fave.getPhotos(
                offset=offset,
                count=chunk_size
            )
            for item in response["items"]:
                yield self(
                    id=item["id"],
                    owner_id=item["owner_id"]
                )
