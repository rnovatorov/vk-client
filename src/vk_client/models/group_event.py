from vk_client import enums, validators
from vk_client.models import _base, _mixins


class GroupEvent(_base.Model):

    def __init__(self, vk, type, object):
        super(GroupEvent, self).__init__(vk)

        self.type = type
        self.object = object


class MessageAllow(_base.Model, _mixins.HasUser):

    def __init__(self, vk, user_id, key):
        assert validators.positive(user_id)

        super(MessageAllow, self).__init__(vk)

        self._user_id = user_id
        self.key = key


class MessageDeny(_base.Model, _mixins.HasUser):

    def __init__(self, vk, user_id):
        assert validators.positive(user_id)

        super(MessageDeny, self).__init__(vk)

        self._user_id = user_id


class GroupEventManager(_base.ModelManager):

    _model = GroupEvent

    def from_update(self, type, object):
        type = enums.GroupEventType(type)

        if type in [
            enums.GroupEventType.MESSAGE_NEW,
            enums.GroupEventType.MESSAGE_REPLY
        ]:
            return self(
                type=type,
                object=self._vk.Message(
                    id=object["id"]
                )
            )

        elif type in [
            enums.GroupEventType.MESSAGE_ALLOW
        ]:
            return self(
                type=type,
                object=MessageAllow(
                    self._vk,
                    user_id=object["user_id"],
                    key=object["key"]
                )
            )

        elif type in [
            enums.GroupEventType.MESSAGE_DENY
        ]:
            return self(
                type=type,
                object=MessageDeny(
                    self._vk,
                    user_id=object["user_id"]
                )
            )

        else:
            raise NotImplementedError
