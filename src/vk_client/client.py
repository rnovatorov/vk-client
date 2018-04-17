import attr
import vk
from vk_client import config
from vk_client.utils import PartialSelf, create_sleep_hook
from vk_client.entities.user import UserManager
from vk_client.entities.link import LinkManager


@attr.s
class VkClient(object):

    api = attr.ib()

    User = PartialSelf(UserManager)
    Link = PartialSelf(LinkManager)

    @classmethod
    def create(cls, access_token=None):
        session = vk.Session(access_token)

        sleep_hook = create_sleep_hook(config.API_RATE_LIMIT)
        session.requests_session.hooks["response"].append(sleep_hook)

        api = vk.API(session, v=config.API_VERSION)

        return cls(api=api)
