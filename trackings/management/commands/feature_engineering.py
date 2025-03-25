import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Perform feature engineering on shipment data"

    def handle(self, *args, **kwargs):
        try:
            print("🚀 Starting feature engineering...")

            # Load cleaned dataset
            df = pd.read_json("shipments_filled.json")

            # Convert timestamps to datetime
            df["actual_arrival"] = pd.to_datetime(df["actual_arrival"])
            df["estimated_arrival"] = pd.to_datetime(df["estimated_arrival"])

            # Rename estimated_arrival to scheduled_arrival for consistency
            df.rename(columns={"estimated_arrival": "scheduled_arrival"}, inplace=True)

            # Create new features
            df["arrival_day"] = df["actual_arrival"].dt.dayofweek  # Monday=0, Sunday=6
            df["arrival_hour"] = df["actual_arrival"].dt.hour  # Extract hour of the day
            df["delay_minutes"] = (df["actual_arrival"] - df["scheduled_arrival"]).dt.total_seconds() / 60  # Convert to minutes

            # Drop rows with negative delay (if any)
            df = df[df["delay_minutes"] >= 0]

            # Save the new dataset
            df.to_csv("shipments_features.csv", index=False)

            self.stdout.write(self.style.SUCCESS("✅ Feature Engineering Done! Data saved as 'shipments_features.csv' 🚀"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {e}"))
