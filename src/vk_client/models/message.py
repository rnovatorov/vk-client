import more_itertools as mit
import cached_property
from vk_client import config, errors, utils, validators
from vk_client.models import _base, _mixins


class Message(
    _base.Model,
    _mixins.HasId,
    _mixins.HasUser,

):
    def __init__(self, vk, id, user_id, date, read_state, out, title, body,
                 geo, attachments, fwd_messages, emoji, important, deleted,
                 random_id):
        assert validators.positive(id)

        super(Message, self).__init__(vk)

        self._id = id

    @cached_property.cached_property
    def _data(self):
        raise NotImplementedError


class MessageManager(_base.ModelManager):

    _model = Message
