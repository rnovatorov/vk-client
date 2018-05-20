import time
import vk
from vk_client import config


def create_api(access_token=None, captcha_handler=None):
    if captcha_handler is not None:
        session_class = type("Session", (vk.Session,), {
            "get_captcha_key": captcha_handler
        })
    else:
        session_class = vk.Session
    session = session_class(access_token)

    sleep_hook = create_sleep_hook(config.API_RATE_LIMIT)
    session.requests_session.hooks["response"].append(sleep_hook)

    return vk.API(session, v=config.API_VERSION)


def create_sleep_hook(seconds):
    def hook(r, *args, **kwargs):
        time.sleep(seconds)
    return hook
