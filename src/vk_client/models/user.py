import attr
from vk_client import validators
from vk_client.models._base import Model, model_manager


@attr.s
class User(Model):

    id = attr.ib(validator=validators.positive)


@attr.s
class UserManager(model_manager(User)):
    pass
