from django.db import models
from django.utils import timezone
from django.db.models import Avg

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()

        # Calculate on-time delivery rate
        on_time_deliveries = completed_orders.filter(delivery_date__lte=timezone.now()).count()
        self.on_time_delivery_rate = (on_time_deliveries / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        # Calculate quality rating average
        completed_orders_with_rating = completed_orders.filter(quality_rating__isnull=False)
        self.quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        # Calculate average response time
        acknowledged_orders = completed_orders.exclude(acknowledgment_date=None)
        total_acknowledged_orders = acknowledged_orders.count()
        total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() / 3600 for order in acknowledged_orders)
        self.average_response_time = total_response_time / total_acknowledged_orders if total_acknowledged_orders > 0 else 0

        # Calculate fulfillment rate
        successfully_fulfilled_orders = completed_orders.filter(status='completed').count()
        self.fulfillment_rate = (successfully_fulfilled_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
