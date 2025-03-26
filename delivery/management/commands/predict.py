import os
import time
import itertools
import numpy as np
import joblib
import pyfiglet
from django.core.management.base import BaseCommand
from rich import print

class Command(BaseCommand):
    help = "Predict delivery time based on user input"

    def handle(self, *args, **kwargs):
        os.system("cls" if os.name == "nt" else "clear")
        logo = pyfiglet.figlet_format("LOGISTICS", font="block")  # You can use 'block' or other bold fonts
        print(f"[bold cyan]\n{logo}[/bold cyan]")

        ship_animation = """
🚢 Supply Chain Terminal
-------------------------------------------------
                   |
                   |    |  |      
              )_)  )_)  )_)  )_)  
             )___))___))___))___) 
           )____)____)____)_____) 
       ____|____|____|____|____|____
  ----\\                   /---------
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

        wave_patterns = itertools.cycle([
            " ~~~~ ~~~~ ~~~~ ~~~~ ~~~~ ",
            "  ~~~~ ~~~~ ~~~~ ~~~~ ~~~~",
            "   ~~~~ ~~~~ ~~~~ ~~~~ ~~~",
            "    ~~~~ ~~~~ ~~~~ ~~~~ ~~",
            "   ~~~~ ~~~~ ~~~~ ~~~~ ~~~",
            "  ~~~~ ~~~~ ~~~~ ~~~~ ~~~~",
            " ~~~~ ~~~~ ~~~~ ~~~~ ~~~~ ",
        ])

        for _ in range(10):  # Animation plays for 10 frames
            os.system("cls" if os.name == "nt" else "clear")
            print(f"[bold cyan]{ship_animation}[/bold cyan]")
            print(f"[bold blue]{next(wave_patterns)}[/bold blue]")
            time.sleep(0.2)



        try:
            print("\n🚀 Welcome to [bold cyan]Logistics CLI[/bold cyan]!")

            agent_age = int(input("Agent Age: "))
            while agent_age < 18:
                print("Agent age must be above 18")
                agent_age= int(input("Agent Age: "))

            agent_rating = int(input("Agent Rating (1-5): "))
            while agent_rating < 1 or agent_rating > 5:
                print("Please enter a valid rating between 1 and 5.")
                agent_rating = int(input("Agent Rating (1-5): "))

            # Validate Distance (positive float)
            distance = float(input("Distance (km): "))
            while distance <= 0:
                print("Please enter a valid positive number for Distance.")
                distance = float(input("Distance (km): "))

            # Validate Day of the Week (0-6)
            day_of_week = int(input("Day of the Week (0=Monday, 6=Sunday): "))
            while day_of_week < 0 or day_of_week > 6:
                print("Please enter a valid number between 0 (Monday) and 6 (Sunday).")
                day_of_week = int(input("Day of the Week (0=Monday, 6=Sunday): "))

            # Validate Peak Hour (1 or 0)
            peak_hour = int(input("Peak Hour? (1 for Yes, 0 for No): "))
            while peak_hour not in [0, 1]:
                print("Please enter either 1 (Yes) or 0 (No) for Peak Hour.")
                peak_hour = int(input("Peak Hour? (1 for Yes, 0 for No): "))


            pickup_delay = float(input("Pickup Delay (hours): "))
            while pickup_delay < 0:
                print("Please enter a valid positive number for Pickup Delay.")
                pickup_delay = float(input("Pickup Delay (hours): "))

            # Validate Vehicle Type (0=Bike, 1=Car, 2=Truck)
            vehicle_type = int(input("Vehicle Type (0=Bike, 1=Car, 2=Truck): "))
            while vehicle_type not in [0, 1, 2]:
                print("Please enter a valid number (0=Bike, 1=Car, 2=Truck).")
                vehicle_type = int(input("Vehicle Type (0=Bike, 1=Car, 2=Truck): "))

            # Validate Traffic Condition (0=Low, 1=Medium, 2=High)
            traffic_condition = int(input("Traffic Condition (0=Low, 1=Medium, 2=High): "))
            while traffic_condition not in [0, 1, 2]:
                print("Please enter a valid number (0=Low, 1=Medium, 2=High) for Traffic Condition.")
                traffic_condition = int(input("Traffic Condition (0=Low, 1=Medium, 2=High): "))

            # Validate Weather Condition (0=Clear, 1=Rainy, 2=Snowy)
            weather_condition = int(input("Weather Condition (0=Clear, 1=Rainy, 2=Snowy): "))
            while weather_condition not in [0, 1, 2]:
                print("Please enter a valid number (0=Clear, 1=Rainy, 2=Snowy) for Weather Condition.")
                weather_condition = int(input("Weather Condition (0=Clear, 1=Rainy, 2=Snowy): "))

            input_data = np.array([
                agent_age, agent_rating, distance, day_of_week, peak_hour,
                pickup_delay, vehicle_type, traffic_condition, weather_condition
            ]).reshape(1, -1)

            model = joblib.load("trained_model.pkl")

            predicted_time = model.predict(input_data)

            print("\n⏳ [bold green]Processing prediction...[/bold green]")
            time.sleep(2)
            print(self.style.SUCCESS(f"\n🚚 Estimated Delivery Time: {predicted_time[0]:.2f} hours"))

        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"Invalid input: {e}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Model file not found! Ensure 'trained_model.pkl' exists."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
