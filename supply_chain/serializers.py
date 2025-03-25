from rest_framework import serialziers
from trackings.models import Shipment

class ShipmentSerializer(serialziers.ModelSerializer):
    class Meta:
        model= Shipment
        fields = '__all__'