import json
import numpy as np
import joblib
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


class Command(BaseCommand):
    help = "Train a machine learning model for delivery time prediction"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("📊 Starting model training..."))

        # Load cleaned data
        file_path = "cleaned_data.json"
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        X = []
        y = []

        for item in data:
            pickup_delay = max(0, int(item["pickup_time"].split(":")[0]) - int(item["order_time"].split(":")[0]))
            is_weekend = 1 if item["day_of_week"] in [5, 6] else 0


            traffic_level = item["peak_hour"]
            weather_impact = item.get("weather_condition", 0)
            historical_performance = item.get("agent_past_avg_delivery_time", 30)

            X.append([
                item["agent_age"],
                item["agent_rating"],
                item["distance_km"],
                item["day_of_week"],
                pickup_delay,
                is_weekend,
                traffic_level,
                weather_impact,
                historical_performance
            ])
            y.append(item["delivery_time"])

        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)

        # Clip outliers in target variable
        lower_bound, upper_bound = np.percentile(y, [1, 99])
        y = np.clip(y, lower_bound, upper_bound)

        # Scale features
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Split into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf = RandomForestRegressor()
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='r2', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_rf = grid_search.best_estimator_

        # Train Gradient Boosting and XGBoost
        gb = GradientBoostingRegressor(n_estimators=200, max_depth=10, random_state=42)
        gb.fit(X_train, y_train)

        xgb = XGBRegressor(n_estimators=200, max_depth=10, random_state=42)
        xgb.fit(X_train, y_train)

        models = {"Random Forest": best_rf, "Gradient Boosting": gb, "XGBoost": xgb}
        for name, model in models.items():
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            self.stdout.write(self.style.SUCCESS(f"✅ {name} Model - MAE: {mae:.2f}, R² Score: {r2:.2f}"))

        best_model = max(models.items(), key=lambda x: r2_score(y_test, x[1].predict(X_test)))[1]
        model_path = "trained_model.pkl"
        joblib.dump(best_model, model_path)

        self.stdout.write(self.style.SUCCESS(f"💾 Best Model saved as {model_path}"))
