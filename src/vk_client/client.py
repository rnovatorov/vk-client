import attr
import vk
from vk_client import config
from vk_client.utils import PartialSelf, create_sleep_hook
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
        session = vk.Session(access_token)
        sleep_hook = create_sleep_hook(config.API_RATE_LIMIT)
        session.requests_session.hooks["response"].append(sleep_hook)
        api = vk.API(session, v=config.API_VERSION)

        return cls(api=api)
