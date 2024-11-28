import mongoengine as me


class TransactionSummary(me.Document):
    """
    A MongoEngine Document class to represent a transaction summary record.

    Attributes:
        mode (str): The grouping mode, can be 'daily', 'weekly', or 'monthly'.
        stat_type (str): The aggregation type, either 'count' or 'amount'.
        merchantId (me.ObjectIdField): Optional. The unique identifier for the merchant associated with the summary.
        key (str): The date key, formatted as per the mode.
        value (Decimal): The aggregated amount or count.
        date (datetime): The start date of the period for sorting.
    """

    mode = me.StringField(required=True, choices=("daily", "weekly", "monthly"))
    stat_type = me.StringField(required=True, choices=("count", "amount"))
    merchantId = me.ObjectIdField(null=True, default=None)
    key = me.StringField(required=True)
    value = me.DecimalField(required=True)
    date = me.DateTimeField(required=True)

    meta = {
        "indexes": [
            {"fields": ["mode", "stat_type", "merchantId", "key"], "unique": True},
            {"fields": ["mode", "stat_type", "merchantId", "date"]},
        ]
    }
