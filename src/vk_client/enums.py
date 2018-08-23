import enum


class LikableType(enum.Enum):

    COMMENT = "comment"
    PHOTO = "photo"
    POST = "post"


class GroupEventType(enum.Enum):

    # TODO: Fill all sections

    # Messages
    MESSAGE_NEW = "message_new"
    MESSAGE_REPLY = "message_reply"
    MESSAGE_ALLOW = "message_allow"
    MESSAGE_DENY = "messages_deny"

    # Photos

    # Audio

    # Video

    # Wall posts

    # Wall comments

    # Boards

    # Market

    # Users

    # Other
