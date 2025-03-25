from django.db import models
import uuid

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('in_transit', 'IN TRANSIT'),
        ('delivered', 'DELIVERED'),
        ('delayed', 'DELAYED'),
    ]

    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_transit')
    estimated_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    weather_conditions = models.CharField(max_length=50, blank=True, null=True)
    traffic_data = models.CharField(max_length=50, blank=True, null=True)
    shipment_type = models.CharField(max_length=50, choices=[('fragile', 'Fragile'), ('standard', 'Standard')], default='standard')
    carrier_details = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Shipment {self.tracking_id} - {self.status}"