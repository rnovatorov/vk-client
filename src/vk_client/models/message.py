import arrow
import more_itertools as mit
import cached_property
from collections import Iterable
from vk_client import validators
from vk_client.models import _base, _mixins


class Message(
    _base.Model,
    _mixins.HasId
):
    def __init__(self, vk, id):
        assert validators.positive(id)

        super(Message, self).__init__(vk)

        self._id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.id == self.id

        return NotImplemented

    def __repr__(self):
        return "Message({})".format(self.id)

    @property
    def text(self):
        return self._data["text"]

    @property
    def date(self):
        return arrow.get(self._data["date"])

    @property
    def sender(self):
        return self._vk.User(self._data["from_id"])

    @cached_property.cached_property
    def _data(self):
        response = self._vk.api.messages.getById(message_ids=self.id)
        return mit.one(response["items"])


class MessageManager(_base.ModelManager):

    _model = Message

    def broadcast(self, peers, message):
        assert isinstance(peers, Iterable)

        self._vk.api.messages.send(
            peer_ids=','.join(str(peer.id) for peer in peers),
            message=message
        )

    def send(self, peer, message):
        self._vk.api.messages.send(
            peer_id=peer.id,
            message=message
        )
