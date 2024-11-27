from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.IntegerField()
