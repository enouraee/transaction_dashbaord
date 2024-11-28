from bson import ObjectId
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import TransactionSummary
from transactions.serializers import TransactionSerializer


class TransactionSummaryView(APIView):
    """
    API view to retrieve precomputed transaction summaries based on type and mode.

    This endpoint provides aggregated data of transactions either by count or amount,
    grouped by daily, weekly, or monthly intervals. An optional merchant ID can be
    provided to filter transactions specific to a merchant.

    Query Parameters:
    - type (str): Required. Specifies the aggregation type, either 'count' or 'amount'.
    - mode (str): Required. Specifies the grouping interval, one of 'daily', 'weekly', or 'monthly'.
    - merchantId (str): Optional. The ObjectId of the merchant to filter transactions.

    Responses:
    - 200 OK: A list of aggregated transaction data with 'key' as the date grouping and 'value' as the aggregated amount or count.
    - 400 Bad Request: Returned when invalid query parameters are provided.
    """

    def get(self, request):
        stat_type = request.query_params.get("type")
        mode = request.query_params.get("mode")
        merchant_id = request.query_params.get("merchantId")

        # Validate inputs
        if stat_type not in ["count", "amount"]:
            return Response(
                {"error": "Invalid type parameter"}, status=status.HTTP_400_BAD_REQUEST
            )
        if mode not in ["daily", "weekly", "monthly"]:
            return Response(
                {"error": "Invalid mode parameter"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Build the query
        query = {
            "mode": mode,
            "stat_type": stat_type,
        }
        if merchant_id:
            try:
                merchant_obj_id = ObjectId(merchant_id)
                query["merchantId"] = merchant_obj_id
            except Exception:
                return Response(
                    {"error": "Invalid merchantId"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            query["merchantId"] = None  # Query for overall summaries

        # Retrieve data from TransactionSummary collection, sorted by date
        summaries = TransactionSummary.objects.filter(**query).order_by("date")

        # Prepare the response data
        response_data = []
        for summary in summaries:
            response_data.append(
                {
                    "key": summary.key,
                    "value": summary.value,
                }
            )

        # Use the serializer to serialize the response data
        serializer = TransactionSerializer(response_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
