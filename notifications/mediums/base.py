from abc import ABC, abstractmethod


class NotificationMedium(ABC):
    """
    Abstract base class for notification mediums.
    """

    @abstractmethod
    def send_message(self, notification):
        pass
