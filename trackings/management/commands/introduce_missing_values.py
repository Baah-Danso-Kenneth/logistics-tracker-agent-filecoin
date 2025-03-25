import json
import random
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Introduce missing values into 'actual_arrival' field in shipments.json"

    def handle(self, *args, **kwargs):
        try:
            with open("shipments.json", "r") as file:
                shipments = json.load(file)

            for shipment in shipments:
                if random.random() < 0.2:  # 20% probability to make it null
                    shipment["actual_arrival"] = None

            with open("shipments_with_missing.json", "w") as file:
                json.dump(shipments, file, indent=4)

            self.stdout.write(self.style.SUCCESS("✅ Missing values introduced! Check 'shipments_with_missing.json'."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("❌ Error: 'shipments.json' not found!"))
