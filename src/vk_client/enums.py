import enum


class LikableType(enum.Enum):

    COMMENT = "comment"
    PHOTO = "photo"
    POST = "post"


class GroupEventType(enum.Enum):

    # Messages
    MESSAGE_NEW = "message_new"
    MESSAGE_REPLY = "message_reply"
    MESSAGE_ALLOW = "message_allow"
    MESSAGE_DENY = "messages_deny"

    # Photos
    PHOTO_NEW = "photo_new"
    PHOTO_COMMENT_NEW = "photo_comment_new"
    PHOTO_COMMENT_EDIT = "photo_comment_edit"
    PHOTO_COMMENT_RESTORE = "photo_comment_restore"
    PHOTO_COMMENT_DELETE = "photo_comment_delete"

    # Audio
    AUDIO_NEW = "audio_new"

    # Video
    VIDEO_NEW = "video_new"
    VIDEO_COMMENT_NEW = "video_comment_new"
    VIDEO_COMMENT_EDIT = "video_comment_edit"
    VIDEO_COMMENT_RESTORE = "video_comment_restore"
    VIDEO_COMMENT_DELETE = "video_comment_delete"

    # Wall posts
    WALL_POST_NEW = "wall_post_new"
    WALL_REPOST = "wall_repost"

    # Wall comments
    WALL_REPLY_NEW = "wall_reply_new"
    WALL_REPLY_EDIT = "wall_reply_edit"
    WALL_REPLY_RESTORE = "wall_reply_restore"
    WALL_REPLY_DELETE = "wall_reply_delete"

    # Boards
    BOARD_POST_NEW = "board_post_new"
    BOARD_POST_EDIT = "board_post_edit"
    BOARD_POST_RESTORE = "board_post_restore"
    BOARD_POST_DELETE = "board_post_delete"

    # Market
    MARKET_COMMENT_NEW = "market_comment_new"
    MARKET_COMMENT_EDIT = "market_comment_edit"
    MARKET_COMMENT_RESTORE = "market_comment_restore"
    MARKET_COMMENT_DELETE = "market_comment_delete"

    # Users
    GROUP_LEAVE = "group_leave"
    GROUP_JOIN = "group_join"
    USER_BLOCK = "user_block"
    USER_UNBLOCK = "user_unblock"

    # Other
    POLL_VOTE_NEW = "poll_vote_new"
    GROUP_OFFICERS_EDIT = "group_officers_edit"
    GROUP_CHANGE_SETTINGS = "group_change_settings"
    GROUP_CHANGE_PHOTO = "group_change_photo"
    VKPAY_TRANSACTION = "vkpay_transaction"


class GroupJoinType(enum.Enum):

    JOIN = "join"
    UNSURE = "unsure"
    ACCEPTED = "accepted"
    APPROVED = "approved"
    REQUEST = "request"
