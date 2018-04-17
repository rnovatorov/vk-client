import attr
from vk_client.utils import offset_range
from vk_client.entities._base import entity_manager


MAX_CHUNK_SIZE = 50


@attr.s
class BookmarkManager(entity_manager()):

    def count_links(self):
        response = self._vk.api.fave.getLinks(count=1)
        return response["count"]

    def add_link(self, url, text):
        self._vk.api.fave.addLink(link=url, text=text)

    def get_links(self, count=MAX_CHUNK_SIZE):
        for offset, chunk_size in offset_range(0, count, MAX_CHUNK_SIZE):
            response = self._vk.api.fave.getLinks(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self._vk.Link(
                    id=item["id"],
                    url=item["url"],
                    title=item["title"],
                    description=item["description"],
                    photo_50=item["photo_50"],
                    photo_100=item["photo_100"],
                    photo_200=item["photo_200"]
                )

    def remove_link(self, link):
        self._vk.api.fave.removeLink(link_id=link.id)

    def count_users(self):
        response = self._vk.api.fave.getUsers(count=1)
        return response["count"]

    def add_user(self, user):
        self._vk.api.fave.addUser(user_id=user.id)

    def get_users(self, count=MAX_CHUNK_SIZE):
        for offset, chunk_size in offset_range(0, count, MAX_CHUNK_SIZE):
            response = self._vk.api.fave.getUsers(
                count=chunk_size,
                offset=offset
            )
            for item in response["items"]:
                yield self._vk.User(id=item["id"])

    def remove_user(self, user):
        self._vk.api.fave.removeUser(user_id=user.id)
