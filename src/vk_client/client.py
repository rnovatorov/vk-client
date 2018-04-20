import attr
from vk_client.api import create_api
from vk_client.utils import PartialSelf
from vk_client.models.comment import CommentManager
from vk_client.models.group import GroupManager
from vk_client.models.photo import PhotoManager
from vk_client.models.post import PostManager
from vk_client.models.user import UserManager


@attr.s
class VkClient(object):

    # Api
    api = attr.ib(repr=False)

    # Models
    Comment = PartialSelf(CommentManager)
    Group = PartialSelf(GroupManager)
    Photo = PartialSelf(PhotoManager)
    Post = PartialSelf(PostManager)
    User = PartialSelf(UserManager)

    @classmethod
    def create(cls, access_token=None):
        api = create_api(access_token)
        return cls(api=api)
