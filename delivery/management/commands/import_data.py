import csv
from datetime import datetime, time
from django.core.management.base import BaseCommand
from delivery.models import SupplyChain

class Command(BaseCommand):
    help = "Import delivery data from CSV"

    def handle(self, *args, **kwargs):
        file_path = "/home/gee/Documents/supply_chain_dt.csv"
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                order_time = row["Order_Time"].strip()
                pickup_time = row["Pickup_Time"].strip()

                if order_time.lower() in ["nan", ""]:
                    order_time = time(0, 0, 0)
                else:
                    order_time = datetime.strptime(order_time, "%H:%M:%S").time()

                if pickup_time.lower() in ["nan", ""]:
                    pickup_time = time(0, 0, 0)  # Default to 00:00:00
                else:
                    pickup_time = datetime.strptime(pickup_time, "%H:%M:%S").time()

                order_date = datetime.strptime(row["Order_Date"], "%Y-%m-%d").date()

                if not SupplyChain.objects.filter(order_id=row["Order_ID"]).exists():
                    SupplyChain.objects.create(
                        order_id=row["Order_ID"],
                        agent_age=int(row["Agent_Age"]),
                        agent_rating=float(row["Agent_Rating"]) if row["Agent_Rating"].strip() else 0.0,
                        store_latitude=float(row["Store_Latitude"]),
                        store_longitude=float(row["Store_Longitude"]),
                        drop_latitude=float(row["Drop_Latitude"]),
                        drop_longitude=float(row["Drop_Longitude"]),
                        order_date=order_date,
                        order_time=order_time,
                        pickup_time=pickup_time,
                        weather=row["Weather"],
                        traffic=row["Traffic"],
                        vehicle=row["Vehicle"],
                        area=row["Area"],
                        delivery_time=int(row["Delivery_Time"]),
                        category=row["Category"],
                    )
        self.stdout.write(self.style.SUCCESS("Successfully imported data ✅"))
