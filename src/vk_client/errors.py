class VkClientError(Exception):
    """Generic error."""


class Unreachable(RuntimeError):
    """Raised when unreachable code reached."""


class NotFound(VkClientError):
    """Raised when model instance has not been found."""
