from .base import NotificationMedium


class SMSMedium(NotificationMedium):
    """
    Concrete implementation for SMS notifications.
    """

    def send_message(self, notification):
        # Simulate sending SMS
        template = self.get_template(notification.template_name)
        message = self.render_template(template, notification.context_data)
        phone_number = notification.recipient_contact.get("phone", "09121111111")

        # Simulate sending SMS (e.g., print or integrate with SMS API)
        print(f"Sending SMS to {phone_number}: {message}")

        # Return success response
        return {"status": "sent", "message": "SMS sent successfully."}

    def get_template(self, template_name):
        from notifications.models import NotificationTemplate

        template = NotificationTemplate.objects(
            name=template_name, medium="sms"
        ).first()
        if not template:
            raise ValueError(f"Template '{template_name}' for SMS not found.")
        return template.content

    def render_template(self, template_content, context_data):
        from django.template import Context, Template

        template = Template(template_content)
        context = Context(context_data)
        return template.render(context)
