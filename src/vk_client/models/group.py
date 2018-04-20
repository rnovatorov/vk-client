import attr
from vk_client import validators
from vk_client.models._base import Model, model_manager


@attr.s
class Group(Model):

    id = attr.ib(validator=validators.negative)


@attr.s
class GroupManager(model_manager(Group)):
    pass
