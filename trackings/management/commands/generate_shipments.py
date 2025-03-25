import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from trackings.models import Shipment

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake shipment data'

    def handle(self, *args, **kwargs):
        num_records = 100
        statuses = ['in_transit', 'delivered', 'delayed']
        weather_conditions = ['Clear', 'Rainy', 'Snowy', 'Stormy']
        traffic_data = ['Light', 'Moderate', 'Heavy']
        shipment_types = ['fragile', 'standard']

        for _ in range(num_records):
            origin = fake.city()
            destination = fake.city()
            status = random.choice(statuses)

            created_at = fake.date_time_between(start_date='-1y', end_date='now')
            estimated_arrival = created_at + timedelta(days=random.randint(1, 10))
            actual_arrival = estimated_arrival if status == 'delivered' else None

            Shipment.objects.create(
                origin=origin,
                destination=destination,
                status=status,
                estimated_arrival=estimated_arrival,
                actual_arrival=actual_arrival,
                weather_conditions=random.choice(weather_conditions),
                traffic_data=random.choice(traffic_data),
                shipment_type=random.choice(shipment_types),
                carrier_details=fake.company()
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_records} fake shipments!'))
