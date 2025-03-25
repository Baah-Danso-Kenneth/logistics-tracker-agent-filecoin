from django.contrib import admin
from trackings.models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'origin', 'destination', 'status', 'created_at')
