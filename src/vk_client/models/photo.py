import attr
from vk_client import config
from vk_client.enums import LikableType
from vk_client.utils import offset_range
from vk_client.models._base import Model, model_manager
from vk_client.models._mixins import LikableMixin, OwnedMixin


@attr.s
class Photo(
    Model,
    LikableMixin,
    OwnedMixin
):
    LIKABLE_TYPE = LikableType.PHOTO


@attr.s
class PhotoManager(model_manager(Photo)):

    @property
    def liked(self):
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
