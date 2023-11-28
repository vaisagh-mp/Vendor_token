from rest_framework import serializers
from .models import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'vendor_code', 'name', 'contact_details', 'address')


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'issue_date', 'items', 'quantity', 'status', 'acknowledgment_date')


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ('id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')