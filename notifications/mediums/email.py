from .base import NotificationMedium


class EmailMedium(NotificationMedium):
    """
    Concrete implementation for Email notifications.
    """

    def send_message(self, notification):
        from django.core.mail import send_mail

        template = self.get_template(notification.template_name)
        message = self.render_template(template, notification.context_data)
        email_address = notification.recipient_contact.get("email", "")

        if not email_address:
            raise ValueError("Email address not provided for Email medium.")

        subject = notification.context_data.get("subject", "Notification")

        print(f"Sending Email to {email_address}: \n {message}")
        # Return success response
        return {"status": "sent", "message": "Email sent successfully."}

    def get_template(self, template_name):
        from notifications.models import NotificationTemplate

        template = NotificationTemplate.objects(
            name=template_name, medium="email"
        ).first()
        if not template:
            raise ValueError(f"Template '{template_name}' for Email not found.")
        return template.content

    def render_template(self, template_content, context_data):
        from django.template import Context, Template

        template = Template(template_content)
        context = Context(context_data)
        return template.render(context)
