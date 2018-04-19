import attr
from vk_client.api import create_api
from vk_client.utils import PartialSelf
from vk_client.entities.group import GroupManager
from vk_client.entities.photo import PhotoManager
from vk_client.entities.post import PostManager
from vk_client.entities.user import UserManager


@attr.s
class VkClient(object):

    # Api
    api = attr.ib(repr=False)

    # Entities
    Group = PartialSelf(GroupManager)
    Photo = PartialSelf(PhotoManager)
    Post = PartialSelf(PostManager)
    User = PartialSelf(UserManager)

    @classmethod
    def create(cls, access_token=None):
        api = create_api(access_token)
        return cls(api=api)
