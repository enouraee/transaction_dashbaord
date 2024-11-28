from datetime import datetime

import mongoengine as me


class NotificationTemplate(me.Document):
    """
    A MongoEngine Document to store notification templates.

    Fields:
        name (StringField): The unique name of the template.
        medium (StringField): The medium for which this template is designed.
        content (StringField): The template content.
        created_at (DateTimeField): Timestamp when the template was created.
    """

    name = me.StringField(required=True)
    medium = me.StringField(required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "notification_templates",
        "indexes": [
            {"fields": ("name", "medium"), "unique": True},
        ],
    }
