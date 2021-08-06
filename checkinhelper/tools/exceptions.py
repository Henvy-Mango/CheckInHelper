from checkinhelper.tools.utils import log


class CheckinHelperException(Exception):
    """Base checkinhelper exception."""

    def __init__(self, message):
        super().__init__(message)
        log.error(message)


class CookiesExpired(CheckinHelperException):
    """Cookies has expired."""


class NotificationError(CheckinHelperException):
    """
    A notification error. Raised after an issue with the sent notification.
    """


class NoSuchNotifierError(CheckinHelperException):
    """
    An unknown notifier was requests, one that was not registered.
    """
