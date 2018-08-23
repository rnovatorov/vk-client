import attr
from vk_client.api import create_api
from vk_client.models.bots_long_poll import BotsLongPollManager
from vk_client.models.comment import CommentManager
from vk_client.models.group import GroupManager
from vk_client.models.group_event import GroupEventManager
from vk_client.models.photo import PhotoManager
from vk_client.models.post import PostManager
from vk_client.models.user import UserManager


@attr.s
class VkClient(object):

    # Api
    api = attr.ib(repr=False)

    # Models
    BotsLongPoll = attr.ib(
        default=attr.Factory(BotsLongPollManager, takes_self=True),
        repr=False
    )
    Comment = attr.ib(
        default=attr.Factory(CommentManager, takes_self=True),
        repr=False
    )
    Group = attr.ib(
        default=attr.Factory(GroupManager, takes_self=True),
        repr=False
    )
    GroupEvent = attr.ib(
        default=attr.Factory(GroupEventManager, takes_self=True),
        repr=False
    )
    Photo = attr.ib(
        default=attr.Factory(PhotoManager, takes_self=True),
        repr=False
    )
    Post = attr.ib(
        default=attr.Factory(PostManager, takes_self=True),
        repr=False
    )
    User = attr.ib(
        default=attr.Factory(UserManager, takes_self=True),
        repr=False
    )

    @classmethod
    def create(cls, access_token=None, captcha_handler=None):
        api = create_api(
            access_token=access_token,
            captcha_handler=captcha_handler
        )
        return cls(api=api)
