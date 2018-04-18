import attr
from vk_client.utils import offset_range
from vk_client.entities._base import entity_manager


CHUNK_SIZE_DEFAULT = 50
CHUNK_SIZE_MAX = 100


@attr.s
class PhotoFaveManagerMixin(object):

    def count_photos(self):
        response = self._vk.api.fave.getPhotos(count=1)
        return response["count"]

    def get_photos(self, count=CHUNK_SIZE_DEFAULT):
        for offset, chunk_size in offset_range(0, count, CHUNK_SIZE_MAX):
            response = self._vk.api.fave.getPhotos(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self._vk.Photo(
                    id=item["id"],
                    owner_id=item["owner_id"]
                )


@attr.s
class PostFaveManagerMixin(object):

    def count_posts(self):
        response = self._vk.api.fave.getPosts(count=1)
        return response["count"]

    def get_posts(self, count=CHUNK_SIZE_DEFAULT):
        for offset, chunk_size in offset_range(0, count, CHUNK_SIZE_MAX):
            response = self._vk.api.fave.getPosts(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self._vk.Post(
                    id=item["id"],
                    owner_id=item["owner_id"]
                )


@attr.s
class FaveManager(
    entity_manager(),
    PhotoFaveManagerMixin,
    PostFaveManagerMixin
):
    pass
