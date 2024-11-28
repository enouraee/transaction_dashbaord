from datetime import datetime

from celery import shared_task

from notifications.mediums.registry import MEDIUM_HANDLERS
from notifications.models import Notification, NotificationLog


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_notification(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.status == "sent":
            # Notification already processed
            return

        for medium_name in notification.mediums:
            medium_handler = MEDIUM_HANDLERS.get(medium_name)
            if not medium_handler:
                # Medium handler not found
                continue

            # Check if a log exists for this medium
            log = NotificationLog.objects(
                notification=notification, medium=medium_name
            ).first()

            if log and log.status == "sent":
                # Message already sent via this medium
                continue

            if not log:
                log = NotificationLog(
                    notification=notification,
                    medium=medium_name,
                    status="pending",
                    attempts=0,
                    created_at=datetime.utcnow(),
                )

            try:
                response = medium_handler.send_message(notification)
                log.status = "sent"
                log.response = response.get("message")
                log.last_attempt_at = datetime.utcnow()
                log.attempts += 1
                log.save()
            except Exception as e:
                log.status = "failed"
                log.response = str(e)
                log.last_attempt_at = datetime.utcnow()
                log.attempts += 1
                log.save()
                raise self.retry(exc=e)

        # Update notification status
        notification.status = "sent"
        notification.save()
    except Notification.DoesNotExist:
        # Notification not found
        pass

    except Exception as e:
        # General exception handling
        raise self.retry(exc=e)
