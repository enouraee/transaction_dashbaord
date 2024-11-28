from datetime import datetime

import mongoengine as me


class Notification(me.Document):
    """
    A MongoEngine Document to represent a notification to be sent.

    Fields:
        recipient_id (ObjectIdField): The ID of the recipient user.
        recipient_contact (DictField): Contact details like email, phone number.
        mediums (ListField): List of mediums to send the notification through.
        template_name (StringField): The name of the template to use.
        context_data (DictField): Data to render the template.
        status (StringField): The status of the notification ('pending', 'sent', 'failed').
        created_at (DateTimeField): Timestamp when the notification was created.
        task_id (StringField): The Celery task ID associated with sending this notification.
    """

    recipient_id = me.ObjectIdField(required=True)
    recipient_contact = me.DictField(required=True)
    mediums = me.ListField(me.StringField(), required=True)
    template_name = me.StringField(required=True)
    context_data = me.DictField()
    status = me.StringField(
        choices=("pending", "sent", "failed"), default="pending", required=True
    )
    created_at = me.DateTimeField(default=datetime.utcnow)
    task_id = me.StringField()

    meta = {
        "collection": "notifications",
        "indexes": [
            "recipient_id",
            "status",
            "created_at",
        ],
    }
