import json
import uuid
from datetime import datetime
from django.core.management.base import BaseCommand
from trackings.models import Shipment

class Command(BaseCommand):
    help = "Export shipments data to a JSON file"

    def handle(self, *args, **kwargs):
        shipments = list(Shipment.objects.all().values())


        for shipment in shipments:
            for key, value in shipment.items():
                if isinstance(value, uuid.UUID):
                    shipment[key] = str(value)
                elif isinstance(value, datetime):
                    shipment[key] = value.isoformat()

        with open("shipments.json", "w") as file:
            json.dump(shipments, file, indent=4)

        self.stdout.write(self.style.SUCCESS("Successfully exported shipments to shipments.json"))
