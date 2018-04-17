import attr
from vk_client.entities._base import Entity, entity_manager


@attr.s
class Link(Entity):

    id = attr.ib()
    url = attr.ib()
    title = attr.ib()
    description = attr.ib()
    photo_50 = attr.ib()
    photo_100 = attr.ib()
    photo_200 = attr.ib()


@attr.s
class LinkManager(entity_manager(Link)):

    def get(self, count=50):
        response = self.vk.api.fave.getLinks(
            count=count
        )
        return [
            self(
                id=item["id"],
                url=item["url"],
                title=item["title"],
                description=item["description"],
                photo_50=item["photo_50"],
                photo_100=item["photo_100"],
                photo_200=item["photo_200"]
            )
            for item in response["items"]
        ]
