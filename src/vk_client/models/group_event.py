from vk_client import enums, validators
from vk_client.models import _base, _mixins


class GroupEvent(_base.Model):

    def __init__(self, vk, type, object):
        super(GroupEvent, self).__init__(vk)

        self.type = type
        self.object = object


class GroupLeave(_base.Model, _mixins.HasUser):

    def __init__(self, vk, user_id, himself):
        assert validators.positive(user_id)

        super(GroupLeave, self).__init__(vk)

        self._user_id = user_id
        self.himself = himself


class GroupJoin(_base.Model, _mixins.HasUser):

    def __init__(self, vk, user_id, join_type):
        assert validators.positive(user_id)

        super(GroupJoin, self).__init__(vk)

        self._user_id = user_id
        self.join_type = join_type


class GroupEventManager(_base.ModelManager):

    _model = GroupEvent

    def from_update(self, type, object):
        type = enums.GroupEventType(type)

        # Messages
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
            enums.GroupEventType.MESSAGE_ALLOW,
            enums.GroupEventType.MESSAGE_DENY
        ]:
            return self(
                type=type,
                object=self._vk.User(
                    id=object["user_id"],
                )
            )

        # Photos
        elif type in [
            enums.GroupEventType.PHOTO_NEW
        ]:
            return self(
                type=type,
                object=self._vk.Photo(
                    id=object["id"],
                    owner_id=object["owner_id"]
                )
            )

        # TODO: Add all event types for Photos section.

        # Audio
        # TODO: Implement.

        # Video
        # TODO: Implement.

        # Wall posts
        # TODO: Implement.

        # Wall comments
        # TODO: Implement.

        # Boards
        # TODO: Implement.

        # Market
        # TODO: Implement.

        # Users
        elif type in [
            enums.GroupEventType.GROUP_LEAVE
        ]:
            return self(
                type=type,
                object=GroupLeave(
                    self._vk,
                    user_id=object["user_id"],
                    himself=bool(object["self"])
                )
            )

        elif type in [
            enums.GroupEventType.GROUP_JOIN
        ]:
            return self(
                type=type,
                object=GroupJoin(
                    self._vk,
                    user_id=object["user_id"],
                    join_type=enums.GroupJoinType(object["join_type"])
                )
            )

        # TODO: Add all event types for Users section.

        # Other
        # TODO: Implement.

        else:
            raise NotImplementedError
