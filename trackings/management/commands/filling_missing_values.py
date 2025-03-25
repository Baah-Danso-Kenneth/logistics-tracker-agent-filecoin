import json
import pandas as pd
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fill missing values in 'actual_arrival' using median timestamp"

    def handle(self, *args, **kwargs):
        try:
            # Load JSON data
            df = pd.read_json("shipments_with_missing.json")

            # Convert actual_arrival to datetime format
            df["actual_arrival"] = pd.to_datetime(df["actual_arrival"], errors="coerce")

            # Compute median timestamp
            median_value = df["actual_arrival"].median()

            # Fill missing values properly (avoid chained assignment)
            df.loc[:, "actual_arrival"] = df["actual_arrival"].fillna(median_value)

            # Save the processed data
            df.to_json("shipments_filled.json", orient="records", indent=4, date_format="iso")

            self.stdout.write(
                self.style.SUCCESS("✅ Missing values filled using median! Saved as 'shipments_filled.json' 🚀"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("❌ Error: 'shipments_with_missing.json' not found!"))
