from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from datetime import timedelta
from django.http import JsonResponse
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({
                'status':403,
                'errors':serializer.errors,
                'message':'Something error'
            })
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj , _ = Token.objects.get_or_create(user=user)
        return Response({
                'status':200,
                'payload':serializer.data,
                'token':str(token_obj),
                'message':'Your data is saved'
            })

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed')
    on_time_delivery_pos = completed_pos.filter(
        delivery_date__lte=F('delivery_date'))
    if completed_pos.exists():
        return on_time_delivery_pos.count() / completed_pos.count()
    return 0.0


def calculate_quality_rating_avg(vendor):
    completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed')
    quality_ratings = completed_pos.exclude(quality_rating__isnull=True)
    if quality_ratings.exists():
        return quality_ratings.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    return 0.0


def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False)
    if acknowledged_pos.exists():
        response_times = acknowledged_pos.annotate(
            response_time=F('acknowledgment_date') - F('issue_date')
        ).aggregate(avg_response=Avg('response_time'))
        # in hours
        return response_times['avg_response'].total_seconds() / 3600
    return 0.0


def calculate_fulfillment_rate(vendor):
    all_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfilled_pos = all_pos.filter(
        status='completed').exclude(quality_rating__lt=1)
    if all_pos.exists():
        return successful_fulfilled_pos.count() / all_pos.count()
    return 0.0


class VendorViewset(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        vendor = self.queryset.get(pk=pk)
        serializer = self.serializer_class(vendor)
        return Response(serializer.data)

    def update(self, request, pk=None):
        vendor = self.queryset.get(pk=pk)
        serializer = self.serializer_class(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        vendor = self.queryset.get(pk=pk)
        vendor.delete()
        return Response(status=204)

    @action(detail=True, methods=['get'], url_path='performance')
    def vendor_performance(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
            quality_rating_avg = calculate_quality_rating_avg(vendor)
            average_response_time = calculate_average_response_time(vendor)
            fulfillment_rate = calculate_fulfillment_rate(vendor)

            return JsonResponse({
                'vendor_id': pk,
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': average_response_time,
                'fulfillment_rate': fulfillment_rate
            })
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor does not exist'}, status=404)


class PurchaseOrderViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        PurchaseOrder = self.queryset.get(pk=pk)
        serializer = self.serializer_class(PurchaseOrder)
        return Response(serializer.data)

    def update(self, request, pk=None):
        PurchaseOrder = self.queryset.get(pk=pk)
        serializer = self.serializer_class(PurchaseOrder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        PurchaseOrder = self.queryset.get(pk=pk)
        PurchaseOrder.delete()
        return Response(status=204)

    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        try:
            # purchase_order = self.get_object()
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            serializer = self.serializer_class(purchase_order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist.'}, status=404)
