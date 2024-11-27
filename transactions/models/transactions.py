import mongoengine as me


class Transaction(me.Document):
    """
    A MongoEngine Document class to represent a transaction record.

    Attributes:
        merchantId (me.ObjectIdField):
            The unique identifier for the merchant associated with the transaction.
            Stored as an ObjectId in MongoDB.

        amount (me.DecimalField):
            The amount of the transaction.
            This field supports high-precision decimal values, suitable for financial data.

        createdAt (me.DateTimeField):
            The timestamp indicating when the transaction was created.
            Useful for sorting and tracking transaction history.

    Notes:
        - This class is a direct representation of a MongoDB collection document.
    """

    merchantId = me.ObjectIdField()
    amount = me.DecimalField()
    createdAt = me.DateTimeField()
