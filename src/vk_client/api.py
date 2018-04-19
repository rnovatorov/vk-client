import time
import vk
from vk_client import config


def create_api(access_token):
    session = vk.Session(access_token)
    sleep_hook = create_sleep_hook(config.API_RATE_LIMIT)
    session.requests_session.hooks["response"].append(sleep_hook)
    return vk.API(session, v=config.API_VERSION)


def create_sleep_hook(seconds):
    def hook(r, *args, **kwargs):
        time.sleep(seconds)
    return hook
