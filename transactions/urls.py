from django.urls import path

from .views import TransactionHistoryView, TransactionSummaryView

urlpatterns = [
    path(
        "transaction-history/",
        TransactionHistoryView.as_view(),
        name="transaction-history",
    ),
    path(
        "transaction-summary/",
        TransactionSummaryView.as_view(),
        name="transaction-summary",
    ),
]
