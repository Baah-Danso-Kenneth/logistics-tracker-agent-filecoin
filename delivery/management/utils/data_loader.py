import numpy as np
import json
from sklearn.preprocessing import StandardScaler

def load_cleaned_data(file_path="cleaned_data.json"):
    """Loads and processes cleaned JSON data"""
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    X, y = [], []
    for item in data:
        pickup_delay = max(0, int(item["pickup_time"].split(":")[0]) - int(item["order_time"].split(":")[0]))
        is_weekend = 1 if item["day_of_week"] in [5, 6] else 0

        X.append([
            item["agent_age"],
            item["agent_rating"],
            item["distance_km"],
            item["day_of_week"],
            item["peak_hour"],
            pickup_delay,
            is_weekend
        ])
        y.append(item["delivery_time"])

    return np.array(X), np.array(y)

def process_input(agent_age, agent_rating, distance_km, day_of_week, peak_hour, pickup_delay):
    """Processes a single input into the correct format for prediction"""
    scaler = StandardScaler()
    input_data = np.array([[agent_age, agent_rating, distance_km, day_of_week, peak_hour, pickup_delay, 1 if day_of_week in [5, 6] else 0]])
    return scaler.fit_transform(input_data)
