import attr
from vk_client.models.base import Model, ModelManager


@attr.s
class GroupEvent(Model):

    type = attr.ib()
    _object = attr.ib()


@attr.s
class GroupEventManager(ModelManager):

    _model = GroupEvent
