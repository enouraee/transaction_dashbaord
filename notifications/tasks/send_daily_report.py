from celery import shared_task

from notifications.models import Notification
from notifications.tasks import process_notification
from transactions.models import TransactionSummary


@shared_task
def send_daily_reports():
    # Get the date for the report (yesterday)
    from datetime import datetime, timedelta

    report_date = datetime.utcnow() - timedelta(days=1)
    report_date_str = report_date.strftime("%Y-%m-%d")

    # Get all merchant IDs from TransactionSummary for the report date
    merchant_ids = TransactionSummary.objects(date=report_date).distinct("merchantId")

    # Define a mapping of merchant IDs to their contact info and names(Mock)
    merchant_info = {
        "merchant_id_1": {
            "email": "63a69a2d18f9347bd89d5f76",
            "phone": "1234567890",
            "name": "Merchant One",
        },
        "merchant_id_2": {
            "email": "63a69a2d18f9347bd89d5f0a",
            "phone": "1234567891",
            "name": "Merchant Two",
        },
    }

    for merchant_id in merchant_ids:
        # Convert merchant_id to string if necessary
        merchant_id_str = str(merchant_id)

        # Get transaction summaries for the merchant
        # Assuming you have separate summaries for 'count' and 'amount'
        count_summary = TransactionSummary.objects(
            merchantId=merchant_id, date=report_date, stat_type="count", mode="daily"
        ).first()

        amount_summary = TransactionSummary.objects(
            merchantId=merchant_id, date=report_date, stat_type="amount", mode="daily"
        ).first()

        if not count_summary or not amount_summary:
            continue  # No transactions for this merchant on this date

        # Get merchant info from the mapping
        info = merchant_info.get(merchant_id_str, "merchant_data")
        if not info:
            # Skip if no contact info is available for this merchant
            print(f"No contact info for merchant ID {merchant_id_str}")
            continue

        recipient_contact = {
            "email": info["email"],
            "phone": info["phone"],
        }
        merchant_name = info["name"]

        # Create notification
        notification = Notification(
            recipient_id=merchant_id,
            recipient_contact=recipient_contact,
            mediums=["email", "sms"],
            template_name="daily_report",
            context_data={
                "merchant_name": merchant_name,
                "transaction_count": count_summary.value,
                "transaction_amount": amount_summary.value,
                "date": report_date_str,
            },
        )
        notification.save()

        # Enqueue the notification for processing
        task = process_notification.delay(str(notification.id))
        notification.task_id = task.id
        notification.save()
