from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import *
from django.db.models import Avg

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from rest_framework import generics, status
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer, UserLoginSerializer

class UserSignup(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({"access_token": str(refresh.access_token), "refresh_token": str(refresh)}, status=status.HTTP_200_OK)




class PurchaseOrderDetailAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(po_number=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Recalculate and update vendor performance metrics
            purchase_order.vendor.update_performance_metrics()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if purchase_order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        
        # Recalculate and update vendor performance metrics
        purchase_order.vendor.update_performance_metrics()

        return Response(status=status.HTTP_204_NO_CONTENT)

class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    def get(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateAPIView(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Recalculate and update vendor performance metrics
            serializer.instance.vendor.update_performance_metrics()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_orders = completed_orders.count()
        on_time_deliveries = completed_orders.filter(delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        completed_orders_with_rating = completed_orders.filter(quality_rating__isnull=False)
        quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        acknowledged_orders = completed_orders.exclude(acknowledgment_date=None)
        total_acknowledged_orders = acknowledged_orders.count()
        total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() / 3600 for order in acknowledged_orders)
        average_response_time = total_response_time / total_acknowledged_orders if total_acknowledged_orders > 0 else 0

        successfully_fulfilled_orders = completed_orders.filter(status='completed').count()
        fulfillment_rate = (successfully_fulfilled_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        performance_metrics = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return Response(performance_metrics)