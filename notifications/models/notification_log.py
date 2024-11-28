from datetime import datetime

import mongoengine as me

from notifications.models import Notification


class NotificationLog(me.Document):
    """
    A MongoEngine Document to log each send attempt of a notification.

    Fields:
        notification (ReferenceField): Reference to the Notification.
        medium (StringField): The medium used to send the notification.
        status (StringField): Status of the send attempt ('pending', 'sent', 'failed').
        attempts (IntField): Number of attempts made to send the notification.
        last_attempt_at (DateTimeField): Timestamp of the last attempt.
        response (StringField): Response or error message from the medium.
        created_at (DateTimeField): Timestamp when the log entry was created.
    """

    notification = me.ReferenceField(
        Notification, required=True, reverse_delete_rule=me.CASCADE
    )
    medium = me.StringField(required=True)
    status = me.StringField(
        choices=("pending", "sent", "failed"), default="pending", required=True
    )
    attempts = me.IntField(default=0)
    last_attempt_at = me.DateTimeField()
    response = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "notification_logs",
        "indexes": [
            "notification",
            "medium",
            "status",
            "last_attempt_at",
        ],
    }
