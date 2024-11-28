import datetime

from bson import ObjectId
from django.core.management.base import BaseCommand
from pymongo import UpdateOne

from transactions.helpers import (
    construct_aggregation_group_and_sort_fields,
    format_group_id_to_date_key,
)
from transactions.models import Transaction, TransactionSummary


class Command(BaseCommand):
    help = "Updates the transaction summary data"

    def handle(self, *args, **options):
        modes = ["daily", "weekly", "monthly"]

        for mode in modes:
            self.update_transaction_summary(mode, group_by_merchant=False)
            self.update_transaction_summary(mode, group_by_merchant=True)

    def update_transaction_summary(self, mode, group_by_merchant):
        group_id, sort_fields = construct_aggregation_group_and_sort_fields(mode)

        if group_by_merchant:
            # Include merchantId in group_id
            group_id["merchantId"] = "$merchantId"

        # Build the aggregation pipeline
        pipeline = [
            {
                "$group": {
                    "_id": group_id,
                    "total_amount": {"$sum": "$amount"},
                    "total_count": {"$sum": 1},
                }
            },
        ]

        # Perform the aggregation
        results = Transaction.objects.aggregate(*pipeline)

        # Prepare bulk operations for efficiency
        bulk_ops = []
        for result in results:
            group_id = result["_id"]
            merchant_id = group_id.get("merchantId")
            if "merchantId" in group_id and merchant_id is None:
                merchant_id = None  # Ensure merchantId is explicitly None
            key = format_group_id_to_date_key(group_id, mode)
            date = self.get_start_date(group_id, mode)

            for stat_type in ["amount", "count"]:
                value = (
                    result["total_amount"]
                    if stat_type == "amount"
                    else result["total_count"]
                )

                # Prepare the update operation
                query = {
                    "mode": mode,
                    "stat_type": stat_type,
                    "key": key,
                    "merchantId": merchant_id,  # Always include merchantId, even if None
                }

                update = {
                    "$set": {
                        "value": value,
                        "date": date,
                    }
                }

                bulk_ops.append(UpdateOne(query, update, upsert=True))

        if bulk_ops:
            # Perform bulk write operation
            TransactionSummary._get_collection().bulk_write(bulk_ops)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully updated {len(bulk_ops)} summaries for mode: {mode}, group_by_merchant: {group_by_merchant}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"No summaries to update for mode: {mode}, group_by_merchant: {group_by_merchant}"
                )
            )

    def get_start_date(self, group_id, mode):
        """
        Returns the start date of the period based on the grouping mode.

        Parameters:
        - group_id (dict): The group identifier from the aggregation result.
        - mode (str): The grouping mode, can be 'daily', 'weekly', or 'monthly'.

        Returns:
        - date (datetime): The start date of the period.
        """
        if mode == "daily":
            date = datetime.datetime(
                group_id["year"], group_id["month"], group_id["day"]
            )
        elif mode == "weekly":
            iso_year = group_id["isoYear"]
            iso_week = group_id["isoWeek"]
            date = datetime.datetime.strptime(f"{iso_year}-W{iso_week}-1", "%G-W%V-%u")
        elif mode == "monthly":
            date = datetime.datetime(group_id["year"], group_id["month"], 1)
        else:
            raise ValueError("Mode must be 'daily', 'weekly', or 'monthly'")
        return date
