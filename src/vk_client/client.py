import attr
from vk_client.api import create_api
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
    Comment = attr.ib(default=attr.Factory(CommentManager, takes_self=True))
    Group = attr.ib(default=attr.Factory(GroupManager, takes_self=True))
    Photo = attr.ib(default=attr.Factory(PhotoManager, takes_self=True))
    Post = attr.ib(default=attr.Factory(PostManager, takes_self=True))
    User = attr.ib(default=attr.Factory(UserManager, takes_self=True))

    @classmethod
    def create(cls, access_token=None, captcha_handler=None):
        api = create_api(
            access_token=access_token,
            captcha_handler=captcha_handler
        )
        return cls(api=api)
