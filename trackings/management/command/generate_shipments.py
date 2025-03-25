import random
from django.core.management.base import BaseCommand
from faker import Faker
from trackings.models import Shipment
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake shipment data'

    def handle(self, *args, **kwargs):
        num_records=100
        statuses = ['in_transit', 'delivered', 'delayed']
        for _ in range(num_records):
            origin = fake.city()
            destination = fake.city()
            status = random.choice(statuses)

            created_at = fake.date_time_between(start_day='-1y', end_date='now')
            estimated_arrival = created_at + timedelta(days=random.randint(1, 10))
            actual_arrival = estimated_arrival if status == 'delivered' else None

            Shipment.objects.create(
                origin=origin,
                destination=destination,
                status=status,
                estimated_arrival=estimated_arrival,
                actual_arrival=actual_arrival,
                created_at=created_at,
                updated_at=datetime.now()
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_records} fake shipments!'))